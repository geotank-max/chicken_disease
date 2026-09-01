# app/__init__.py
import os
from flask import Flask, redirect, url_for, render_template, request, session
from config import Config
from extensions import db, csrf, login_manager
from app.models.user import UserTable


def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    # Initialize Google OAuth
    from app.services.oauth_service import init_oauth
    init_oauth(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "សូមចូលប្រើប្រាស់មុន។"
    login_manager.login_message_category = "warning"

    @app.after_request
    def set_cache_headers(response):
        """
        Cache policy per endpoint:
        - OAuth endpoints: never cache, so Google always runs a fresh
          login flow and shows the account picker.
        - Home page: allow a short *private* cache so that when the user
          closes and reopens the browser on the same account, the page
          loads instantly from cache instead of a full server round-trip.
        - Everything else: left to the browser's default behaviour.
        """
        endpoint = request.endpoint or ""

        if endpoint.startswith("oauth."):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        elif endpoint == "user_home.index":
            # private = only this user's browser may cache it (never a
            # shared proxy). 5-minute freshness window.
            response.headers["Cache-Control"] = "private, max-age=300"

        return response

    @login_manager.user_loader
    def load_user(user_id: str):
        return UserTable.query.get(int(user_id))

    from app.routes.user_routes import user_bp
    from app.routes.role_routes import role_bp
    from app.routes.permission_routes import permission_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.expert_system import expert_system_bp
    from app.routes.audit_routes import audit_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(permission_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(expert_system_bp)

    from app.routes.oauth_routes import oauth_bp
    app.register_blueprint(oauth_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(dashboard_bp)

    from app.routes.doctor_application_routes import doctor_app_bp
    app.register_blueprint(doctor_app_bp)

    from app.routes.notification_routes import notification_bp
    app.register_blueprint(notification_bp)

    from app.routes.user_home_routes import user_home_bp
    app.register_blueprint(user_home_bp)

    from app.translations import t, get_current_language, LANGUAGES, get_translated_option

    # Context processor: inject localization and badges into all templates
    @app.context_processor
    def inject_i18n_and_badges():
        from flask_login import current_user
        context = {
            "t": t,
            "current_lang": get_current_language(),
            "LANGUAGES": LANGUAGES,
            "get_translated_option": get_translated_option,
        }
        if current_user and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            from app.services.notification_service import NotificationService
            context["notif_count"] = NotificationService.get_unread_count(current_user.id)
            if current_user.has_permission("USER_CREATE"):
                context["pending_applications"] = NotificationService.get_pending_applications_count()
                context["pending_cases"] = NotificationService.get_pending_cases_count()
            elif current_user.has_permission("review_cases"):
                context["pending_cases"] = NotificationService.get_pending_cases_count()
        return context

    app.jinja_env.filters["t"] = t

    @app.route("/set-language/<lang>")
    def set_language(lang):
        """Toggle or select active interface language ('km' or 'en')."""
        if lang in LANGUAGES:
            session["lang"] = lang
        
        referrer = request.referrer
        # Ensure referrer is a relative or local URL to prevent open redirect
        if referrer and (referrer.startswith(request.host_url) or referrer.startswith("/")):
            return redirect(referrer)
            
        from flask_login import current_user
        if current_user and current_user.is_authenticated:
            if current_user.has_permission("view_dashboard"):
                return redirect(url_for("dashboard.index"))
            return redirect(url_for("user_home.index"))
        return redirect(url_for("expert_system.diagnose"))

    # ── Error handlers ────────────────────────────────────────────
    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/error.html",
            error_code=403,
            title="Access Denied",
            message="You don't have permission to access this page. If you believe this is a mistake, contact your administrator.",
            icon="bi-shield-x",
            icon_class="forbidden",
        ), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/error.html",
            error_code=404,
            title="Page Not Found",
            message="The page you're looking for doesn't exist or has been moved. Check the URL or head back to the homepage.",
            icon="bi-search",
            icon_class="not-found",
        ), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/error.html",
            error_code=500,
            title="Something Went Wrong",
            message="An unexpected error occurred on our end. Please try again later or contact support if the problem persists.",
            icon="bi-exclamation-octagon",
            icon_class="server-error",
        ), 500

    @app.errorhandler(413)
    def request_too_large(e):
        return render_template("errors/error.html",
            error_code=413,
            title="File Too Large",
            message="រូបភាពដែលបានឡើងផ្ទុករបស់អ្នកធំពេក។ សូមប្រើរូបភាពដែលមានទំហំតូចជាង 50 MB សម្រាប់គ្រប់រូបភាពទាំងអស់ក្នុងការដាក់ស្នើតែមួយ។",
            icon="bi-file-earmark-x",
            icon_class="server-error",
        ), 413

    @app.route("/")
    def home():
        from flask_login import current_user
        if current_user.is_authenticated:
            if current_user.has_permission("view_dashboard"):
                return redirect(url_for("dashboard.index"))
            return redirect(url_for("user_home.index"))
        return redirect(url_for("expert_system.diagnose", step="1"))


    with app.app_context():
        from app.models.role import RoleTable
        from app.models.permission import PermissionTable
        from app.models.expert_system import Category, Symptom, Disease, Rule, Case
        from app.models.audit_log import AuditLog
        from app.models.doctor_application import DoctorApplication
        from app.models.notification import Notification

        if os.environ.get("RESET_DB", "0") == "1":
            db.drop_all()

        db.create_all()

        from utils.db_migrate import migrate_schema, migrate_create_tables
        migrate_schema()
        migrate_create_tables()

        if not UserTable.query.first():
            from app.services.seed_service import seed_all
            seed_all()
        else:
            from app.services.seed_service import upgrade_permissions
            upgrade_permissions()

    return app
