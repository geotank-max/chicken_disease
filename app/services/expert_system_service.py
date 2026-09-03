# app/services/expert_system_service.py
from datetime import datetime
from typing import List, Optional
from extensions import db
from app.models.expert_system import (
    Category, Symptom, Disease, Rule, Case, CaseMessage,
    TreatmentStep, CaseTreatmentProgress, CaseDiagnosis,
    CASE_STATUS_CONFIRMED, CASE_STATUS_REJECTED, CASE_STATUS_PENDING,
    FOLLOWUP_STATUSES,
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
        disease_id = disease.id

        # 1. Unlink any cases where this disease was recorded as primary or override diagnosis
        Case.query.filter_by(disease_id=disease_id).update({"disease_id": None}, synchronize_session=False)
        Case.query.filter_by(override_disease_id=disease_id).update({"override_disease_id": None}, synchronize_session=False)

        # 2. Delete all inference outcome records (tbl_case_diagnoses) referencing this disease
        CaseDiagnosis.query.filter_by(disease_id=disease_id).delete(synchronize_session=False)

        # 3. Clean up CaseTreatmentProgress for any treatment steps belonging to this disease
        step_ids = [step.id for step in disease.treatment_steps]
        if step_ids:
            CaseTreatmentProgress.query.filter(
                CaseTreatmentProgress.step_id.in_(step_ids)
            ).delete(synchronize_session=False)

        # 4. If any other CaseDiagnosis references rules belonging to this disease, unlink rule_id
        rule_ids = [rule.id for rule in disease.rules]
        if rule_ids:
            CaseDiagnosis.query.filter(
                CaseDiagnosis.rule_id.in_(rule_ids)
            ).update({"rule_id": None}, synchronize_session=False)

        # 5. Delete the disease itself (SQLAlchemy cascades will delete rules, rules_symptoms, and treatment_steps)
        db.session.delete(disease)
        db.session.commit()


class TreatmentStepService:
    """CRUD + ordering for doctor/admin-authored treatment steps (Option A)."""

    @staticmethod
    def get_by_id(step_id: int) -> Optional[TreatmentStep]:
        return TreatmentStep.query.get(step_id)

    @staticmethod
    def list_for_disease(disease_id: int) -> List[TreatmentStep]:
        return (
            TreatmentStep.query
            .filter_by(disease_id=disease_id)
            .order_by(TreatmentStep.position.asc(), TreatmentStep.id.asc())
            .all()
        )

    @staticmethod
    def add(disease: Disease, text: str, note: str = "", created_by_id: int | None = None) -> TreatmentStep:
        existing = TreatmentStepService.list_for_disease(disease.id)
        next_pos = (existing[-1].position + 1) if existing else 0
        step = TreatmentStep(
            disease_id=disease.id,
            position=next_pos,
            text=text.strip(),
            note=(note or "").strip() or None,
            created_by_id=created_by_id,
        )
        db.session.add(step)
        db.session.commit()
        return step

    @staticmethod
    def update(step: TreatmentStep, text: str, note: str = "") -> TreatmentStep:
        step.text = text.strip()
        step.note = (note or "").strip() or None
        db.session.commit()
        return step

    @staticmethod
    def delete(step: TreatmentStep) -> None:
        db.session.delete(step)
        db.session.commit()
        TreatmentStepService._renumber(step.disease_id)

    @staticmethod
    def move(step: TreatmentStep, direction: str) -> None:
        """Swap a step with its neighbour above ('up') or below ('down')."""
        steps = TreatmentStepService.list_for_disease(step.disease_id)
        idx = next((i for i, s in enumerate(steps) if s.id == step.id), None)
        if idx is None:
            return
        swap_with = None
        if direction == "up" and idx > 0:
            swap_with = steps[idx - 1]
        elif direction == "down" and idx < len(steps) - 1:
            swap_with = steps[idx + 1]
        if swap_with is None:
            return
        step.position, swap_with.position = swap_with.position, step.position
        db.session.commit()

    @staticmethod
    def _renumber(disease_id: int) -> None:
        """Re-pack positions to 0..n-1 after a delete."""
        steps = TreatmentStepService.list_for_disease(disease_id)
        for i, s in enumerate(steps):
            s.position = i
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

    @staticmethod
    def set_follow_up_status(case: Case, status: str) -> Case:
        """Update the recovery/outcome follow-up status of a case."""
        if status not in FOLLOWUP_STATUSES:
            raise ValueError(f"Invalid follow-up status: {status}")
        case.follow_up_status = status
        case.follow_up_updated_at = datetime.utcnow()
        db.session.commit()
        return case

    @staticmethod
    def toggle_treatment_step(case: Case, step_key: int, done: bool) -> Case:
        """Mark a treatment checklist step done/undone for this case.

        When the diagnosed disease has structured steps, `step_key` is a
        TreatmentStep id and state is stored in CaseTreatmentProgress. Otherwise
        `step_key` is a positional index into the derived-text checklist and
        state is stored in the Case.treatment_checked_steps JSON (Option B).
        """
        if case.uses_structured_steps:
            valid_ids = {s.id for s in case.final_disease.treatment_steps}
            if step_key not in valid_ids:
                raise ValueError(f"Unknown treatment step id: {step_key}")
            row = next(
                (p for p in case.treatment_progress_rows if p.step_id == step_key),
                None,
            )
            if row is None:
                row = CaseTreatmentProgress(case_id=case.id, step_id=step_key)
                db.session.add(row)
            row.done = done
            row.completed_at = datetime.utcnow() if done else None
            db.session.commit()
            return case

        # Fallback: Option B index-based JSON state.
        import json as _json
        checked = set(case._checked_step_set)
        total = len(case.treatment_steps)
        if step_key < 0 or step_key >= total:
            raise ValueError(f"Step index out of range: {step_key}")
        if done:
            checked.add(step_key)
        else:
            checked.discard(step_key)
        case.treatment_checked_steps = _json.dumps(sorted(checked))
        db.session.commit()
        return case


class CaseMessageService:
    @staticmethod
    def add_message(case: Case, author_id: int, body: str, is_doctor: bool = False) -> CaseMessage:
        """Append a comment/question to a case thread."""
        msg = CaseMessage(
            case_id=case.id,
            author_id=author_id,
            body=body,
            is_doctor=is_doctor,
        )
        db.session.add(msg)
        db.session.commit()
        return msg
