# app/routes/doctor_application_routes.py
import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from extensions import db
from app.models.doctor_application import (
    DoctorApplication, APPLICATION_PENDING, APPLICATION_APPROVED, APPLICATION_REJECTED,
)
from app.models.role import RoleTable
from app.forms.doctor_application_forms import DoctorApplicationForm, ApplicationReviewForm
from app.services.audit_service import AuditService

doctor_app_bp = Blueprint("doctor_app", __name__, url_prefix="/doctor-application")


def _save_pdf(file, user_id):
    """Save uploaded PDF and return relative path."""
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "applications", str(user_id))
    os.makedirs(upload_dir, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    return os.path.join("applications", str(user_id), filename)


@doctor_app_bp.route("/apply", methods=["GET", "POST"])
@login_required
def apply():
    # Only regular Users can apply (not already Doctor/Admin)
    if current_user.has_role("Admin") or current_user.has_role("Doctor"):
        flash("You already have elevated privileges.", "info")
        return redirect(url_for("expert_system.diagnose"))

    # Check if there's already a pending application
    existing = DoctorApplication.query.filter_by(
        user_id=current_user.id, status=APPLICATION_PENDING
    ).first()
    if existing:
        flash("You already have a pending application. Please wait for admin review.", "info")
        return render_template("doctor_application/status.html", application=existing)

    form = DoctorApplicationForm()

    if form.validate_on_submit():
        # Save PDFs
        dv_path = _save_pdf(form.pdf_dv_certificate.data, current_user.id)
        id_path = _save_pdf(form.pdf_id_card.data, current_user.id)
        birth_path = _save_pdf(form.pdf_birth_certificate.data, current_user.id)
        diploma_path = None
        if form.pdf_diploma.data:
            diploma_path = _save_pdf(form.pdf_diploma.data, current_user.id)

        application = DoctorApplication(
            user_id=current_user.id,
            full_name=form.full_name.data,
            phone=form.phone.data or None,
            address=form.address.data or None,
            motivation=form.motivation.data or None,
            pdf_dv_certificate=dv_path,
            pdf_id_card=id_path,
            pdf_birth_certificate=birth_path,
            pdf_diploma=diploma_path,
            status=APPLICATION_PENDING,
        )
        db.session.add(application)
        db.session.commit()

        AuditService.log("CREATE", "DoctorApplication", application.id, "Doctor application submitted")
        flash("Your application has been submitted! An admin will review it shortly.", "success")
        return render_template("doctor_application/status.html", application=application)

    return render_template("doctor_application/apply.html", form=form)


@doctor_app_bp.route("/my-status")
@login_required
def my_status():
    """User checks their application status."""
    applications = DoctorApplication.query.filter_by(
        user_id=current_user.id
    ).order_by(DoctorApplication.created_at.desc()).all()
    return render_template("doctor_application/my_status.html", applications=applications)


@doctor_app_bp.route("/admin/list")
@login_required
def admin_list():
    """Admin views all applications."""
    if not current_user.has_role("Admin"):
        abort(403)

    status_filter = request.args.get("status", "").strip() or None
    query = DoctorApplication.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    applications = query.order_by(DoctorApplication.created_at.desc()).all()

    return render_template(
        "doctor_application/admin_list.html",
        applications=applications,
        current_filter=status_filter or "",
    )


@doctor_app_bp.route("/admin/<int:app_id>", methods=["GET", "POST"])
@login_required
def admin_review(app_id):
    """Admin reviews a specific application."""
    if not current_user.has_role("Admin"):
        abort(403)

    application = DoctorApplication.query.get_or_404(app_id)
    form = ApplicationReviewForm()

    if form.validate_on_submit():
        from datetime import datetime

        application.reviewed_by_id = current_user.id
        application.reviewed_at = datetime.utcnow()
        application.review_notes = form.review_notes.data or None

        if form.action.data == "approve":
            application.status = APPLICATION_APPROVED
            # Assign Doctor role to the user
            doctor_role = db.session.scalar(db.select(RoleTable).filter_by(name="Doctor"))
            if doctor_role:
                application.user.roles = [doctor_role]
            AuditService.log("UPDATE", "DoctorApplication", application.id, "Application approved")
            flash(f"Application approved. {application.full_name} is now a Doctor.", "success")
        else:
            application.status = APPLICATION_REJECTED
            AuditService.log("UPDATE", "DoctorApplication", application.id, "Application rejected")
            flash("Application rejected.", "info")

        db.session.commit()
        return redirect(url_for("doctor_app.admin_list"))

    return render_template(
        "doctor_application/admin_review.html",
        application=application,
        form=form,
    )


@doctor_app_bp.route("/uploads/<path:filename>")
@login_required
def serve_upload(filename):
    """Serve uploaded PDF files (admin only)."""
    if not current_user.has_permission("USER_CREATE"):
        abort(403)
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    # Ensure safe path join on Windows — normalize separators
    safe_path = os.path.normpath(filename)
    # Prevent directory traversal
    if safe_path.startswith("..") or os.path.isabs(safe_path):
        abort(404)
    full_path = os.path.join(upload_dir, safe_path)
    if not os.path.isfile(full_path):
        abort(404)
    directory = os.path.dirname(full_path)
    file_name = os.path.basename(full_path)
    return send_from_directory(directory, file_name)
