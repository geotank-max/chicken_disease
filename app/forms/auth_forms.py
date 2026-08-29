# app/forms/auth_forms.py
"""Forms for forgot-password and reset-password flows."""
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


def strong_password(form, field):
    """Require: min 8 chars, upper, lower, digit, special."""
    password = field.data or ""
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*()<>?\"{}|<>_\-+=]", password):
        raise ValidationError("Password must contain at least one special character.")


class ForgotPasswordForm(FlaskForm):
    """User submits their email to receive a password-reset link."""
    email = StringField(
        "Email Address",
        validators=[DataRequired(), Email(), Length(max=120)],
        render_kw={"placeholder": "Enter your registered email"},
    )
    submit = SubmitField("Send Reset Link")


class ResetPasswordForm(FlaskForm):
    """User sets a new password after following the reset link."""
    password = PasswordField(
        "New Password",
        validators=[DataRequired(), strong_password],
        render_kw={"placeholder": "Enter new password"},
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
        render_kw={"placeholder": "Confirm new password"},
    )
    submit = SubmitField("Reset Password")
