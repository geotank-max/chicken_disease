# app/services/notification_service.py
from datetime import datetime
from extensions import db
from app.models.notification import Notification
from app.models.expert_system import Case, CASE_STATUS_PENDING
from app.models.doctor_application import DoctorApplication, APPLICATION_PENDING


class NotificationService:
    """Service for creating notifications and computing badge counts."""

    # ── Create notifications ────────────────────────────────────────────

    @staticmethod
    def notify_user(user_id, title, message="", category="system", link=None):
        """Send a notification to a specific user."""
        n = Notification(
            user_id=user_id,
            title=title,
            message=message,
            category=category,
            link=link,
        )
        db.session.add(n)
        db.session.commit()
        return n

    @staticmethod
    def notify_all_users(title, message="", category="system", link=None):
        """Send a notification to all regular users."""
        from app.models.user import UserTable
        from app.models.role import RoleTable
        user_role = db.session.scalar(db.select(RoleTable).filter_by(name="User"))
        if not user_role:
            return
        users = UserTable.query.filter(UserTable.roles.any(id=user_role.id)).all()
        for user in users:
            n = Notification(
                user_id=user.id,
                title=title,
                message=message,
                category=category,
                link=link,
            )
            db.session.add(n)
        db.session.commit()

    # ── Badge counts ────────────────────────────────────────────────────

    @staticmethod
    def get_unread_count(user_id):
        """Total unread notifications for a user."""
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    @staticmethod
    def get_pending_cases_count():
        """Number of cases waiting for doctor/admin review."""
        return Case.query.filter_by(status=CASE_STATUS_PENDING).count()

    @staticmethod
    def get_pending_applications_count():
        """Number of doctor applications waiting for admin review."""
        return DoctorApplication.query.filter_by(status=APPLICATION_PENDING).count()

    # ── Read / manage ───────────────────────────────────────────────────

    @staticmethod
    def get_user_notifications(user_id, limit=20):
        """Get recent notifications for a user."""
        return (
            Notification.query
            .filter_by(user_id=user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark a single notification as read."""
        n = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if n:
            n.is_read = True
            db.session.commit()

    @staticmethod
    def mark_all_read(user_id):
        """Mark all notifications as read for a user."""
        Notification.query.filter_by(user_id=user_id, is_read=False).update(
            {"is_read": True}
        )
        db.session.commit()
