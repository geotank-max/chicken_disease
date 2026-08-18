from datetime import datetime, timedelta
from sqlalchemy import func
from extensions import db
from app.models.expert_system import Case, Disease, Symptom, Rule, CASE_STATUS_PENDING
from app.models.user import UserTable


class DashboardService:
    @staticmethod
    def get_summary() -> dict:
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        return {
            "total_cases": Case.query.count(),
            "cases_this_week": Case.query.filter(Case.created_at >= week_ago).count(),
            "pending_reviews": Case.query.filter_by(status=CASE_STATUS_PENDING).count(),
            "total_diseases": Disease.query.count(),
            "total_symptoms": Symptom.query.count(),
            "total_rules": Rule.query.count(),
            "total_users": UserTable.query.count(),
        }

    @staticmethod
    def get_top_diseases(limit: int = 5) -> list[dict]:
        rows = (
            db.session.query(Disease.name, func.count(Case.id).label("count"))
            .join(Case, Case.disease_id == Disease.id)
            .group_by(Disease.id, Disease.name)
            .order_by(func.count(Case.id).desc())
            .limit(limit)
            .all()
        )
        return [{"name": name, "count": count} for name, count in rows]

    @staticmethod
    def get_cases_by_day(days: int = 7) -> list[dict]:
        start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=days - 1)
        rows = (
            db.session.query(func.date(Case.created_at).label("day"), func.count(Case.id))
            .filter(Case.created_at >= start)
            .group_by(func.date(Case.created_at))
            .order_by(func.date(Case.created_at))
            .all()
        )
        day_map = {str(day): count for day, count in rows}
        result = []
        for i in range(days):
            d = (start + timedelta(days=i)).date()
            result.append({"date": d.strftime("%m/%d"), "count": day_map.get(str(d), 0)})
        return result

    @staticmethod
    def get_recent_cases(limit: int = 5) -> list[Case]:
        return Case.query.order_by(Case.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_status_breakdown() -> dict:
        rows = (
            db.session.query(Case.status, func.count(Case.id))
            .group_by(Case.status)
            .all()
        )
        return {status: count for status, count in rows}
