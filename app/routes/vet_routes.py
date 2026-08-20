# app/routes/vet_routes.py
"""
Vet directory: list nearby vets, filter by province, and escalate cases.
"""
import math
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from flask_babel import gettext as _
from extensions import db
from app.models.vet_clinic import VetClinic
from app.models.expert_system import Case
from app.services.notification_service import NotificationService

vets_bp = Blueprint("vets", __name__, url_prefix="/vets")


def _haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lng points."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


@vets_bp.route("/")
@login_required
def index():
    """List vet clinics with optional province filter and distance sort."""
    province = request.args.get("province", "").strip()
    user_lat = request.args.get("lat", type=float)
    user_lng = request.args.get("lng", type=float)

    query = VetClinic.query.filter_by(is_active=True)
    if province:
        query = query.filter(VetClinic.province.ilike(f"%{province}%"))

    clinics = query.order_by(VetClinic.province, VetClinic.name).all()

    # If user provides geolocation, compute distances and sort
    if user_lat is not None and user_lng is not None:
        for clinic in clinics:
            if clinic.latitude and clinic.longitude:
                clinic.distance_km = round(
                    _haversine(user_lat, user_lng, clinic.latitude, clinic.longitude), 1
                )
            else:
                clinic.distance_km = None
        clinics.sort(key=lambda c: c.distance_km if c.distance_km is not None else 9999)
    else:
        for clinic in clinics:
            clinic.distance_km = None

    # Get distinct provinces for filter dropdown
    provinces = sorted(set(c.province for c in VetClinic.query.filter_by(is_active=True).all()))

    return render_template(
        "vets/index.html",
        clinics=clinics,
        provinces=provinces,
        selected_province=province,
        user_lat=user_lat,
        user_lng=user_lng,
    )


@vets_bp.route("/api/list")
@login_required
def api_list():
    """JSON API for vet clinics (for offline caching)."""
    clinics = VetClinic.query.filter_by(is_active=True).all()
    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "address": c.address,
            "province": c.province,
            "district": c.district,
            "latitude": c.latitude,
            "longitude": c.longitude,
            "specialization": c.specialization,
        }
        for c in clinics
    ])


@vets_bp.route("/escalate/<int:case_id>", methods=["POST"])
@login_required
def escalate(case_id: int):
    """Escalate a case to the nearest vet / any available doctor."""
    case = Case.query.get_or_404(case_id)

    # Only case owner can escalate
    if case.user_id != current_user.id:
        flash(_("You cannot escalate this case."), "danger")
        return redirect(url_for("expert_system.cases_detail", case_id=case_id))

    vet_id = request.form.get("vet_id", type=int)

    # Try to notify a specific vet if selected
    if vet_id:
        clinic = VetClinic.query.get(vet_id)
        if clinic and clinic.user_id:
            NotificationService.notify_user(
                user_id=clinic.user_id,
                title=_("Case escalated to you"),
                message=f"Case #{case.id} has been escalated by {current_user.full_name}. "
                        f"Disease: {case.disease.name if case.disease else 'Unknown'}. "
                        f"Please review.",
                link=url_for("expert_system.cases_detail", case_id=case.id),
            )
    else:
        # Notify all doctors
        from app.models.role import RoleTable
        doctor_role = RoleTable.query.filter_by(name="Doctor").first()
        if doctor_role:
            for doctor in doctor_role.users:
                NotificationService.notify_user(
                    user_id=doctor.id,
                    title=_("Case escalated to you"),
                    message=f"Case #{case.id} escalated by {current_user.full_name}. "
                            f"Disease: {case.disease.name if case.disease else 'Unknown'}.",
                    link=url_for("expert_system.cases_detail", case_id=case.id),
                )

    flash(_("Case escalated successfully."), "success")
    return redirect(url_for("expert_system.cases_detail", case_id=case_id))
