# app/models/notification.py
from datetime import datetime
from extensions import db


class Notification(db.Model):
    __tablename__ = "tbl_notifications"

    id = db.Column(db.Integer, db.Sequence('seq_notifications_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.String(500))
    category = db.Column(db.String(30), nullable=False)  # disease, application, case, system
    link = db.Column(db.String(255))  # URL to navigate to
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("UserTable", backref="notifications")

    def __repr__(self):
        return f"<Notification {self.id} user={self.user_id} read={self.is_read}>"
