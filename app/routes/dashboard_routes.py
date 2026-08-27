from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from utils.decorators import require_permission
from app.services.dashboard_service import DashboardService
from app.services.expert_system_service import DiseaseService
from app.models.expert_system import (
    CASE_STATUS_PENDING,
    CASE_STATUS_CONFIRMED,
    CASE_STATUS_REJECTED,
)

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")

_VALID_STATUSES = {CASE_STATUS_PENDING, CASE_STATUS_CONFIRMED, CASE_STATUS_REJECTED}


@dashboard_bp.route("/")
@login_required
@require_permission("view_dashboard")
def index():
    # ── Read simple, optional filters from the query string ────────────────
    date_from = request.args.get("date_from", "").strip() or None
    date_to = request.args.get("date_to", "").strip() or None
    disease_id = request.args.get("disease_id", 0, type=int) or None
    status = request.args.get("status", "").strip() or None
    if status not in _VALID_STATUSES:
        status = None

    filters = {
        "date_from": date_from,
        "date_to": date_to,
        "disease_id": disease_id,
        "status": status,
    }

    summary = DashboardService.get_summary(**filters)
    top_diseases = DashboardService.get_top_diseases(**filters)
    cases_by_day = DashboardService.get_cases_by_day(**filters)
    recent_cases = DashboardService.get_recent_cases(**filters)
    status_breakdown = DashboardService.get_status_breakdown(**filters)
    high_risk_cases = DashboardService.get_high_risk_cases(**filters)

    diseases = DiseaseService.get_all()

    return render_template(
        "dashboard/index.html",
        summary=summary,
        top_diseases=top_diseases,
        cases_by_day=cases_by_day,
        recent_cases=recent_cases,
        status_breakdown=status_breakdown,
        high_risk_cases=high_risk_cases,
        diseases=diseases,
        filters={
            "date_from": date_from or "",
            "date_to": date_to or "",
            "disease_id": disease_id or 0,
            "status": status or "",
        },
        has_filters=any([date_from, date_to, disease_id, status]),
    )
