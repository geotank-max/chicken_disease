# app/models/user.py
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db
from app.models.associations import tbl_user_roles


class UserTable(UserMixin, db.Model):
    __tablename__ = "tbl_users"
    
    id = db.Column(db.Integer, db.Sequence('seq_users_id'), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Email verification fields
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verify_token_hash = db.Column(db.String(255), nullable=True)
    email_verify_token_expires = db.Column(db.DateTime, nullable=True)
    
    # Password reset fields
    reset_token_hash = db.Column(db.String(255), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # NOTE: matches RoleTable.users
    roles = db.relationship("RoleTable", secondary=tbl_user_roles, back_populates="users")
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
    
    # ── Token helpers ─────────────────────────────────────────────
    
    def generate_email_verify_token(self) -> str:
        """Generate a secure email verification token. Returns the raw token (to email)."""
        raw_token = secrets.token_urlsafe(32)
        self.email_verify_token_hash = generate_password_hash(raw_token)
        self.email_verify_token_expires = datetime.utcnow() + timedelta(hours=24)
        return raw_token
    
    def verify_email_token(self, raw_token: str) -> bool:
        """Verify a raw email token against the stored hash. Single-use."""
        if not self.email_verify_token_hash:
            return False
        if self.email_verify_token_expires and datetime.utcnow() > self.email_verify_token_expires:
            return False
        if not check_password_hash(self.email_verify_token_hash, raw_token):
            return False
        # Consume the token (single-use)
        self.email_verified = True
        self.email_verify_token_hash = None
        self.email_verify_token_expires = None
        return True
    
    def generate_reset_token(self) -> str:
        """Generate a secure password-reset token. Returns the raw token (to email)."""
        raw_token = secrets.token_urlsafe(32)
        self.reset_token_hash = generate_password_hash(raw_token)
        self.reset_token_expires = datetime.utcnow() + timedelta(minutes=30)
        return raw_token
    
    def verify_reset_token(self, raw_token: str) -> bool:
        """Verify a raw reset token against the stored hash. Single-use."""
        if not self.reset_token_hash:
            return False
        if self.reset_token_expires and datetime.utcnow() > self.reset_token_expires:
            return False
        if not check_password_hash(self.reset_token_hash, raw_token):
            return False
        # Consume the token (single-use)
        self.reset_token_hash = None
        self.reset_token_expires = None
        return True
    
    # ── Role / Permission helpers ─────────────────────────────────
    
    def has_role(self, role_name: str) -> bool:
        return any(role.name == role_name for role in self.roles)
    
    def get_permission_codes(self) -> set[str]:
        return {perm.code for role in self.roles for perm in role.permissions}
    
    def has_permission(self, permission_code: str) -> bool:
        return permission_code in self.get_permission_codes()
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    
        
