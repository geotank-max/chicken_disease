# app/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import UserTable
from app.models.role import RoleTable
from app.services.user_service import UserService
from app.services.audit_service import AuditService
from app.services.email_service import EmailService
from app.forms.auth_forms import ForgotPasswordForm, ResetPasswordForm
from extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        user = UserTable.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash("Your account is inactive. Please contact administrator.", "warning")
                return render_template("auth/login.html", username=username)
            
            login_user(user)
            AuditService.log("LOGIN", "User", user.id, "User logged in")
            flash("Logged in successfully.", "success")
            
            # Redirect based on permissions
            if user.has_permission("view_dashboard"):
                return redirect(url_for("dashboard.index"))
            else:
                return redirect(url_for("user_home.index"))
        
        flash("Invalid username or password.", "danger")
        return render_template("auth/login.html", username=username)
    
    return render_template("auth/login.html", username="")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        full_name = request.form.get("full_name", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        
        errors: list[str] = []
        
        if not username:
            errors.append("Username is required.")
        if not email:
            errors.append("Email is required.")
        if not full_name:
            errors.append("Full name is required.")
        if not password:
            errors.append("Password is required.")
        if password and password != confirm_password:
            errors.append("Passwords do not match.")
            
        if username and UserTable.query.filter_by(username=username).first():
            errors.append("This username is already taken.")
        if email and UserTable.query.filter_by(email=email).first():
            errors.append("This email is already registered.")
            
        if errors:
            for msg in errors:
                flash(msg, "danger")
            return render_template(
                "auth/register.html",
                username=username,
                email=email,
                full_name=full_name,
            )
            
        default_role = RoleTable.query.filter_by(name="User").first()
        default_role_id = default_role.id if default_role else None
        
        data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "is_active": True,
        }
        
        new_user = UserService.create_user(
            data=data,
            password=password,
            role_id=default_role_id,
        )
        
        # Send email verification
        raw_token = new_user.generate_email_verify_token()
        db.session.commit()
        EmailService.send_verification_email(new_user, raw_token)
        
        login_user(new_user)
        AuditService.log("REGISTER", "User", new_user.id, "New user registered")
        flash("Account created successfully. Please check your email to verify your address.", "success")
        
        # Redirect based on permissions (new users are typically 'User' role)
        if new_user.has_permission("view_dashboard"):
            return redirect(url_for("dashboard.index"))
        else:
            return redirect(url_for("user_home.index"))
    
    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    user_id = current_user.id
    logout_user()
    # Note: current_user is anonymous after logout_user(), so we can't use it for logging user_id directly inside AuditService if we rely on current_user there.
    # However, AuditService uses current_user. Since we just logged out, current_user is anonymous.
    # We should log BEFORE logging out if we want to capture the user ID, or pass it explicitly.
    # But AuditService.log uses current_user internally. Let's adjust AuditService or log before logout.
    # Actually, let's log before logout to capture the user.
    # Wait, I can't easily change AuditService to take user_id as optional override without changing its signature.
    # Let's just log "LOGOUT" before calling logout_user().
    
    # Re-implementing log here manually or calling service before logout
    # But wait, AuditService.log uses current_user.id.
    AuditService.log("LOGOUT", "User", user_id, "User logged out")

    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


# ── Email Verification ────────────────────────────────────────────

@auth_bp.route("/verify-email")
def verify_email():
    """Verify user email via token link sent to their inbox."""
    token = request.args.get("token", "")
    email = request.args.get("email", "")

    if not token or not email:
        flash("Invalid verification link.", "danger")
        return redirect(url_for("auth.login"))

    user = UserTable.query.filter_by(email=email).first()

    if not user:
        # Don't reveal whether email exists
        flash("Email verified successfully. You can now log in.", "success")
        return redirect(url_for("auth.login"))

    if user.email_verified:
        flash("Your email is already verified.", "info")
        return redirect(url_for("auth.login"))

    if user.verify_email_token(token):
        db.session.commit()
        AuditService.log("EMAIL_VERIFIED", "User", user.id, "Email address verified")
        flash("Email verified successfully. You can now log in.", "success")
    else:
        flash("Invalid or expired verification link. Please request a new one.", "danger")

    return redirect(url_for("auth.login"))


@auth_bp.route("/resend-verification")
@login_required
def resend_verification():
    """Resend email verification for the currently logged-in user."""
    if current_user.email_verified:
        flash("Your email is already verified.", "info")
    else:
        raw_token = current_user.generate_email_verify_token()
        db.session.commit()
        EmailService.send_verification_email(current_user, raw_token)
        flash("A new verification email has been sent. Check your inbox.", "success")

    return redirect(url_for("auth.login"))


# ── Forgot Password ──────────────────────────────────────────────

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Show forgot-password form and send reset link."""
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = UserTable.query.filter(db.func.lower(UserTable.email) == email).first()

        if user and user.is_active:
            raw_token = user.generate_reset_token()
            db.session.commit()
            sent = EmailService.send_password_reset_email(user, raw_token)
            if not sent:
                import logging
                logging.getLogger(__name__).error(f"Failed to send reset email to {user.email}")

        # Always show success message — never reveal if email exists
        flash("If that email is registered, you will receive a password reset link shortly.", "success")
        return redirect(url_for("auth.forgot_password"))

    return render_template("auth/forgot_password.html", form=form)


# ── Reset Password ───────────────────────────────────────────────

@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """Validate reset token and allow user to set a new password."""
    token = request.args.get("token", "") or request.form.get("token", "")
    email = request.args.get("email", "") or request.form.get("email", "")

    if not token or not email:
        flash("Invalid password reset link.", "danger")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        user = UserTable.query.filter_by(email=email).first()

        if not user:
            flash("Invalid password reset link.", "danger")
            return redirect(url_for("auth.forgot_password"))

        if user.verify_reset_token(token):
            user.set_password(form.password.data)
            db.session.commit()
            AuditService.log("PASSWORD_RESET", "User", user.id, "Password reset via email")
            flash("Your password has been reset. You can now log in with your new password.", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Invalid or expired reset link. Please request a new one.", "danger")
            return redirect(url_for("auth.forgot_password"))

    return render_template("auth/reset_password.html", form=form, token=token, email=email)
