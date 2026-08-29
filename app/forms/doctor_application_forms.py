# app/forms/doctor_application_forms.py
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional


class DoctorApplicationForm(FlaskForm):
    """Form for users to apply for Doctor role."""

    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=3, max=150)],
        render_kw={"placeholder": "Your full legal name"},
    )
    phone = StringField(
        "Phone Number",
        validators=[Optional(), Length(max=30)],
        render_kw={"placeholder": "e.g. 012 345 678"},
    )
    address = TextAreaField(
        "Address",
        validators=[Optional(), Length(max=500)],
        render_kw={"placeholder": "Your current address", "rows": 2},
    )
    motivation = TextAreaField(
        "Motivation / Experience",
        validators=[Optional(), Length(max=1000)],
        render_kw={"placeholder": "Briefly describe your veterinary experience or why you want to become a doctor on this platform.", "rows": 3},
    )

    # PDF uploads
    pdf_dv_certificate = FileField(
        "DV Certificate (PDF)",
        validators=[FileRequired(), FileAllowed(["pdf"], "PDF files only.")],
    )
    pdf_id_card = FileField(
        "ID Card (PDF)",
        validators=[FileRequired(), FileAllowed(["pdf"], "PDF files only.")],
    )
    pdf_birth_certificate = FileField(
        "Birth Certificate (PDF)",
        validators=[FileRequired(), FileAllowed(["pdf"], "PDF files only.")],
    )
    pdf_diploma = FileField(
        "Diploma / Degree (PDF, optional)",
        validators=[Optional(), FileAllowed(["pdf"], "PDF files only.")],
    )

    submit = SubmitField("Submit Application")


class ApplicationReviewForm(FlaskForm):
    """Form for admin to approve/reject an application."""

    action = SelectField(
        "Decision",
        choices=[("approve", "Approve"), ("reject", "Reject")],
        validators=[DataRequired()],
    )
    review_notes = TextAreaField(
        "Notes",
        validators=[Optional(), Length(max=500)],
        render_kw={"placeholder": "Reason for decision (optional)", "rows": 3},
    )
    submit = SubmitField("Submit Decision")
