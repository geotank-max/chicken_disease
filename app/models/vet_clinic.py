# app/models/vet_clinic.py
from datetime import datetime
from extensions import db


class VetClinic(db.Model):
    """Veterinary clinic / doctor directory for farmer escalation."""
    __tablename__ = "tbl_vet_clinics"

    id = db.Column(db.Integer, db.Sequence('seq_vet_clinics_id'), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30))
    address = db.Column(db.Text)
    province = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    specialization = db.Column(db.String(200))  # e.g. "poultry", "general livestock"
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Optional link to a registered doctor user
    user_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"), nullable=True)
    user = db.relationship("UserTable", foreign_keys=[user_id])

    def __repr__(self):
        return f"<VetClinic {self.name} ({self.province})>"
