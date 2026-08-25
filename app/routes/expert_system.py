# app/routes/expert_system.py
import os
import uuid
import shutil

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash,
    abort, send_file, send_from_directory, session, current_app,
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from extensions import db
from utils.decorators import require_permission
from app.forms.expert_system_forms import (
    CategoryForm,
    SymptomForm,
    DiseaseForm,
    RuleForm,
    FlockInfoForm,
    CaseReviewForm,
    ALLOWED_PHOTO_EXTENSIONS,
)
from app.services.diagnosis_service import DiagnosisService
from app.services.expert_system_service import (
    CategoryService,
    SymptomService,
    DiseaseService,
    RuleService,
    CaseService,
)
from app.services.audit_service import AuditService
from app.services.pdf_service import PdfService
from app.services.notification_service import NotificationService
from app.models.expert_system import CASE_STATUS_PENDING, CasePhoto, PHOTO_CATEGORIES

expert_system_bp = Blueprint("expert_system", __name__, url_prefix="/expert-system")

# ── Photo upload constants ──────────────────────────────────────────────────
MAX_PHOTOS_PER_CATEGORY = 5
_ALLOWED_MIME_PREFIXES = ("image/jpeg", "image/png", "image/webp", "image/gif")


def _parse_flock_data(form_data):
    flock_size = form_data.get("flock_size", "").strip()
    return {
        "flock_size": int(flock_size) if flock_size.isdigit() else None,
        "bird_age": form_data.get("bird_age", "").strip(),
        "breed": form_data.get("breed", "").strip(),
        "location": form_data.get("location", "").strip(),
        "notes": form_data.get("notes", "").strip(),
    }


def _stage_uploaded_photos(files_map: dict) -> list[dict]:
    """
    Save uploaded photo files to a temporary staging area.

    files_map: {category: [FileStorage, ...], ...}
    Returns a list of dicts: [{stage_path, original_filename, category}, ...]
    The stage_path is relative to UPLOAD_FOLDER.
    Orphaned staging dirs are cleaned up when photos are committed or the
    wizard is abandoned (garbage-collected on next upload from the same user).
    """
    staged = []
    stage_token = uuid.uuid4().hex
    upload_root = current_app.config["UPLOAD_FOLDER"]

    for category, file_list in files_map.items():
        if not file_list:
            continue
        for file in file_list[:MAX_PHOTOS_PER_CATEGORY]:
            if not file or not file.filename:
                continue
            # Basic content-type guard (browser may lie, but adds a layer)
            if not any(file.mimetype.startswith(p) for p in _ALLOWED_MIME_PREFIXES):
                continue
            ext = os.path.splitext(secure_filename(file.filename))[1].lower()
            if ext not in {f".{e}" for e in ALLOWED_PHOTO_EXTENSIONS}:
                continue

            stage_dir = os.path.join(upload_root, "cases", "_staging", stage_token, category)
            os.makedirs(stage_dir, exist_ok=True)
            filename = f"{uuid.uuid4().hex}{ext}"
            full_path = os.path.join(stage_dir, filename)
            file.save(full_path)
            rel_path = os.path.join("cases", "_staging", stage_token, category, filename)
            staged.append({
                "stage_path": rel_path,
                "original_filename": secure_filename(file.filename),
                "category": category,
            })

    return staged


def _commit_photos_to_case(case_id: int, staged: list[dict]) -> None:
    """
    Move staged files into cases/<case_id>/ and create CasePhoto DB records.
    Called immediately after a Case row is committed.
    """
    upload_root = current_app.config["UPLOAD_FOLDER"]
    dest_dir = os.path.join(upload_root, "cases", str(case_id))
    os.makedirs(dest_dir, exist_ok=True)

    for entry in staged:
        src = os.path.join(upload_root, entry["stage_path"])
        if not os.path.isfile(src):
            continue  # already moved or deleted

        filename = os.path.basename(src)
        dest = os.path.join(dest_dir, filename)
        shutil.move(src, dest)

        rel_path = os.path.join("cases", str(case_id), filename)
        photo = CasePhoto(
            case_id=case_id,
            file_path=rel_path,
            original_filename=entry["original_filename"],
            category=entry["category"],
        )
        db.session.add(photo)

    db.session.commit()


@expert_system_bp.route("/author-rules")
@login_required
@require_permission("author_rules")
def author_rules():
    return redirect(url_for("expert_system.rules_index"))


@expert_system_bp.route("/diagnose", methods=["GET", "POST"])
@login_required
@require_permission("run_diagnosis")
def diagnose():
    step = request.args.get("step", "1")
    if request.method == "POST":
        step = request.form.get("step", "1")

    flock_form = FlockInfoForm()
    diagnosis_results = None
    selected_ids = []
    saved_case = None

    if request.method == "POST" and step == "1":
        flock_data = _parse_flock_data(request.form)
        session["diagnosis_wizard"] = flock_data

        # Collect and stage any uploaded photos
        files_map = {
            cat: request.files.getlist(f"photos_{cat}")
            for cat in PHOTO_CATEGORIES
        }
        staged = _stage_uploaded_photos(files_map)
        # Overwrite previous staging on re-submission of step 1
        session["diagnosis_photos"] = staged

        return redirect(url_for("expert_system.diagnose", step="2"))

    if request.method == "POST" and step == "2":
        selected_ids = [int(sid) for sid in request.form.getlist("symptoms")]
        session["diagnosis_symptoms"] = selected_ids
        if not selected_ids:
            flash("សូមជ្រើសរើសរោគសញ្ញាយ៉ាងហោចណាស់មួយ។", "warning")
            return redirect(url_for("expert_system.diagnose", step="2"))
        return redirect(url_for("expert_system.diagnose", step="3"))

    if step == "3":
        selected_ids = session.get("diagnosis_symptoms", [])
        flock_data = session.get("diagnosis_wizard", {})
        if not selected_ids:
            flash("សូមជ្រើសរើសរោគសញ្ញាមុនពេលវិភាគ។", "warning")
            return redirect(url_for("expert_system.diagnose", step="2"))

        if request.method == "POST" and request.form.get("action") == "save":
            diagnosis_results = DiagnosisService.run_inference(selected_ids)
            saved_case = DiagnosisService.record_case(
                current_user.id,
                selected_ids,
                diagnosis_results[0] if diagnosis_results else None,
                flock_data=flock_data,
            )

            # Commit any staged photos now that we have a case ID
            staged_photos = session.get("diagnosis_photos", [])
            if staged_photos:
                _commit_photos_to_case(saved_case.id, staged_photos)

            session.pop("diagnosis_wizard", None)
            session.pop("diagnosis_symptoms", None)
            session.pop("diagnosis_photos", None)
            if saved_case and saved_case.disease:
                AuditService.log("DIAGNOSE", "Case", saved_case.id, f"Diagnosis saved: {saved_case.disease.name}")

            # Notify all doctors/admins about the new pending case
            NotificationService.notify_doctors_new_case(saved_case)

            flash("ករណីត្រូវបានរក្សាទុកដោយជោគជ័យ។", "success")
            return redirect(url_for("expert_system.cases_detail", case_id=saved_case.id))

        diagnosis_results = DiagnosisService.run_inference(selected_ids)

    if step == "2" and session.get("diagnosis_wizard"):
        flock_form.flock_size.data = session["diagnosis_wizard"].get("flock_size")
        flock_form.bird_age.data = session["diagnosis_wizard"].get("bird_age")
        flock_form.breed.data = session["diagnosis_wizard"].get("breed")
        flock_form.location.data = session["diagnosis_wizard"].get("location")
        flock_form.notes.data = session["diagnosis_wizard"].get("notes")

    if step in ("2", "3"):
        selected_ids = session.get("diagnosis_symptoms", selected_ids)

    symptoms_grouped = DiagnosisService.get_symptoms_grouped()

    return render_template(
        "expert_system/diagnose.html",
        step=step,
        flock_form=flock_form,
        symptoms_grouped=symptoms_grouped,
        results=diagnosis_results,
        selected_ids=set(selected_ids),
        flock_data=session.get("diagnosis_wizard", {}),
        saved_case=saved_case,
    )


@expert_system_bp.route("/cases")
@login_required
@require_permission("view_cases")
def cases_index():
    from app.services.expert_system_service import DiseaseService as _DS

    page = request.args.get("page", 1, type=int)
    status_filter = request.args.get("status", "").strip() or None
    disease_filter = request.args.get("disease_id", 0, type=int) or None
    date_from = request.args.get("date_from", "").strip() or None
    date_to = request.args.get("date_to", "").strip() or None

    user_id = None
    if not (current_user.has_permission("review_cases")):
        user_id = current_user.id

    pagination = CaseService.get_paginated(
        page=page,
        per_page=10,
        user_id=user_id,
        status=status_filter,
        disease_id=disease_filter,
        date_from=date_from,
        date_to=date_to,
    )

    diseases = _DS.get_all()

    return render_template(
        "expert_system/cases/index.html",
        cases=pagination.items,
        pagination=pagination,
        diseases=diseases,
        filters={
            "status": status_filter or "",
            "disease_id": disease_filter or 0,
            "date_from": date_from or "",
            "date_to": date_to or "",
        },
    )


@expert_system_bp.route("/cases/<int:case_id>")
@login_required
@require_permission("view_cases")
def cases_detail(case_id: int):
    case = CaseService.get_by_id(case_id)
    if case is None:
        abort(404)

    if not current_user.has_permission("review_cases"):
        if case.user_id != current_user.id:
            abort(403)

    review_form = CaseReviewForm()
    can_review = (
        current_user.has_permission("review_cases")
        and case.status == CASE_STATUS_PENDING
    )

    return render_template(
        "expert_system/cases/detail.html",
        case=case,
        review_form=review_form,
        can_review=can_review,
    )


@expert_system_bp.route("/cases/<int:case_id>/review", methods=["POST"])
@login_required
@require_permission("review_cases")
def cases_review(case_id: int):
    case = CaseService.get_by_id(case_id)
    if case is None:
        abort(404)

    form = CaseReviewForm()
    if form.validate_on_submit():
        override_id = form.override_disease_id.data if form.override_disease_id.data else None
        if override_id == 0:
            override_id = None
        CaseService.review_case(
            case,
            current_user.id,
            form.action.data,
            doctor_notes=form.doctor_notes.data or "",
            override_disease_id=override_id,
        )
        AuditService.log("REVIEW", "Case", case.id, f"Case reviewed: {form.action.data}")
        
        # Notify the case owner
        if case.user_id:
            status_km = "បានបញ្ជាក់" if form.action.data == "confirm" else "បានបដិសេធ"
            NotificationService.notify_user(
                user_id=case.user_id,
                title=f"ករណី #{case.id} របស់អ្នកត្រូវបាន{status_km}",
                message=form.doctor_notes.data or "",
                category="case",
                link=url_for("expert_system.cases_detail", case_id=case.id),
            )
        
        flash("ការពិនិត្យត្រូវបានរក្សាទុក។", "success")
    else:
        flash("មិនអាចដាក់ស្នើការពិនិត្យបានទេ។", "danger")

    return redirect(url_for("expert_system.cases_detail", case_id=case_id))


@expert_system_bp.route("/cases/<int:case_id>/feedback", methods=["POST"])
@login_required
@require_permission("view_cases")
def cases_feedback(case_id: int):
    case = CaseService.get_by_id(case_id)
    if case is None:
        abort(404)

    # Only the case owner can leave feedback
    if case.user_id != current_user.id:
        abort(403)

    # Prevent double feedback
    if case.feedback_rating is not None:
        flash("អ្នកបានផ្តល់មតិប្រតិកម្មរួចហើយ។", "info")
        return redirect(url_for("expert_system.cases_detail", case_id=case_id))

    rating = request.form.get("rating", 0, type=int)
    feedback_text = request.form.get("feedback_text", "").strip()

    if rating < 1 or rating > 5:
        flash("សូមជ្រើសរើសពិន្ទុវាយតម្លៃ។", "warning")
        return redirect(url_for("expert_system.cases_detail", case_id=case_id))

    CaseService.submit_feedback(case, rating, feedback_text)
    flash("សូមអរគុណសម្រាប់មតិប្រតិកម្មរបស់អ្នក!", "success")
    return redirect(url_for("expert_system.cases_detail", case_id=case_id))


@expert_system_bp.route("/cases/photos/<path:filename>")
@login_required
@require_permission("view_cases")
def cases_photo(filename: str):
    """Serve a case symptom photo.

    Access rules:
      - Doctors / Admins (review_cases): can view any case photo.
      - Farmers (run_diagnosis only): can only view photos belonging to their own cases.
    Prevents directory traversal; only serves files under uploads/cases/.
    """
    safe = os.path.normpath(filename)
    # Block absolute paths and traversal attempts
    if os.path.isabs(safe) or safe.startswith(".."):
        abort(404)

    # The stored file_path in CasePhoto is like  "cases/42/abc.jpg"
    # Reconstruct so the first path segment is the case_id folder
    parts = safe.replace("\\", "/").split("/")
    # parts[0] should be "cases", parts[1] the case_id dir
    if len(parts) < 3 or parts[0] != "cases":
        abort(404)

    try:
        case_id = int(parts[1])
    except (ValueError, IndexError):
        abort(404)

    # Ownership check for non-reviewers
    if not current_user.has_permission("review_cases"):
        case = CaseService.get_by_id(case_id)
        if case is None or case.user_id != current_user.id:
            abort(403)

    upload_root = current_app.config["UPLOAD_FOLDER"]
    full_path = os.path.join(upload_root, safe)
    if not os.path.isfile(full_path):
        abort(404)

    directory = os.path.dirname(full_path)
    file_name = os.path.basename(full_path)
    return send_from_directory(directory, file_name)


@expert_system_bp.route("/cases/<int:case_id>/print")
@login_required
@require_permission("view_cases")
def cases_print(case_id: int):
    case = CaseService.get_by_id(case_id)
    if case is None:
        abort(404)
    if not current_user.has_permission("review_cases"):
        if case.user_id != current_user.id:
            abort(403)
    return render_template("expert_system/cases/print.html", case=case, pdf_mode=False)


@expert_system_bp.route("/cases/<int:case_id>/pdf")
@login_required
@require_permission("view_cases")
def cases_pdf(case_id: int):
    case = CaseService.get_by_id(case_id)
    if case is None:
        abort(404)
    if not current_user.has_permission("review_cases"):
        if case.user_id != current_user.id:
            abort(403)

    pdf_buffer = PdfService.render_case_pdf(case)
    if pdf_buffer is None:
        flash("មិនអាចបង្កើត PDF បានទេ។ សូមប្រើមុខងារបោះពុម្ព។", "warning")
        return redirect(url_for("expert_system.cases_print", case_id=case_id))

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"case_{case_id}_report.pdf",
        mimetype="application/pdf",
    )


@expert_system_bp.route("/cases/export-csv")
@login_required
@require_permission("view_cases")
def cases_export_csv():
    import csv
    from io import StringIO, BytesIO

    if not current_user.has_permission("review_cases"):
        abort(403)

    status_filter = request.args.get("status", "").strip() or None
    disease_filter = request.args.get("disease_id", 0, type=int) or None
    date_from = request.args.get("date_from", "").strip() or None
    date_to = request.args.get("date_to", "").strip() or None

    pagination = CaseService.get_paginated(
        page=1, per_page=10000,
        status=status_filter, disease_id=disease_filter,
        date_from=date_from, date_to=date_to,
    )
    cases = pagination.items

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow([
        "ID", "Date", "User", "Disease", "Confidence (%)",
        "Status", "Flock Size", "Bird Age", "Breed", "Location",
        "Symptoms", "Reviewed By", "Doctor Notes",
    ])
    for c in cases:
        writer.writerow([
            c.id,
            c.created_at.strftime("%Y-%m-%d %H:%M"),
            c.user.username if c.user else "",
            c.final_disease.name if c.final_disease else "",
            c.confidence or "",
            c.status,
            c.flock_size or "",
            c.bird_age or "",
            c.breed or "",
            c.location or "",
            "; ".join(s.name for s in c.symptoms),
            c.reviewed_by.full_name if c.reviewed_by else "",
            c.doctor_notes or "",
        ])

    output = BytesIO()
    output.write("\ufeff".encode("utf-8"))  # BOM for Excel Khmer support
    output.write(si.getvalue().encode("utf-8"))
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="cases_export.csv",
        mimetype="text/csv; charset=utf-8",
    )


@expert_system_bp.route("/categories")
@login_required
@require_permission("manage_categories")
def categories_index():
    categories = CategoryService.get_all()
    return render_template("expert_system/categories/index.html", categories=categories)


@expert_system_bp.route("/categories/create", methods=["GET", "POST"])
@login_required
@require_permission("manage_categories")
def categories_create():
    form = CategoryForm()
    if form.validate_on_submit():
        category = CategoryService.create(
            {"name": form.name.data, "description": form.description.data}
        )
        AuditService.log("CREATE", "Category", category.id, f"Created category: {category.name}")
        flash(f"ប្រភេទ '{category.name}' ត្រូវបានបង្កើត។", "success")
        return redirect(url_for("expert_system.categories_index"))
    return render_template("expert_system/categories/create.html", form=form)


@expert_system_bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
@require_permission("manage_categories")
def categories_edit(category_id: int):
    category = CategoryService.get_by_id(category_id)
    if category is None:
        abort(404)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        CategoryService.update(
            category,
            {"name": form.name.data, "description": form.description.data},
        )
        AuditService.log("UPDATE", "Category", category.id, f"Updated category: {category.name}")
        flash("ប្រភេទត្រូវបានកែប្រែ។", "success")
        return redirect(url_for("expert_system.categories_index"))
    return render_template(
        "expert_system/categories/edit.html",
        form=form,
        category=category,
    )


@expert_system_bp.route("/categories/<int:category_id>/delete", methods=["GET", "POST"])
@login_required
@require_permission("manage_categories")
def categories_delete(category_id: int):
    category = CategoryService.get_by_id(category_id)
    if category is None:
        abort(404)
    if request.method == "POST":
        category_name = category.name
        CategoryService.delete(category)
        AuditService.log("DELETE", "Category", category_id, f"Deleted category: {category_name}")
        flash("ប្រភេទត្រូវបានលុប។", "success")
        return redirect(url_for("expert_system.categories_index"))
    return render_template(
        "expert_system/categories/delete_confirm.html",
        category=category,
    )


@expert_system_bp.route("/symptoms")
@login_required
@require_permission("manage_symptoms")
def symptoms_index():
    symptoms = SymptomService.get_all()
    return render_template("expert_system/symptoms/index.html", symptoms=symptoms)


@expert_system_bp.route("/symptoms/create", methods=["GET", "POST"])
@login_required
@require_permission("manage_symptoms")
def symptoms_create():
    form = SymptomForm()
    if form.validate_on_submit():
        try:
            symptom = SymptomService.create(
                {
                    "name": form.name.data,
                    "description": form.description.data,
                    "category_id": form.category_id.data,
                }
            )
            AuditService.log("CREATE", "Symptom", symptom.id, f"Created symptom: {symptom.name}")
            flash(f"Symptom '{symptom.name}' created successfully.", "success")
            return redirect(url_for("expert_system.symptoms_index"))
        except Exception:
            db.session.rollback()
            flash("A symptom with this name already exists.", "danger")
    return render_template("expert_system/symptoms/create.html", form=form)


@expert_system_bp.route("/symptoms/<int:symptom_id>/edit", methods=["GET", "POST"])
@login_required
@require_permission("manage_symptoms")
def symptoms_edit(symptom_id: int):
    symptom = SymptomService.get_by_id(symptom_id)
    if symptom is None:
        abort(404)
    form = SymptomForm(obj=symptom)
    if form.validate_on_submit():
        SymptomService.update(
            symptom,
            {
                "name": form.name.data,
                "description": form.description.data,
                "category_id": form.category_id.data,
            },
        )
        AuditService.log("UPDATE", "Symptom", symptom.id, f"Updated symptom: {symptom.name}")
        flash("រោគសញ្ញាត្រូវបានកែប្រែ។", "success")
        return redirect(url_for("expert_system.symptoms_index"))
    return render_template(
        "expert_system/symptoms/edit.html",
        form=form,
        symptom=symptom,
    )


@expert_system_bp.route("/symptoms/<int:symptom_id>/delete", methods=["GET", "POST"])
@login_required
@require_permission("manage_symptoms")
def symptoms_delete(symptom_id: int):
    symptom = SymptomService.get_by_id(symptom_id)
    if symptom is None:
        abort(404)
    if request.method == "POST":
        symptom_name = symptom.name
        SymptomService.delete(symptom)
        AuditService.log("DELETE", "Symptom", symptom_id, f"Deleted symptom: {symptom_name}")
        flash("រោគសញ្ញាត្រូវបានលុប។", "success")
        return redirect(url_for("expert_system.symptoms_index"))
    return render_template(
        "expert_system/symptoms/delete_confirm.html",
        symptom=symptom,
    )


@expert_system_bp.route("/diseases")
@login_required
@require_permission("manage_diseases")
def diseases_index():
    diseases = DiseaseService.get_all()
    return render_template("expert_system/diseases/index.html", diseases=diseases)


@expert_system_bp.route("/diseases/create", methods=["GET", "POST"])
@login_required
@require_permission("manage_diseases")
def diseases_create():
    form = DiseaseForm()
    if form.validate_on_submit():
        try:
            disease = DiseaseService.create(
                {
                    "name": form.name.data,
                    "description": form.description.data,
                    "treatment": form.treatment.data,
                    "prevention": form.prevention.data,
                    "severity": form.severity.data,
                    "is_contagious": form.is_contagious.data,
                    "category_id": form.category_id.data,
                }
            )
            AuditService.log("CREATE", "Disease", disease.id, f"Created disease: {disease.name}")
            flash(f"Disease '{disease.name}' created successfully.", "success")
            return redirect(url_for("expert_system.diseases_index"))
        except Exception:
            db.session.rollback()
            flash("A disease with this name already exists.", "danger")
    return render_template("expert_system/diseases/create.html", form=form)


@expert_system_bp.route("/diseases/<int:disease_id>/edit", methods=["GET", "POST"])
@login_required
@require_permission("manage_diseases")
def diseases_edit(disease_id: int):
    disease = DiseaseService.get_by_id(disease_id)
    if disease is None:
        abort(404)
    form = DiseaseForm(obj=disease)
    if form.validate_on_submit():
        DiseaseService.update(
            disease,
            {
                "name": form.name.data,
                "description": form.description.data,
                "treatment": form.treatment.data,
                "prevention": form.prevention.data,
                "severity": form.severity.data,
                "is_contagious": form.is_contagious.data,
                "category_id": form.category_id.data,
            },
        )
        AuditService.log("UPDATE", "Disease", disease.id, f"Updated disease: {disease.name}")
        flash("ជំងឺត្រូវបានកែប្រែ។", "success")
        return redirect(url_for("expert_system.diseases_index"))
    return render_template(
        "expert_system/diseases/edit.html",
        form=form,
        disease=disease,
    )


@expert_system_bp.route("/diseases/<int:disease_id>/delete", methods=["GET", "POST"])
@login_required
@require_permission("manage_diseases")
def diseases_delete(disease_id: int):
    disease = DiseaseService.get_by_id(disease_id)
    if disease is None:
        abort(404)
    if request.method == "POST":
        disease_name = disease.name
        DiseaseService.delete(disease)
        AuditService.log("DELETE", "Disease", disease_id, f"Deleted disease: {disease_name}")
        flash("ជំងឺត្រូវបានលុប។", "success")
        return redirect(url_for("expert_system.diseases_index"))
    return render_template(
        "expert_system/diseases/delete_confirm.html",
        disease=disease,
    )


@expert_system_bp.route("/rules")
@login_required
@require_permission("manage_rules")
def rules_index():
    rules = RuleService.get_all()
    return render_template("expert_system/rules/index.html", rules=rules)


@expert_system_bp.route("/rules/create", methods=["GET", "POST"])
@login_required
@require_permission("manage_rules")
def rules_create():
    form = RuleForm()
    if form.validate_on_submit():
        rule = RuleService.create(
            {
                "title": form.title.data,
                "description": form.description.data,
                "priority": form.priority.data,
                "confidence": form.confidence.data,
                "disease_id": form.disease_id.data,
            },
            symptom_ids=form.symptom_ids.data or [],
        )
        AuditService.log("CREATE", "Rule", rule.id, f"Created rule: {rule.title}")
        flash(f"វិធាន '{rule.title}' ត្រូវបានបង្កើត។", "success")
        return redirect(url_for("expert_system.rules_index"))
    return render_template("expert_system/rules/create.html", form=form)


@expert_system_bp.route("/rules/<int:rule_id>/edit", methods=["GET", "POST"])
@login_required
@require_permission("manage_rules")
def rules_edit(rule_id: int):
    rule = RuleService.get_by_id(rule_id)
    if rule is None:
        abort(404)
    form = RuleForm(original_rule=rule, obj=rule)
    if form.validate_on_submit():
        RuleService.update(
            rule,
            {
                "title": form.title.data,
                "description": form.description.data,
                "priority": form.priority.data,
                "confidence": form.confidence.data,
                "disease_id": form.disease_id.data,
            },
            symptom_ids=form.symptom_ids.data or [],
        )
        AuditService.log("UPDATE", "Rule", rule.id, f"Updated rule: {rule.title}")
        flash("វិធានត្រូវបានកែប្រែ។", "success")
        return redirect(url_for("expert_system.rules_index"))
    return render_template(
        "expert_system/rules/edit.html",
        form=form,
        rule=rule,
    )


@expert_system_bp.route("/rules/<int:rule_id>/delete", methods=["GET", "POST"])
@login_required
@require_permission("manage_rules")
def rules_delete(rule_id: int):
    rule = RuleService.get_by_id(rule_id)
    if rule is None:
        abort(404)
    if request.method == "POST":
        rule_title = rule.title
        RuleService.delete(rule)
        AuditService.log("DELETE", "Rule", rule_id, f"Deleted rule: {rule_title}")
        flash("វិធានត្រូវបានលុប។", "success")
        return redirect(url_for("expert_system.rules_index"))
    return render_template(
        "expert_system/rules/delete_confirm.html",
        rule=rule,
    )
