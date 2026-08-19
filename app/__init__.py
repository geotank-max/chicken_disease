# app/__init__.py
import os
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, csrf, login_manager
from app.models.user import UserTable


def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "សូមចូលប្រើប្រាស់មុន។"
    login_manager.login_message_category = "warning"

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

    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    with app.app_context():
        from app.models.role import RoleTable
        from app.models.permission import PermissionTable
        from app.models.expert_system import Category, Symptom, Disease, Rule, Case
        from app.models.audit_log import AuditLog
        from app.models.doctor_application import DoctorApplication

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

    return app
