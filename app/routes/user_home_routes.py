# app/routes/user_home_routes.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.services.user_home_service import UserHomeService

user_home_bp = Blueprint("user_home", __name__, url_prefix="/home")


@user_home_bp.route("/")
@login_required
def index():
    stats = UserHomeService.get_my_stats(current_user.id)
    recent_cases = UserHomeService.get_recent_cases(current_user.id)
    featured_disease = UserHomeService.get_featured_disease()

    return render_template(
        "user_home/index.html",
        stats=stats,
        recent_cases=recent_cases,
        featured_disease=featured_disease,
    )

