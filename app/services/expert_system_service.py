# app/services/expert_system_service.py
from datetime import datetime
from typing import List, Optional
from extensions import db
from app.models.expert_system import (
    Category, Symptom, Disease, Rule, Case,
    CASE_STATUS_CONFIRMED, CASE_STATUS_REJECTED, CASE_STATUS_PENDING,
)


class CategoryService:
    @staticmethod
    def get_all() -> List[Category]:
        return Category.query.order_by(Category.name.asc()).all()

    @staticmethod
    def get_by_id(category_id: int) -> Optional[Category]:
        return Category.query.get(category_id)

    @staticmethod
    def create(data: dict) -> Category:
        category = Category(
            name=data["name"],
            description=data.get("description") or "",
        )
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def update(category: Category, data: dict) -> Category:
        category.name = data["name"]
        category.description = data.get("description") or ""
        db.session.commit()
        return category

    @staticmethod
    def delete(category: Category) -> None:
        db.session.delete(category)
        db.session.commit()


class SymptomService:
    @staticmethod
    def get_all() -> List[Symptom]:
        return Symptom.query.order_by(Symptom.name.asc()).all()

    @staticmethod
    def get_by_id(symptom_id: int) -> Optional[Symptom]:
        return Symptom.query.get(symptom_id)

    @staticmethod
    def create(data: dict) -> Symptom:
        category_id = data.get("category_id") or None
        if category_id == 0:
            category_id = None
        symptom = Symptom(
            name=data["name"],
            description=data.get("description") or "",
            category_id=category_id,
        )
        db.session.add(symptom)
        db.session.commit()
        return symptom

    @staticmethod
    def update(symptom: Symptom, data: dict) -> Symptom:
        category_id = data.get("category_id") or None
        if category_id == 0:
            category_id = None
        symptom.name = data["name"]
        symptom.description = data.get("description") or ""
        symptom.category_id = category_id
        db.session.commit()
        return symptom

    @staticmethod
    def delete(symptom: Symptom) -> None:
        db.session.delete(symptom)
        db.session.commit()


class DiseaseService:
    @staticmethod
    def get_all() -> List[Disease]:
        return Disease.query.order_by(Disease.name.asc()).all()

    @staticmethod
    def get_by_id(disease_id: int) -> Optional[Disease]:
        return Disease.query.get(disease_id)

    @staticmethod
    def create(data: dict) -> Disease:
        category_id = data.get("category_id") or None
        if category_id == 0:
            category_id = None
        disease = Disease(
            name=data["name"],
            description=data["description"],
            treatment=data["treatment"],
            prevention=data.get("prevention") or "",
            severity=data.get("severity") or "",
            is_contagious=bool(data.get("is_contagious")),
            category_id=category_id,
        )
        db.session.add(disease)
        db.session.commit()
        return disease

    @staticmethod
    def update(disease: Disease, data: dict) -> Disease:
        category_id = data.get("category_id") or None
        if category_id == 0:
            category_id = None
        disease.name = data["name"]
        disease.description = data["description"]
        disease.treatment = data["treatment"]
        disease.prevention = data.get("prevention") or ""
        disease.severity = data.get("severity") or ""
        disease.is_contagious = bool(data.get("is_contagious"))
        disease.category_id = category_id
        db.session.commit()
        return disease

    @staticmethod
    def delete(disease: Disease) -> None:
        db.session.delete(disease)
        db.session.commit()


class RuleService:
    @staticmethod
    def get_all() -> List[Rule]:
        return Rule.query.order_by(Rule.priority.asc(), Rule.id.asc()).all()

    @staticmethod
    def get_by_id(rule_id: int) -> Optional[Rule]:
        return Rule.query.get(rule_id)

    @staticmethod
    def create(data: dict, symptom_ids: List[int]) -> Rule:
        rule = Rule(
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            confidence=data["confidence"],
            disease_id=data["disease_id"],
        )
        if symptom_ids:
            # Ensure symptom_ids are integers
            symptom_ids = [int(sid) for sid in symptom_ids]
            rule.symptoms = Symptom.query.filter(Symptom.id.in_(symptom_ids)).all()
        db.session.add(rule)
        db.session.commit()
        return rule

    @staticmethod
    def update(rule: Rule, data: dict, symptom_ids: List[int]) -> Rule:
        rule.title = data["title"]
        rule.description = data["description"]
        rule.priority = data["priority"]
        rule.confidence = data["confidence"]
        rule.disease_id = data["disease_id"]
        if symptom_ids:
             # Ensure symptom_ids are integers
            symptom_ids = [int(sid) for sid in symptom_ids]
            rule.symptoms = Symptom.query.filter(Symptom.id.in_(symptom_ids)).all()
        else:
            rule.symptoms = []
        db.session.commit()
        return rule

    @staticmethod
    def delete(rule: Rule) -> None:
        db.session.delete(rule)
        db.session.commit()


class CaseService:
    @staticmethod
    def get_all() -> List[Case]:
        return Case.query.order_by(Case.created_at.desc()).all()

    @staticmethod
    def get_paginated(page: int = 1, per_page: int = 10, user_id: int | None = None,
                      status: str | None = None, disease_id: int | None = None,
                      date_from: str | None = None, date_to: str | None = None):
        """Return paginated and filtered cases."""
        from datetime import datetime
        query = Case.query

        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        if disease_id:
            query = query.filter_by(disease_id=disease_id)
        if date_from:
            try:
                dt = datetime.strptime(date_from, "%Y-%m-%d")
                query = query.filter(Case.created_at >= dt)
            except ValueError:
                pass
        if date_to:
            try:
                dt = datetime.strptime(date_to, "%Y-%m-%d")
                dt = dt.replace(hour=23, minute=59, second=59)
                query = query.filter(Case.created_at <= dt)
            except ValueError:
                pass

        return query.order_by(Case.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_by_user(user_id: int) -> List[Case]:
        return Case.query.filter_by(user_id=user_id).order_by(Case.created_at.desc()).all()

    @staticmethod
    def get_by_id(case_id: int) -> Optional[Case]:
        return Case.query.get(case_id)

    @staticmethod
    def get_pending() -> List[Case]:
        return Case.query.filter_by(status=CASE_STATUS_PENDING).order_by(Case.created_at.desc()).all()

    @staticmethod
    def review_case(case: Case, reviewer_id: int, action: str, doctor_notes: str = "", override_disease_id: int | None = None) -> Case:
        case.reviewed_by_id = reviewer_id
        case.reviewed_at = datetime.utcnow()
        case.doctor_notes = doctor_notes or None

        if action == "confirm":
            case.status = CASE_STATUS_CONFIRMED
            case.override_disease_id = override_disease_id or None
        elif action == "reject":
            case.status = CASE_STATUS_REJECTED
            case.override_disease_id = None
        else:
            case.status = CASE_STATUS_PENDING

        db.session.commit()
        return case

    @staticmethod
    def submit_feedback(case: Case, rating: int, text: str = "") -> Case:
        case.feedback_rating = rating
        case.feedback_text = text or None
        case.feedback_at = datetime.utcnow()
        db.session.commit()
        return case
