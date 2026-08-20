# app/__init__.py
import os
from flask import Flask, redirect, url_for, request, session
from config import Config
from extensions import db, csrf, login_manager, babel
from app.models.user import UserTable


def get_locale():
    # 1. User explicitly chose a language (stored in session)
    lang = session.get("lang")
    if lang and lang in Config.LANGUAGES:
        return lang
    # 2. Best match from Accept-Language header
    return request.accept_languages.best_match(Config.LANGUAGES, default="en")


def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    # Use lazy_gettext so the message is translated at request time
    from flask_babel import lazy_gettext as _l
    login_manager.login_message = _l("Please log in first.")

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
    app.register_blueprint(audit_bp)
    app.register_blueprint(dashboard_bp)

    from app.routes.doctor_application_routes import doctor_app_bp
    app.register_blueprint(doctor_app_bp)

    from app.routes.notification_routes import notification_bp
    app.register_blueprint(notification_bp)

    from app.routes.api_routes import api_bp
    app.register_blueprint(api_bp)

    from app.routes.vet_routes import vets_bp
    app.register_blueprint(vets_bp)

    # Context processor: inject notification badges into all templates
    @app.context_processor
    def inject_badges():
        from flask_login import current_user
        badges = {}
        if current_user and hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            from app.services.notification_service import NotificationService
            badges["notif_count"] = NotificationService.get_unread_count(current_user.id)
            if current_user.has_role("Admin"):
                badges["pending_applications"] = NotificationService.get_pending_applications_count()
                badges["pending_cases"] = NotificationService.get_pending_cases_count()
            elif current_user.has_role("Doctor"):
                badges["pending_cases"] = NotificationService.get_pending_cases_count()
        return badges

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    @app.route("/sw.js")
    def service_worker():
        """Serve service worker from root so it can control the whole origin."""
        from flask import send_from_directory
        return send_from_directory(
            app.static_folder, "sw.js",
            mimetype="application/javascript",
        )

    @app.route("/set-language/<lang>")
    def set_language(lang):
        if lang in app.config["LANGUAGES"]:
            session["lang"] = lang
        return redirect(request.referrer or url_for("home"))

    # Inject current locale and available languages into all templates
    @app.context_processor
    def inject_locale():
        return {
            "current_lang": get_locale(),
            "available_languages": app.config["LANGUAGES"],
        }

    with app.app_context():
        from app.models.role import RoleTable
        from app.models.permission import PermissionTable
        from app.models.expert_system import Category, Symptom, Disease, Rule, Case
        from app.models.audit_log import AuditLog
        from app.models.doctor_application import DoctorApplication
        from app.models.notification import Notification
        from app.models.vet_clinic import VetClinic

        if os.environ.get("RESET_DB", "0") == "1":
            db.drop_all()

        db.create_all()

        from utils.db_migrate import migrate_schema
        migrate_schema()

        if not UserTable.query.first():
            from app.services.seed_service import seed_all
            seed_all()
        else:
            from app.services.seed_service import upgrade_permissions
            upgrade_permissions()

        # Seed vet clinics (idempotent)
        from app.services.vet_seed_service import seed_vet_clinics
        seed_vet_clinics()

    return app
