# app/models/__init__.py
from .user import UserTable
from .role import RoleTable
from .permission import PermissionTable
from .expert_system import Category, Symptom, Disease, Rule, Case
from .doctor_application import DoctorApplication
from .notification import Notification
from .vet_clinic import VetClinic

__all__ = [
    "UserTable",
    "RoleTable",
    "PermissionTable",
    "Category",
    "Symptom",
    "Disease",
    "Rule",
    "Case",
    "DoctorApplication",
    "Notification",
    "VetClinic",
]
