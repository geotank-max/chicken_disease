# app/services/email_service.py
"""Reusable SMTP email service for transactional emails."""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app, url_for, render_template

logger = logging.getLogger(__name__)


class EmailService:
    """Thin wrapper around smtplib for sending transactional emails."""

    @staticmethod
    def _get_smtp_config() -> dict:
        """Pull SMTP settings from app config (sourced from .env)."""
        return {
            "host": current_app.config["MAIL_SERVER"],
            "port": current_app.config["MAIL_PORT"],
            "username": current_app.config["MAIL_USERNAME"],
            "password": current_app.config["MAIL_PASSWORD"],
            "use_tls": current_app.config["MAIL_USE_TLS"],
            "sender": current_app.config["MAIL_DEFAULT_SENDER"],
        }

    @staticmethod
    def _send(to: str, subject: str, html_body: str, text_body: str | None = None) -> bool:
        """Send a single email. Returns True on success, False on failure."""
        cfg = EmailService._get_smtp_config()

        msg = MIMEMultipart("alternative")
        msg["From"] = cfg["sender"]
        msg["To"] = to
        msg["Subject"] = subject

        if text_body:
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        try:
            if cfg["use_tls"]:
                server = smtplib.SMTP(cfg["host"], cfg["port"])
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(cfg["host"], cfg["port"])

            server.login(cfg["username"], cfg["password"])
            server.sendmail(cfg["sender"], to, msg.as_string())
            server.quit()
            return True
        except Exception as e:
            logger.error(f"Failed to send email to {to}: {e}")
            return False

    # ── Public convenience methods ────────────────────────────────

    @staticmethod
    def send_verification_email(user, raw_token: str) -> bool:
        """Send email verification link to the user."""
        verify_url = url_for("auth.verify_email", token=raw_token, email=user.email, _external=True)

        html_body = render_template(
            "emails/verify_email.html",
            user=user,
            verify_url=verify_url,
        )
        text_body = (
            f"Hi {user.full_name},\n\n"
            f"Please verify your email by visiting:\n{verify_url}\n\n"
            f"This link expires in 24 hours.\n\n"
            f"If you did not create an account, ignore this email."
        )

        return EmailService._send(
            to=user.email,
            subject="Verify Your Email - IDNS",
            html_body=html_body,
            text_body=text_body,
        )

    @staticmethod
    def send_password_reset_email(user, raw_token: str) -> bool:
        """Send password reset link to the user."""
        reset_url = url_for("auth.reset_password", token=raw_token, email=user.email, _external=True)

        html_body = render_template(
            "emails/reset_password.html",
            user=user,
            reset_url=reset_url,
        )
        text_body = (
            f"Hi {user.full_name},\n\n"
            f"You requested a password reset. Visit this link:\n{reset_url}\n\n"
            f"This link expires in 30 minutes.\n\n"
            f"If you did not request this, ignore this email."
        )

        return EmailService._send(
            to=user.email,
            subject="Reset Your Password - IDNS",
            html_body=html_body,
            text_body=text_body,
        )
