# app/services/user_service.py
from typing import List, Optional
from app.models.user import UserTable
from app.models.role import RoleTable
from extensions import db

class UserService:
    @staticmethod
    def get_user_all() -> List[UserTable]:
        return UserTable.query.order_by(UserTable.id.desc()).all()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[UserTable]:
        return UserTable.query.get(user_id)
    
    @staticmethod
    def create_user(
        data: dict,
        password: str,
        role_id: Optional[int] = None,
    ) -> UserTable:
        user = UserTable(
            username=data["username"],
            email=data["email"],
            full_name=data["full_name"],
            is_active=data.get("is_active", True),
        )
        user.set_password(password)
        
        if role_id:
            role = db.session.get(RoleTable, role_id)
            if role:
                user.roles = [role]
                
        db.session.add(user)
        db.session.commit()
        return user
        
    @staticmethod
    def update_user(
        user: UserTable,
        data: dict,
        password: Optional[str] = None,
        role_id: Optional[int] = None,
    ) -> UserTable:
        user.username = data["username"]
        user.email = data["email"]
        user.full_name = data["full_name"]
        user.is_active = data.get("is_active", True)
        
        if password:
            user.set_password(password)
        
        if role_id:
            role = db.session.get(RoleTable, role_id)
            if role:
                user.roles = [role]
                
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user: UserTable) -> None:
        from app.models.expert_system import Case, CaseMessage, TreatmentStep
        from app.models.audit_log import AuditLog
        from app.models.notification import Notification
        from app.models.doctor_application import DoctorApplication
        from app.models.vet_clinic import VetClinic

        user_id = user.id

        try:
            # Delete messages authored by this user
            CaseMessage.query.filter_by(author_id=user_id).delete(synchronize_session=False)

            # Nullify treatment steps created by this user
            TreatmentStep.query.filter_by(created_by_id=user_id).update({"created_by_id": None}, synchronize_session=False)

            # Remove notifications belonging to the user
            for n in Notification.query.filter_by(user_id=user_id).all():
                db.session.delete(n)

            # Nullify audit log references (preserve history)
            AuditLog.query.filter_by(user_id=user_id).update({"user_id": None}, synchronize_session=False)

            # Nullify case.reviewed_by_id where this user reviewed
            Case.query.filter_by(reviewed_by_id=user_id).update({"reviewed_by_id": None}, synchronize_session=False)

            # Delete cases owned by this user
            owned_cases = Case.query.filter_by(user_id=user_id).all()
            for case in owned_cases:
                case.symptoms = []
                db.session.delete(case)

            # Delete doctor applications by this user
            for app in DoctorApplication.query.filter_by(user_id=user_id).all():
                db.session.delete(app)

            # Nullify reviewed_by on applications reviewed by this user
            DoctorApplication.query.filter_by(reviewed_by_id=user_id).update({"reviewed_by_id": None}, synchronize_session=False)

            # Nullify vet clinic link
            VetClinic.query.filter_by(user_id=user_id).update({"user_id": None}, synchronize_session=False)

            # Clear role associations (M2M)
            user.roles = []

            db.session.flush()
            db.session.delete(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise