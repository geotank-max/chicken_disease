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

    @staticmethod
    def notify_doctors_new_case(case):
        """Create a bell notification for every Doctor/Admin when a new case is submitted.

        Finds all active users whose roles carry the 'review_cases' permission,
        skipping the submitter themselves.
        """
        from app.models.user import UserTable
        from app.models.permission import PermissionTable
        from app.models.role import RoleTable

        # Find all roles that have review_cases permission
        reviewable_roles = (
            RoleTable.query
            .filter(RoleTable.permissions.any(PermissionTable.code == "review_cases"))
            .all()
        )
        if not reviewable_roles:
            return

        role_ids = [r.id for r in reviewable_roles]

        # Find all active users holding any of those roles, except the submitter
        reviewers = (
            UserTable.query
            .filter(UserTable.is_active == True)
            .filter(UserTable.roles.any(RoleTable.id.in_(role_ids)))
            .filter(UserTable.id != case.user_id)
            .all()
        )

        disease_name = case.disease.name if case.disease else "មិនស្គាល់"
        submitter = case.user.full_name if case.user else "អ្នកប្រើ"
        from flask import url_for
        link = url_for("expert_system.cases_detail", case_id=case.id)

        for reviewer in reviewers:
            n = Notification(
                user_id=reviewer.id,
                title=f"ករណីថ្មី #{case.id} រង់ចាំពិនិត្យ",
                message=f"{submitter} បានដាក់ស្នើករណីជំងឺ \"{disease_name}\"។ សូមពិនិត្យ។",
                category="case",
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
