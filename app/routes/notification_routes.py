# app/routes/notification_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.services.notification_service import NotificationService

notification_bp = Blueprint("notifications", __name__, url_prefix="/notifications")


@notification_bp.route("/")
@login_required
def index():
    notifications = NotificationService.get_user_notifications(current_user.id, limit=50)
    return render_template("notifications/index.html", notifications=notifications)


@notification_bp.route("/mark-all-read", methods=["POST"])
@login_required
def mark_all_read():
    NotificationService.mark_all_read(current_user.id)
    flash("All notifications marked as read.", "success")
    return redirect(url_for("notifications.index"))


@notification_bp.route("/<int:notif_id>/read")
@login_required
def mark_read(notif_id):
    from app.models.notification import Notification
    n = Notification.query.filter_by(id=notif_id, user_id=current_user.id).first()
    if n:
        NotificationService.mark_as_read(notif_id, current_user.id)
        if n.link:
            return redirect(n.link)
    return redirect(url_for("notifications.index"))
