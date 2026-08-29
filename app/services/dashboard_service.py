from datetime import datetime, timedelta
from sqlalchemy import func, or_
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

        return {
            "total_cases": total_cases,
            "pending_reviews": cls._base_query(**status_free)
                .filter(Case.status == CASE_STATUS_PENDING).count(),
            "confirmed_cases": cls._base_query(**status_free)
                .filter(Case.status == CASE_STATUS_CONFIRMED).count(),
            "rejected_cases": cls._base_query(**status_free)
                .filter(Case.status == CASE_STATUS_REJECTED).count(),
            "cases_this_month": cls._base_query(**status_free)
                .filter(Case.created_at >= month_start).count(),
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
