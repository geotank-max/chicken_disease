from datetime import datetime, timedelta
from sqlalchemy import func, or_, extract, desc
from extensions import db
from app.models.expert_system import (
    Case,
    Disease,
    Symptom,
    Rule,
    CASE_STATUS_PENDING,
    CASE_STATUS_CONFIRMED,
    CASE_STATUS_REJECTED,
)
from app.models.user import UserTable
from app.data.cambodia_geography import get_province_by_key


# Thresholds used to flag "high-risk" cases for the dashboard triage table.
HIGH_RISK_SICK_BIRDS = 10      # many sick birds reported
HIGH_RISK_DEAD_BIRDS = 3       # any notable mortality
LOW_CONFIDENCE_THRESHOLD = 50  # weak diagnosis confidence (percent)

# Tokens that mark a disease severity as dangerous. Severity is free text and
# may be Khmer ("ខ្ពស់" = high) or English ("High"), including combos such as
# "មធ្យម-ខ្ពស់".
DANGEROUS_SEVERITY_TOKENS = ("ខ្ពស់", "high", "severe", "critical")


class DashboardService:
    """Aggregates read-only analytics for the admin / doctor dashboard.

    All list/stat methods accept the same optional filters so the whole
    dashboard can be scoped by date range, disease and status together:
      - date_from / date_to : ISO date strings "YYYY-MM-DD" (inclusive)
      - disease_id          : filter by diagnosed disease
      - status              : one of pending / confirmed / rejected
    """

    # ── Filter helpers ─────────────────────────────────────────────────────
    @staticmethod
    def _parse_date(value: str, end_of_day: bool = False):
        if not value:
            return None
        try:
            dt = datetime.strptime(value, "%Y-%m-%d")
        except (ValueError, TypeError):
            return None
        if end_of_day:
            dt = dt.replace(hour=23, minute=59, second=59)
        return dt

    @classmethod
    def _apply_filters(cls, query, date_from=None, date_to=None,
                       disease_id=None, status=None):
        """Apply the shared dashboard filters to a Case query."""
        df = cls._parse_date(date_from)
        dt = cls._parse_date(date_to, end_of_day=True)
        if df:
            query = query.filter(Case.created_at >= df)
        if dt:
            query = query.filter(Case.created_at <= dt)
        if disease_id:
            query = query.filter(Case.disease_id == disease_id)
        if status:
            query = query.filter(Case.status == status)
        return query

    @classmethod
    def _base_query(cls, **filters):
        return cls._apply_filters(Case.query, **filters)

    # ── Summary cards ──────────────────────────────────────────────────────
    @classmethod
    def get_summary(cls, **filters) -> dict:
        """Headline counts. Respects the active filters where meaningful.

        Note: the status-specific counts (pending/confirmed/rejected) ignore an
        incoming ``status`` filter so each card still shows its own bucket;
        date range and disease filters still apply.
        """
        now = datetime.utcnow()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        status_free = dict(filters)
        status_free.pop("status", None)

        total_cases = cls._base_query(**filters).count()
        pending = cls._base_query(**status_free).filter(Case.status == CASE_STATUS_PENDING).count()
        confirmed = cls._base_query(**status_free).filter(Case.status == CASE_STATUS_CONFIRMED).count()
        rejected = cls._base_query(**status_free).filter(Case.status == CASE_STATUS_REJECTED).count()
        resolved = confirmed + rejected

        confirmation_rate = round((confirmed / resolved * 100), 1) if resolved > 0 else (100.0 if confirmed > 0 else 0.0)
        resolution_rate = round((resolved / total_cases * 100), 1) if total_cases > 0 else 0.0
        pending_percent = round((pending / total_cases * 100), 1) if total_cases > 0 else 0.0
        confirmed_percent = round((confirmed / total_cases * 100), 1) if total_cases > 0 else 0.0
        rejected_percent = round((rejected / total_cases * 100), 1) if total_cases > 0 else 0.0

        return {
            "total_cases": total_cases,
            "pending_reviews": pending,
            "confirmed_cases": confirmed,
            "rejected_cases": rejected,
            "cases_this_month": cls._base_query(**status_free)
                .filter(Case.created_at >= month_start).count(),
            "confirmation_rate": confirmation_rate,
            "resolution_rate": resolution_rate,
            "pending_percent": pending_percent,
            "confirmed_percent": confirmed_percent,
            "rejected_percent": rejected_percent,
            # Knowledge-base counts are global (not case-filtered).
            "total_diseases": Disease.query.count(),
            "total_symptoms": Symptom.query.count(),
            "total_rules": Rule.query.count(),
            "total_users": UserTable.query.count(),
        }

    # ── Top diseases (with percentage) ─────────────────────────────────────
    @classmethod
    def get_top_diseases(cls, limit: int = 6, **filters) -> list[dict]:
        base = cls._base_query(**filters).filter(Case.disease_id.isnot(None))
        total = base.count()

        rows = (
            base.with_entities(Disease.name, Disease.severity, func.count(Case.id).label("count"))
            .join(Disease, Case.disease_id == Disease.id)
            .group_by(Disease.id, Disease.name, Disease.severity)
            .order_by(func.count(Case.id).desc())
            .limit(limit)
            .all()
        )
        result = []
        for name, severity, count in rows:
            percent = round(count / total * 100, 1) if total else 0.0
            result.append({
                "name": name,
                "severity": severity or "",
                "count": count,
                "percent": percent,
                "is_dangerous": cls._is_dangerous_severity(severity),
            })
        return result

    # ── Disease trend over time ────────────────────────────────────────────
    @classmethod
    def get_cases_by_day(cls, days: int = 30, **filters) -> list[dict]:
        """Daily case counts for the trend chart.

        If an explicit date range is supplied it takes precedence over ``days``
        (capped to a sane maximum so the chart stays readable).
        """
        df = cls._parse_date(filters.get("date_from"))
        dt_to = cls._parse_date(filters.get("date_to"), end_of_day=True)

        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        if df:
            start = df.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            start = today - timedelta(days=days - 1)
        end = (dt_to or today).replace(hour=0, minute=0, second=0, microsecond=0)

        span = (end - start).days + 1
        if span < 1:
            span = 1
        span = min(span, 90)  # keep the chart readable

        # Reuse the shared filters but constrain to our computed window.
        trend_filters = dict(filters)
        trend_filters.pop("date_from", None)
        trend_filters.pop("date_to", None)
        query = cls._base_query(**trend_filters).filter(Case.created_at >= start)

        rows = (
            query.with_entities(func.date(Case.created_at).label("day"), func.count(Case.id))
            .group_by(func.date(Case.created_at))
            .order_by(func.date(Case.created_at))
            .all()
        )
        day_map = {str(day): count for day, count in rows}

        result = []
        for i in range(span):
            d = (start + timedelta(days=i)).date()
            result.append({"date": d.strftime("%m/%d"), "count": day_map.get(str(d), 0)})
        return result

    # ── Seasonal Mortality & Outbreaks (Sick vs Dead Birds) ────────────────
    @classmethod
    def get_seasonal_mortality(cls, **filters) -> dict:
        """Aggregates sick vs dead birds by month to identify peak seasonal mortality & outbreaks."""
        now = datetime.utcnow()
        year = now.year
        df = cls._parse_date(filters.get("date_from"))
        if df:
            year = df.year

        month_names = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

        base = cls._base_query(**filters)
        rows = (
            base.with_entities(
                extract("month", Case.created_at).label("month"),
                func.sum(func.coalesce(Case.sick_bird_count, 0)).label("sick"),
                func.sum(func.coalesce(Case.dead_bird_count, 0)).label("dead"),
                func.count(Case.id).label("case_count")
            )
            .group_by(extract("month", Case.created_at))
            .all()
        )

        month_map = {}
        for r in rows:
            if r.month is not None:
                m_idx = int(r.month)
                month_map[m_idx] = {
                    "sick": int(r.sick or 0),
                    "dead": int(r.dead or 0),
                    "cases": int(r.case_count or 0),
                }

        monthly_data = []
        total_sick = 0
        total_dead = 0
        peak_month_name = None
        peak_dead = 0

        for m in range(1, 13):
            info = month_map.get(m, {"sick": 0, "dead": 0, "cases": 0})
            sick = info["sick"]
            dead = info["dead"]
            total_sick += sick
            total_dead += dead
            m_name = month_names[m - 1]

            if dead > peak_dead:
                peak_dead = dead
                peak_month_name = m_name

            monthly_data.append({
                "month_num": m,
                "month": m_name,
                "sick": sick,
                "dead": dead,
                "total": sick + dead,
                "cases": info["cases"]
            })

        total_impacted = total_sick + total_dead
        mortality_rate = round((total_dead / total_impacted * 100), 1) if total_impacted > 0 else 0.0

        return {
            "year": year,
            "months": month_names,
            "monthly_data": monthly_data,
            "total_sick": total_sick,
            "total_dead": total_dead,
            "total_impacted": total_impacted,
            "mortality_rate": mortality_rate,
            "peak_month": peak_month_name if peak_dead > 0 else None,
            "peak_dead": peak_dead,
        }

    # ── Regional Outbreak Hotspots (Cases by Province) ───────────────────
    @classmethod
    def get_cases_by_province(cls, **filters) -> list[dict]:
        """Returns ranked list of provinces with case counts, dominant diseases, and mortality rates."""
        base = cls._base_query(**filters)
        total_cases = base.count()

        rows = (
            base.with_entities(
                Case.province,
                func.count(Case.id).label("cases"),
                func.sum(func.coalesce(Case.sick_bird_count, 0)).label("sick"),
                func.sum(func.coalesce(Case.dead_bird_count, 0)).label("dead"),
            )
            .filter(Case.province.isnot(None))
            .group_by(Case.province)
            .order_by(desc("cases"))
            .all()
        )

        result = []
        for prov_name, count, sick, dead in rows:
            p_obj = get_province_by_key(prov_name) or {}

            # Determine dominant diagnosed disease in this province
            dom_row = (
                cls._base_query(**filters)
                .join(Disease, Case.disease_id == Disease.id)
                .filter(Case.province == prov_name)
                .with_entities(Disease.name, func.count(Case.id).label("d_count"))
                .group_by(Disease.name)
                .order_by(desc("d_count"))
                .first()
            )
            dom_disease = dom_row[0] if dom_row else "—"

            sick_birds = int(sick or 0)
            dead_birds = int(dead or 0)
            impacted = sick_birds + dead_birds
            mortality_rate = round((dead_birds / impacted * 100), 1) if impacted > 0 else 0.0
            percent = round((count / total_cases * 100), 1) if total_cases > 0 else 0.0

            # Compute risk classification
            if mortality_rate >= 35.0 or count >= 10:
                risk_level = "critical"
                risk_label_en = "Critical"
                risk_label_km = "ធ្ងន់ធ្ងរខ្លាំង"
            elif mortality_rate >= 25.0 or count >= 5:
                risk_level = "high"
                risk_label_en = "High"
                risk_label_km = "ខ្ពស់"
            elif mortality_rate >= 15.0 or count >= 2:
                risk_level = "moderate"
                risk_label_en = "Moderate"
                risk_label_km = "មធ្យម"
            else:
                risk_level = "low"
                risk_label_en = "Low"
                risk_label_km = "ទាប"

            result.append({
                "province": prov_name,
                "province_km": p_obj.get("name_km", prov_name),
                "code": p_obj.get("code", prov_name.lower().replace(" ", "_")),
                "cases": count,
                "percent": percent,
                "dominant_disease": dom_disease,
                "sick_birds": sick_birds,
                "dead_birds": dead_birds,
                "impacted_birds": impacted,
                "mortality_rate": mortality_rate,
                "risk_level": risk_level,
                "risk_label_en": risk_label_en,
                "risk_label_km": risk_label_km,
                "lat": p_obj.get("lat"),
                "lng": p_obj.get("lng"),
            })

        return result

    # ── Status breakdown ───────────────────────────────────────────────────
    @classmethod
    def get_status_breakdown(cls, **filters) -> dict:
        # The status card breakdown ignores an incoming status filter so all
        # three buckets remain visible; date/disease filters still apply.
        status_free = dict(filters)
        status_free.pop("status", None)
        rows = (
            cls._base_query(**status_free)
            .with_entities(Case.status, func.count(Case.id))
            .group_by(Case.status)
            .all()
        )
        breakdown = {status: count for status, count in rows}
        # Ensure all three known buckets exist for a stable chart/legend.
        for key in (CASE_STATUS_PENDING, CASE_STATUS_CONFIRMED, CASE_STATUS_REJECTED):
            breakdown.setdefault(key, 0)

        total = sum(breakdown.get(k, 0) for k in (CASE_STATUS_PENDING, CASE_STATUS_CONFIRMED, CASE_STATUS_REJECTED))
        breakdown["total"] = total
        breakdown["pending_pct"] = round((breakdown[CASE_STATUS_PENDING] / total * 100), 1) if total > 0 else 0.0
        breakdown["confirmed_pct"] = round((breakdown[CASE_STATUS_CONFIRMED] / total * 100), 1) if total > 0 else 0.0
        breakdown["rejected_pct"] = round((breakdown[CASE_STATUS_REJECTED] / total * 100), 1) if total > 0 else 0.0

        resolved = breakdown[CASE_STATUS_CONFIRMED] + breakdown[CASE_STATUS_REJECTED]
        breakdown["resolved"] = resolved
        breakdown["confirmation_rate"] = round((breakdown[CASE_STATUS_CONFIRMED] / resolved * 100), 1) if resolved > 0 else 0.0
        breakdown["resolution_rate"] = round((resolved / total * 100), 1) if total > 0 else 0.0

        return breakdown

    # ── Recent cases ───────────────────────────────────────────────────────
    @classmethod
    def get_recent_cases(cls, limit: int = 6, **filters) -> list[Case]:
        return (
            cls._base_query(**filters)
            .order_by(Case.created_at.desc())
            .limit(limit)
            .all()
        )

    # ── High-risk cases ────────────────────────────────────────────────────
    @staticmethod
    def _is_dangerous_severity(severity: str) -> bool:
        if not severity:
            return False
        s = severity.lower()
        return any(tok in severity or tok in s for tok in DANGEROUS_SEVERITY_TOKENS)

    @classmethod
    def get_high_risk_cases(cls, limit: int = 8, **filters) -> list[dict]:
        """Return recent cases flagged as high-risk with their risk reasons.

        A case is high-risk when any of these hold:
          - many sick birds (>= HIGH_RISK_SICK_BIRDS)
          - notable mortality (dead birds >= HIGH_RISK_DEAD_BIRDS)
          - diagnosed disease has a dangerous severity
          - low diagnosis confidence (< LOW_CONFIDENCE_THRESHOLD)
        Rejected cases are excluded (already dismissed by a doctor).
        """
        query = (
            cls._base_query(**filters)
            .filter(Case.status != CASE_STATUS_REJECTED)
            .filter(
                or_(
                    Case.sick_bird_count >= HIGH_RISK_SICK_BIRDS,
                    Case.dead_bird_count >= HIGH_RISK_DEAD_BIRDS,
                    Case.confidence < LOW_CONFIDENCE_THRESHOLD,
                    Case.disease.has(
                        or_(*[Disease.severity.ilike(f"%{tok}%")
                              for tok in DANGEROUS_SEVERITY_TOKENS])
                    ),
                )
            )
            .order_by(Case.created_at.desc())
            .limit(limit)
        )

        results = []
        for case in query.all():
            reasons = cls._risk_reasons(case)
            results.append({"case": case, "reasons": reasons})
        return results

    @classmethod
    def _risk_reasons(cls, case: Case) -> list[dict]:
        """Human-readable Khmer/English risk reasons for a case."""
        reasons = []
        if case.dead_bird_count is not None and case.dead_bird_count >= HIGH_RISK_DEAD_BIRDS:
            reasons.append({
                "color": "dark",
                "icon": "bi-x-octagon",
                "label_km": f"មាន់ស្លាប់ {case.dead_bird_count}",
                "label_en": "Deaths",
            })
        if case.sick_bird_count is not None and case.sick_bird_count >= HIGH_RISK_SICK_BIRDS:
            reasons.append({
                "color": "warning",
                "icon": "bi-thermometer-high",
                "label_km": f"មាន់ឈឺ {case.sick_bird_count}",
                "label_en": "Sick birds",
            })
        disease = case.disease
        if disease is not None and cls._is_dangerous_severity(disease.severity):
            reasons.append({
                "color": "danger",
                "icon": "bi-exclamation-triangle",
                "label_km": "ជំងឺធ្ងន់ធ្ងរ",
                "label_en": "Severe disease",
            })
        if case.confidence is not None and case.confidence < LOW_CONFIDENCE_THRESHOLD:
            reasons.append({
                "color": "secondary",
                "icon": "bi-question-circle",
                "label_km": "ទំនុកចិត្តទាប",
                "label_en": "Low confidence",
            })
        return reasons
