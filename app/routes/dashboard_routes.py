from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from utils.decorators import require_permission
from app.services.dashboard_service import DashboardService

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
@login_required
@require_permission("view_dashboard")
def index():
    if not (current_user.has_role("Admin") or current_user.has_role("Doctor")):
        abort(403)

    summary = DashboardService.get_summary()
    top_diseases = DashboardService.get_top_diseases()
    cases_by_day = DashboardService.get_cases_by_day()
    recent_cases = DashboardService.get_recent_cases()
    status_breakdown = DashboardService.get_status_breakdown()

    return render_template(
        "dashboard/index.html",
        summary=summary,
        top_diseases=top_diseases,
        cases_by_day=cases_by_day,
        recent_cases=recent_cases,
        status_breakdown=status_breakdown,
    )
