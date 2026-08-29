# app/routes/oauth_routes.py
"""OAuth routes for Google social login."""

from flask import Blueprint, redirect, url_for, flash, current_app, session
from flask_login import login_user
from app.models.user import UserTable
from app.models.role import RoleTable
from app.services.oauth_service import oauth
from app.services.audit_service import AuditService
from extensions import db, csrf

oauth_bp = Blueprint("oauth", __name__, url_prefix="/auth/google")


@oauth_bp.route("/login")
def google_login():
    """Redirect user to Google's OAuth 2.0 consent screen.

    We always start the OAuth flow when the user clicks "Continue with
    Google" - even if they already have a session - so Google can show
    the account picker and let them choose or switch accounts. Skipping
    this when already authenticated would redirect straight to the home
    page and never show the picker.
    """
    # Ensure the session is persisted so the OAuth "state" Authlib
    # stores below is written to the cookie before we redirect to
    # Google. Otherwise the state can be lost on the first attempt
    # and only succeed on the retry.
    session.permanent = True

    redirect_uri = current_app.config["GOOGLE_REDIRECT_URI"]
    # prompt="select_account" forces Google to show the account
    # chooser every time instead of silently reusing the currently
    # signed-in account.
    return oauth.google.authorize_redirect(redirect_uri, prompt="select_account")


@oauth_bp.route("/callback")
def google_callback():
    """Handle the callback from Google after user grants consent."""
    try:
        token = oauth.google.authorize_access_token()
    except Exception as e:
        current_app.logger.error(
            "OAuth token error [%s]: %s", type(e).__name__, e, exc_info=True
        )
        # Surface the specific reason so we can distinguish a state
        # mismatch (cookie problem) from a token/clock/config problem.
        flash(f"Google authentication failed: {e}", "danger")
        return redirect(url_for("auth.login"))

    # Extract user info from the ID token (OIDC)
    user_info = token.get("userinfo")
    if not user_info:
        flash("Could not retrieve your Google account information.", "danger")
        return redirect(url_for("auth.login"))

    google_id = user_info["sub"]
    email = user_info.get("email", "")
    full_name = user_info.get("name", "")
    email_verified = user_info.get("email_verified", False)

    if not email:
        flash("Your Google account does not have an email address.", "danger")
        return redirect(url_for("auth.login"))

    # ── Try to find an existing user ─────────────────────────────
    # First check by OAuth ID (returning Google user)
    user = UserTable.query.filter_by(oauth_provider="google", oauth_id=google_id).first()

    if not user:
        # Check by email (link existing local account to Google)
        user = UserTable.query.filter_by(email=email).first()
        if user:
            # Link the existing account to Google
            user.oauth_provider = "google"
            user.oauth_id = google_id
            if email_verified:
                user.email_verified = True
            db.session.commit()

    # ── Create new user if none found ────────────────────────────
    if not user:
        # Generate a username from email (part before @)
        base_username = email.split("@")[0]
        username = base_username
        counter = 1
        while UserTable.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        # Assign default "User" role
        default_role = RoleTable.query.filter_by(name="User").first()

        user = UserTable(
            username=username,
            email=email,
            full_name=full_name or username,
            is_active=True,
            email_verified=email_verified,
            oauth_provider="google",
            oauth_id=google_id,
        )

        if default_role:
            user.roles = [default_role]

        db.session.add(user)
        db.session.commit()
        AuditService.log("REGISTER", "User", user.id, "New user registered via Google OAuth")

    # ── Login the user ───────────────────────────────────────────
    if not user.is_active:
        flash("Your account is inactive. Please contact administrator.", "warning")
        return redirect(url_for("auth.login"))

    # remember=True keeps the user signed in after the browser is
    # closed and reopened (returns to the same account).
    login_user(user, remember=True)
    AuditService.log("LOGIN", "User", user.id, "User logged in via Google OAuth")
    flash("Logged in successfully with Google.", "success")

    if user.has_permission("view_dashboard"):
        return redirect(url_for("dashboard.index"))
    else:
        return redirect(url_for("user_home.index"))
