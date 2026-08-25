# app/models/expert_system.py
from datetime import datetime
from extensions import db
from app.models.associations import tbl_cases_symptoms, tbl_rules_symptoms

CASE_STATUS_PENDING = "pending"
CASE_STATUS_CONFIRMED = "confirmed"
CASE_STATUS_REJECTED = "rejected"


class Category(db.Model):
    __tablename__ = "tbl_categories"

    id = db.Column(db.Integer, db.Sequence('seq_categories_id'), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    diseases = db.relationship("Disease", back_populates="category")
    symptoms = db.relationship("Symptom", back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name}>"


class Symptom(db.Model):
    __tablename__ = "tbl_symptoms"

    id = db.Column(db.Integer, db.Sequence('seq_symptoms_id'), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey("tbl_categories.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    category = db.relationship("Category", back_populates="symptoms")
    cases = db.relationship(
        "Case",
        secondary=tbl_cases_symptoms,
        back_populates="symptoms",
    )
    rules = db.relationship(
        "Rule",
        secondary=tbl_rules_symptoms,
        back_populates="symptoms",
    )

    def __repr__(self) -> str:
        return f"<Symptom {self.name}>"


class Disease(db.Model):
    __tablename__ = "tbl_diseases"

    id = db.Column(db.Integer, db.Sequence('seq_diseases_id'), primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    treatment = db.Column(db.String(255), nullable=False)
    prevention = db.Column(db.String(500))
    severity = db.Column(db.String(50))
    is_contagious = db.Column(db.Boolean, default=False, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("tbl_categories.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    category = db.relationship("Category", back_populates="diseases")
    rules = db.relationship("Rule", back_populates="disease", cascade="all, delete-orphan")
    cases = db.relationship("Case", back_populates="disease", foreign_keys="Case.disease_id")

    def __repr__(self) -> str:
        return f"<Disease {self.name}>"


class Rule(db.Model):
    __tablename__ = "tbl_rules"

    id = db.Column(db.Integer, db.Sequence('seq_rules_id'), primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, nullable=False, default=1)
    confidence = db.Column(db.Float, nullable=False, default=80.0)
    disease_id = db.Column(db.Integer, db.ForeignKey("tbl_diseases.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    disease = db.relationship("Disease", back_populates="rules")
    symptoms = db.relationship(
        "Symptom",
        secondary=tbl_rules_symptoms,
        back_populates="rules",
    )

    def __repr__(self) -> str:
        return f"<Rule {self.title}>"


class Case(db.Model):
    __tablename__ = "tbl_cases"

    id = db.Column(db.Integer, db.Sequence('seq_cases_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"))
    disease_id = db.Column(db.Integer, db.ForeignKey("tbl_diseases.id"))
    confidence = db.Column(db.Float)
    flock_size = db.Column(db.Integer)
    bird_age = db.Column(db.String(80))
    breed = db.Column(db.String(80))
    location = db.Column(db.String(120))
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default=CASE_STATUS_PENDING, nullable=False)
    reviewed_by_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"))
    reviewed_at = db.Column(db.DateTime)
    doctor_notes = db.Column(db.Text)
    override_disease_id = db.Column(db.Integer, db.ForeignKey("tbl_diseases.id"))
    feedback_rating = db.Column(db.Integer)  # 1-5 stars
    feedback_text = db.Column(db.Text)
    feedback_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    symptoms = db.relationship(
        "Symptom",
        secondary=tbl_cases_symptoms,
        back_populates="cases",
    )
    disease = db.relationship("Disease", back_populates="cases", foreign_keys=[disease_id])
    override_disease = db.relationship("Disease", foreign_keys=[override_disease_id])
    user = db.relationship("UserTable", foreign_keys=[user_id])
    reviewed_by = db.relationship("UserTable", foreign_keys=[reviewed_by_id])
    photos = db.relationship("CasePhoto", back_populates="case", cascade="all, delete-orphan", order_by="CasePhoto.uploaded_at")

    @property
    def final_disease(self):
        if self.status == CASE_STATUS_CONFIRMED and self.override_disease:
            return self.override_disease
        return self.disease

    @property
    def status_label_km(self) -> str:
        labels = {
            CASE_STATUS_PENDING: "រង់ចាំពិនិត្យ",
            CASE_STATUS_CONFIRMED: "បានបញ្ជាក់",
            CASE_STATUS_REJECTED: "បានបដិសេធ",
        }
        return labels.get(self.status, self.status)

    def __repr__(self) -> str:
        return f"<Case {self.id}>"


# Photo category labels (Khmer)
PHOTO_CATEGORY_LABELS = {
    "droppings":  "លាមក",
    "eyes":       "ភ្នែក",
    "comb":       "មកុដ",
    "skin":       "ស្បែក / របួស",
    "dead_birds": "មាន់ស្លាប់",
    "coop":       "ទ្រុង / ស្ថានទីចិញ្ចឹម",
    "other":      "ផ្សេងៗ",
}

PHOTO_CATEGORIES = list(PHOTO_CATEGORY_LABELS.keys())


class CasePhoto(db.Model):
    """Stores symptom photos uploaded by farmers when submitting a diagnosis case."""

    __tablename__ = "tbl_case_photos"

    id = db.Column(db.Integer, db.Sequence("seq_case_photos_id"), primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("tbl_cases.id"), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)       # relative path under uploads/
    original_filename = db.Column(db.String(255))               # original name for display
    category = db.Column(db.String(50), default="other")        # droppings, eyes, comb, etc.
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    case = db.relationship("Case", back_populates="photos")

    @property
    def category_label_km(self) -> str:
        return PHOTO_CATEGORY_LABELS.get(self.category, self.category)

    def __repr__(self) -> str:
        return f"<CasePhoto {self.id} case={self.case_id} cat={self.category}>"
