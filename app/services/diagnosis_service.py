from app.models.expert_system import Symptom, Rule, Case, CASE_STATUS_PENDING
from flask_babel import gettext as _
from extensions import db

MIN_CONFIDENCE_THRESHOLD = 30.0


class DiagnosisService:
    @staticmethod
    def get_all_symptoms():
        return Symptom.query.order_by(Symptom.name.asc()).all()

    @staticmethod
    def get_symptoms_grouped():
        symptoms = DiagnosisService.get_all_symptoms()
        grouped: dict[str, list] = {}
        for symptom in symptoms:
            key = symptom.category.name if symptom.category else _("Other")
            grouped.setdefault(key, []).append(symptom)
        return grouped

    @staticmethod
    def get_all_rules():
        return Rule.query.all()

    @staticmethod
    def run_inference(selected_symptom_ids):
        all_rules = Rule.query.all()
        results = []
        input_ids = set(selected_symptom_ids)

        for rule in all_rules:
            rule_symptom_ids = {s.id for s in rule.symptoms}
            if not rule_symptom_ids:
                continue

            matches = input_ids.intersection(rule_symptom_ids)
            if not matches:
                continue

            match_ratio = len(matches) / len(rule_symptom_ids)
            weighted = match_ratio * (rule.confidence or 100.0)
            confidence = min(round(weighted, 2), 100.0)

            if confidence < MIN_CONFIDENCE_THRESHOLD:
                continue

            results.append({
                "disease": rule.disease,
                "confidence": confidence,
                "matched_count": len(matches),
                "required_count": len(rule_symptom_ids),
                "treatment": rule.disease.treatment,
                "rule": rule,
            })

        return sorted(
            results,
            key=lambda x: (-x["confidence"], x["rule"].priority, -x["matched_count"]),
        )

    @staticmethod
    def record_case(user_id, selected_symptom_ids, top_result, flock_data=None):
        flock_data = flock_data or {}
        case = Case(
            user_id=user_id,
            disease_id=top_result["disease"].id if top_result else None,
            confidence=top_result["confidence"] if top_result else None,
            flock_size=flock_data.get("flock_size") or None,
            bird_age=flock_data.get("bird_age") or None,
            breed=flock_data.get("breed") or None,
            location=flock_data.get("location") or None,
            notes=flock_data.get("notes") or None,
            status=CASE_STATUS_PENDING,
        )
        if selected_symptom_ids:
            case.symptoms = Symptom.query.filter(Symptom.id.in_(selected_symptom_ids)).all()
        db.session.add(case)
        db.session.commit()
        return case
