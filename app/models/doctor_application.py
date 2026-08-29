# app/models/doctor_application.py
from datetime import datetime
from extensions import db

APPLICATION_PENDING = "pending"
APPLICATION_APPROVED = "approved"
APPLICATION_REJECTED = "rejected"


class DoctorApplication(db.Model):
    __tablename__ = "tbl_doctor_applications"

    id = db.Column(db.Integer, db.Sequence('seq_doctor_applications_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"), nullable=False)

    # Applicant info
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30))
    address = db.Column(db.Text)
    motivation = db.Column(db.Text)

    # PDF document paths
    pdf_dv_certificate = db.Column(db.String(255), nullable=False)
    pdf_id_card = db.Column(db.String(255), nullable=False)
    pdf_birth_certificate = db.Column(db.String(255), nullable=False)
    pdf_diploma = db.Column(db.String(255))

    # Status
    status = db.Column(db.String(20), default=APPLICATION_PENDING, nullable=False)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"))
    reviewed_at = db.Column(db.DateTime)
    review_notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship("UserTable", foreign_keys=[user_id], backref="doctor_applications")
    reviewed_by = db.relationship("UserTable", foreign_keys=[reviewed_by_id])

    @property
    def status_label(self):
        labels = {
            APPLICATION_PENDING: "Pending Review",
            APPLICATION_APPROVED: "Approved",
            APPLICATION_REJECTED: "Rejected",
        }
        return labels.get(self.status, self.status)

    @property
    def status_color(self):
        colors = {
            APPLICATION_PENDING: "warning",
            APPLICATION_APPROVED: "success",
            APPLICATION_REJECTED: "danger",
        }
        return colors.get(self.status, "secondary")

    def __repr__(self):
        return f"<DoctorApplication {self.id} user={self.user_id} status={self.status}>"
