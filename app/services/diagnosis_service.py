from app.models.expert_system import Symptom, Rule, Case, CASE_STATUS_PENDING
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
            key = symptom.category.name if symptom.category else "ផ្សេងៗ"
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
            # Extended diagnosis context (all optional)
            sick_bird_count=flock_data.get("sick_bird_count"),
            dead_bird_count=flock_data.get("dead_bird_count"),
            symptom_duration=flock_data.get("symptom_duration") or None,
            vaccination_status=flock_data.get("vaccination_status") or None,
            egg_production_drop=flock_data.get("egg_production_drop"),
            feed_or_water_changed=flock_data.get("feed_or_water_changed") or None,
            new_birds_added=flock_data.get("new_birds_added") or None,
            nearby_farms_sick=flock_data.get("nearby_farms_sick") or None,
            coop_condition=flock_data.get("coop_condition") or None,
            appetite_level=flock_data.get("appetite_level") or None,
            water_intake_level=flock_data.get("water_intake_level") or None,
            status=CASE_STATUS_PENDING,
        )
        if selected_symptom_ids:
            case.symptoms = Symptom.query.filter(Symptom.id.in_(selected_symptom_ids)).all()
        db.session.add(case)
        db.session.commit()
        return case
