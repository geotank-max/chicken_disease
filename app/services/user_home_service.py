# app/services/user_home_service.py
"""Service layer for the User Home page — queries only the current user's cases."""
from datetime import datetime, timedelta
from extensions import db
from app.models.expert_system import (
    Case,
    CASE_STATUS_PENDING,
    CASE_STATUS_CONFIRMED,
    CASE_STATUS_REJECTED,
)


class UserHomeService:
    @staticmethod
    def get_my_stats(user_id: int) -> dict:
        """Return stat counts scoped to a single user."""
        now = datetime.utcnow()
        week_ago = now - timedelta(days=7)

        base = Case.query.filter_by(user_id=user_id)

        return {
            "total": base.count(),
            "pending": base.filter_by(status=CASE_STATUS_PENDING).count(),
            "confirmed": base.filter_by(status=CASE_STATUS_CONFIRMED).count(),
            "this_week": base.filter(Case.created_at >= week_ago).count(),
        }

    @staticmethod
    def get_recent_cases(user_id: int, limit: int = 3) -> list[Case]:
        """Return the user's most recent cases."""
        return (
            Case.query
            .filter_by(user_id=user_id)
            .order_by(Case.created_at.desc())
            .limit(limit)
            .all()
        )
