# app/models/expert_system.py
import json
import re
from datetime import datetime
from extensions import db
from app.models.associations import tbl_cases_symptoms, tbl_rules_symptoms

CASE_STATUS_PENDING = "pending"
CASE_STATUS_CONFIRMED = "confirmed"
CASE_STATUS_REJECTED = "rejected"

# Follow-up outcome tracked after a case has been reviewed.
FOLLOWUP_NONE = "none"
FOLLOWUP_IMPROVING = "improving"
FOLLOWUP_NOT_IMPROVED = "not_improved"
FOLLOWUP_RECOVERED = "recovered"
FOLLOWUP_DEAD = "dead"
FOLLOWUP_NEEDS_REVISIT = "needs_revisit"

FOLLOWUP_STATUSES = [
    FOLLOWUP_NONE,
    FOLLOWUP_IMPROVING,
    FOLLOWUP_NOT_IMPROVED,
    FOLLOWUP_RECOVERED,
    FOLLOWUP_DEAD,
    FOLLOWUP_NEEDS_REVISIT,
]

# ── Extended diagnosis context: option values + Khmer labels ────────────────
# Each list drives the <select> options in the diagnosis form (value order)
# and the label maps render the Khmer text on the form and case views.

YES_NO_LABELS = {
    "yes": "បាទ/ចាស",
    "no": "ទេ",
    "unknown": "មិនដឹង",
}
YES_NO_OPTIONS = ["yes", "no", "unknown"]

VACCINATION_LABELS = {
    "unknown": "មិនដឹង",
    "none": "មិនបានចាក់",
    "partial": "ចាក់មិនគ្រប់",
    "full": "ចាក់គ្រប់",
}
VACCINATION_OPTIONS = ["unknown", "none", "partial", "full"]

COOP_CONDITION_LABELS = {
    "clean": "ស្អាត",
    "damp": "សើម",
    "dirty": "កខ្វក់",
    "crowded": "ណែនណាន់",
}
COOP_CONDITION_OPTIONS = ["clean", "damp", "dirty", "crowded"]

INTAKE_LEVEL_LABELS = {
    "normal": "ធម្មតា",
    "reduced": "ថយចុះ",
    "none": "ឈប់ស៊ី/ផឹក",
    "increased": "កើនឡើង",
}
INTAKE_LEVEL_OPTIONS = ["normal", "reduced", "none", "increased"]


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
    treatment_steps = db.relationship(
        "TreatmentStep",
        back_populates="disease",
        cascade="all, delete-orphan",
        order_by="TreatmentStep.position",
    )

    @property
    def has_structured_steps(self) -> bool:
        return len(self.treatment_steps) > 0

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
    # ── Extended diagnosis context (all optional) ──────────────────────────
    sick_bird_count = db.Column(db.Integer)
    dead_bird_count = db.Column(db.Integer)
    symptom_duration = db.Column(db.String(80))       # free text, e.g. "៣ ថ្ងៃ"
    vaccination_status = db.Column(db.String(20))     # unknown/none/partial/full
    egg_production_drop = db.Column(db.Integer)       # percent drop, 0-100
    feed_or_water_changed = db.Column(db.String(10))  # yes/no/unknown
    new_birds_added = db.Column(db.String(10))        # yes/no/unknown
    nearby_farms_sick = db.Column(db.String(10))      # yes/no/unknown
    coop_condition = db.Column(db.String(20))         # clean/damp/dirty/crowded
    appetite_level = db.Column(db.String(20))         # normal/reduced/none/increased
    water_intake_level = db.Column(db.String(20))     # normal/reduced/none/increased
    follow_up_status = db.Column(db.String(30), default=FOLLOWUP_NONE, nullable=False)
    follow_up_updated_at = db.Column(db.DateTime)
    # JSON list of completed treatment step indexes for this case, e.g. "[0, 2]".
    treatment_checked_steps = db.Column(db.Text)
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
    messages = db.relationship("CaseMessage", back_populates="case", cascade="all, delete-orphan", order_by="CaseMessage.created_at")
    treatment_progress_rows = db.relationship("CaseTreatmentProgress", back_populates="case", cascade="all, delete-orphan")

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

    @property
    def follow_up_label_km(self) -> str:
        labels = {
            FOLLOWUP_NONE: "មិនទាន់មាន",
            FOLLOWUP_IMPROVING: "កំពុងធូរស្រាល",
            FOLLOWUP_NOT_IMPROVED: "មិនធូរស្រាល",
            FOLLOWUP_RECOVERED: "ជាសះស្បើយ",
            FOLLOWUP_DEAD: "ស្លាប់",
            FOLLOWUP_NEEDS_REVISIT: "ត្រូវពិនិត្យឡើងវិញ",
        }
        return labels.get(self.follow_up_status, self.follow_up_status)

    @property
    def follow_up_color(self) -> str:
        colors = {
            FOLLOWUP_NONE: "secondary",
            FOLLOWUP_IMPROVING: "info",
            FOLLOWUP_NOT_IMPROVED: "warning",
            FOLLOWUP_RECOVERED: "success",
            FOLLOWUP_DEAD: "dark",
            FOLLOWUP_NEEDS_REVISIT: "danger",
        }
        return colors.get(self.follow_up_status, "secondary")

    # ── Extended diagnosis context labels (Khmer) ──────────────────────────

    @property
    def vaccination_status_label_km(self) -> str:
        return VACCINATION_LABELS.get(self.vaccination_status, "")

    @property
    def feed_or_water_changed_label_km(self) -> str:
        return YES_NO_LABELS.get(self.feed_or_water_changed, "")

    @property
    def new_birds_added_label_km(self) -> str:
        return YES_NO_LABELS.get(self.new_birds_added, "")

    @property
    def nearby_farms_sick_label_km(self) -> str:
        return YES_NO_LABELS.get(self.nearby_farms_sick, "")

    @property
    def coop_condition_label_km(self) -> str:
        return COOP_CONDITION_LABELS.get(self.coop_condition, "")

    @property
    def appetite_level_label_km(self) -> str:
        return INTAKE_LEVEL_LABELS.get(self.appetite_level, "")

    @property
    def water_intake_level_label_km(self) -> str:
        return INTAKE_LEVEL_LABELS.get(self.water_intake_level, "")

    @property
    def has_extended_context(self) -> bool:
        """True if any extended diagnosis context field was filled."""
        return any([
            self.sick_bird_count is not None,
            self.dead_bird_count is not None,
            self.symptom_duration,
            self.vaccination_status,
            self.egg_production_drop is not None,
            self.feed_or_water_changed,
            self.new_birds_added,
            self.nearby_farms_sick,
            self.coop_condition,
            self.appetite_level,
            self.water_intake_level,
        ])

    # ── Treatment checklist (Option B: derived from disease treatment text) ──

    @staticmethod
    def split_treatment_text(text: str) -> list[str]:
        """Split a free-text treatment into individual actionable steps.

        Splits on the Khmer sentence terminator (។), Latin periods, newlines,
        and semicolons, then trims and drops empties. Used to turn the shared
        disease treatment text into a per-case checklist.
        """
        if not text:
            return []
        # Normalize newlines to a delimiter, then split on ។ . ; and bullets.
        parts = re.split(r"[។.;\n•]+", text)
        steps = [p.strip(" \t-–—") for p in parts]
        return [s for s in steps if s]

    @property
    def _checked_step_set(self) -> set:
        """Completed indexes for the fallback (derived-text) checklist."""
        if not self.treatment_checked_steps:
            return set()
        try:
            data = json.loads(self.treatment_checked_steps)
            return {int(i) for i in data}
        except (ValueError, TypeError):
            return set()

    @property
    def uses_structured_steps(self) -> bool:
        """True when the diagnosed disease has doctor-authored steps (Option A)."""
        disease = self.final_disease
        return bool(disease and disease.has_structured_steps)

    @property
    def treatment_steps(self) -> list:
        """Checklist steps for this case.

        Prefers structured, doctor-authored TreatmentStep rows (keyed by step
        id). Falls back to splitting the disease's free-text treatment when no
        structured steps exist (keyed by positional index).

        Each item: {mode, key, text, note, done}.
          - mode "structured": key is the TreatmentStep.id
          - mode "text":       key is the positional index
        """
        disease = self.final_disease
        if disease is None:
            return []

        if disease.has_structured_steps:
            done_ids = {p.step_id for p in self.treatment_progress_rows if p.done}
            return [
                {
                    "mode": "structured",
                    "key": step.id,
                    "text": step.text,
                    "note": step.note,
                    "done": step.id in done_ids,
                }
                for step in disease.treatment_steps
            ]

        # Fallback: Option B derived checklist.
        checked = self._checked_step_set
        return [
            {"mode": "text", "key": i, "text": text, "note": None, "done": i in checked}
            for i, text in enumerate(self.split_treatment_text(disease.treatment))
        ]

    @property
    def treatment_progress(self) -> dict:
        """Summary counts for a progress bar: total, done, percent."""
        steps = self.treatment_steps
        total = len(steps)
        done = sum(1 for s in steps if s["done"])
        percent = round(done / total * 100) if total else 0
        return {"total": total, "done": done, "percent": percent}

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


class CaseMessage(db.Model):
    """A comment/question on a case, enabling doctor <-> farmer follow-up per case."""

    __tablename__ = "tbl_case_messages"

    id = db.Column(db.Integer, db.Sequence("seq_case_messages_id"), primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("tbl_cases.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"), nullable=False)
    body = db.Column(db.Text, nullable=False)
    # Snapshot of whether the author posted while acting as a reviewing doctor,
    # so the thread renders correctly even if roles change later.
    is_doctor = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    case = db.relationship("Case", back_populates="messages")
    author = db.relationship("UserTable", foreign_keys=[author_id])

    def __repr__(self) -> str:
        return f"<CaseMessage {self.id} case={self.case_id} author={self.author_id}>"


class TreatmentStep(db.Model):
    """A doctor/admin-authored, ordered treatment step for a disease (Option A)."""

    __tablename__ = "tbl_treatment_steps"

    id = db.Column(db.Integer, db.Sequence("seq_treatment_steps_id"), primary_key=True)
    disease_id = db.Column(db.Integer, db.ForeignKey("tbl_diseases.id"), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    text = db.Column(db.String(500), nullable=False)
    note = db.Column(db.String(500))  # optional extra detail / dosage
    created_by_id = db.Column(db.Integer, db.ForeignKey("tbl_users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    disease = db.relationship("Disease", back_populates="treatment_steps")
    created_by = db.relationship("UserTable", foreign_keys=[created_by_id])

    def __repr__(self) -> str:
        return f"<TreatmentStep {self.id} disease={self.disease_id} pos={self.position}>"


class CaseTreatmentProgress(db.Model):
    """Per-case completion state of a structured treatment step."""

    __tablename__ = "tbl_case_treatment_progress"

    id = db.Column(db.Integer, db.Sequence("seq_case_treatment_progress_id"), primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey("tbl_cases.id"), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey("tbl_treatment_steps.id", ondelete="CASCADE"), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(db.DateTime)

    case = db.relationship("Case", back_populates="treatment_progress_rows")
    step = db.relationship("TreatmentStep")

    __table_args__ = (
        db.UniqueConstraint("case_id", "step_id", name="uq_case_step"),
    )

    def __repr__(self) -> str:
        return f"<CaseTreatmentProgress case={self.case_id} step={self.step_id} done={self.done}>"
