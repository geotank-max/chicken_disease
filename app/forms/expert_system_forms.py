# app/forms/expert_system_forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField, TextAreaField, SubmitField, IntegerField,
    FloatField, SelectField, BooleanField, MultipleFileField,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional
from app.forms.multi_checkbox_field import MultiCheckboxField
from app.models.expert_system import Category, Disease, Symptom, Rule
from extensions import db

# Allowed image extensions for case photos
ALLOWED_PHOTO_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "gif"]


def _category_choices():
    items = db.session.scalars(
        db.select(Category).order_by(Category.name)
    ).all()
    return [(0, "--- None ---")] + [(c.id, c.name) for c in items]


def _disease_choices():
    items = db.session.scalars(
        db.select(Disease).order_by(Disease.name)
    ).all()
    return [(d.id, d.name) for d in items]


def _symptom_choices():
    items = db.session.scalars(
        db.select(Symptom).order_by(Symptom.name)
    ).all()
    return [(s.id, s.name) for s in items]


class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Description")
    submit = SubmitField("Save")


class SymptomForm(FlaskForm):
    name = StringField("Symptom Name", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Description")
    category_id = SelectField("Category", coerce=int)
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id.choices = _category_choices()


class DiseaseForm(FlaskForm):
    name = StringField("Disease Name", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=5, max=500)])
    treatment = TextAreaField("Treatment", validators=[DataRequired(), Length(min=5, max=500)])
    prevention = TextAreaField("Prevention", validators=[Optional(), Length(max=500)])
    severity = SelectField(
        "Severity",
        choices=[("", "---"), ("Low", "Low"), ("Medium", "Medium"), ("High", "High")],
        validators=[Optional()],
    )
    is_contagious = BooleanField("Contagious")
    category_id = SelectField("Category", coerce=int)
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id.choices = _category_choices()


class RuleForm(FlaskForm):
    title = StringField("Rule Title", validators=[DataRequired(), Length(min=2, max=120)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=5, max=255)])
    priority = IntegerField("Priority", validators=[DataRequired(), NumberRange(min=1, max=100)])
    confidence = FloatField("Confidence (%)", validators=[DataRequired(), NumberRange(min=1, max=100)])
    disease_id = SelectField("Disease", coerce=int, validators=[DataRequired()])
    symptom_ids = MultiCheckboxField("Symptoms", coerce=int)
    submit = SubmitField("Save")

    def __init__(self, original_rule: Rule | None = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.disease_id.choices = _disease_choices()
        self.symptom_ids.choices = _symptom_choices()
        if original_rule and not self.is_submitted():
            self.symptom_ids.data = [s.id for s in original_rule.symptoms]


class FlockInfoForm(FlaskForm):
    flock_size = IntegerField("Flock Size", validators=[Optional(), NumberRange(min=1, max=100000)])
    bird_age = StringField("Bird Age", validators=[Optional(), Length(max=80)])
    breed = StringField("Breed", validators=[Optional(), Length(max=80)])
    location = StringField("Location", validators=[Optional(), Length(max=120)])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])

    # Symptom photos — one multi-file field per visual category (all optional)
    photos_droppings  = MultipleFileField("លាមក",                   validators=[Optional(), FileAllowed(ALLOWED_PHOTO_EXTENSIONS, "Images only.")])
    photos_eyes       = MultipleFileField("ភ្នែក",                   validators=[Optional(), FileAllowed(ALLOWED_PHOTO_EXTENSIONS, "Images only.")])
    photos_comb       = MultipleFileField("មកុដ",                   validators=[Optional(), FileAllowed(ALLOWED_PHOTO_EXTENSIONS, "Images only.")])
    photos_skin       = MultipleFileField("ស្បែក / របួស",            validators=[Optional(), FileAllowed(ALLOWED_PHOTO_EXTENSIONS, "Images only.")])
    photos_dead_birds = MultipleFileField("មាន់ស្លាប់",               validators=[Optional(), FileAllowed(ALLOWED_PHOTO_EXTENSIONS, "Images only.")])
    photos_coop       = MultipleFileField("ទ្រុង / ស្ថានទីចិញ្ចឹម",    validators=[Optional(), FileAllowed(ALLOWED_PHOTO_EXTENSIONS, "Images only.")])
    photos_other      = MultipleFileField("រូបភាពផ្សេងៗ",             validators=[Optional(), FileAllowed(ALLOWED_PHOTO_EXTENSIONS, "Images only.")])

    submit = SubmitField("Continue")


class CaseReviewForm(FlaskForm):
    action = SelectField(
        "Action",
        choices=[("confirm", "Confirm"), ("reject", "Reject")],
        validators=[DataRequired()],
    )
    override_disease_id = SelectField("Override Disease (optional)", coerce=int, validators=[Optional()])
    doctor_notes = TextAreaField("Doctor Notes", validators=[Optional(), Length(max=1000)])
    submit = SubmitField("Submit Review")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.override_disease_id.choices = [(0, "--- Use system result ---")] + _disease_choices()
