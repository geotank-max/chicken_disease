from app.models.expert_system import Symptom, Rule, Case, CaseDiagnosis, CASE_STATUS_PENDING
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
    def build_symptom_index():
        """Return front-end metadata for the Step 2 interactive symptom picker.

        Produces two structures:
          symptoms: [{id, name, description, category}]
          diseases: {disease_name: {"symptoms": set(...), "category": name}}

        Plus a symptom -> related disease map, so the UI can (a) suggest the
        most likely illnesses for the currently selected symptoms and (b) know
        which category each disease belongs to.
        """
        rules = Rule.query.all()
        # disease_name -> {"symptoms": {ids}, "category": name, "severity": str}
        diseases: dict[str, dict] = {}
        # symptom_id -> set(disease_name)
        symptom_to_diseases: dict[int, set] = {}

        for rule in rules:
            disease = rule.disease
            if disease is None:
                continue
            entry = diseases.setdefault(disease.name, {
                "symptoms": set(),
                "category": disease.category.name if disease.category else "",
                "severity": disease.severity or "",
                "description": disease.description or "",
            })
            for symptom in rule.symptoms:
                entry["symptoms"].add(symptom.id)
                symptom_to_diseases.setdefault(symptom.id, set()).add(disease.name)

        return diseases, symptom_to_diseases

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
    def record_case(user_id, selected_symptom_ids, top_result=None, flock_data=None, diagnosis_results=None):
        flock_data = flock_data or {}

        # Resolve top_result and diagnosis_results
        if diagnosis_results and not top_result:
            top_result = diagnosis_results[0]
        elif top_result and not diagnosis_results:
            diagnosis_results = [top_result]

        top_disease = top_result.get("disease") if top_result else None
        top_disease_id = top_disease.id if (top_disease and hasattr(top_disease, "id")) else top_disease
        top_confidence = top_result.get("confidence") if top_result else None

        case = Case(
            user_id=user_id,
            disease_id=top_disease_id,
            confidence=top_confidence,
            flock_size=flock_data.get("flock_size") or None,
            bird_age=flock_data.get("bird_age") or None,
            breed=flock_data.get("breed") or None,
            location=flock_data.get("location") or None,
            # Structured geographic and farm context
            province=flock_data.get("province") or None,
            district=flock_data.get("district") or None,
            commune=flock_data.get("commune") or None,
            latitude=flock_data.get("latitude"),
            longitude=flock_data.get("longitude"),
            farm_type=flock_data.get("farm_type") or None,
            farm_scale=flock_data.get("farm_scale") or None,
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
        db.session.flush()

        if diagnosis_results:
            for rank_idx, result in enumerate(diagnosis_results, start=1):
                disease_obj = result.get("disease")
                disease_id = disease_obj.id if (disease_obj and hasattr(disease_obj, "id")) else disease_obj
                rule_obj = result.get("rule")
                rule_id = rule_obj.id if (rule_obj and hasattr(rule_obj, "id")) else rule_obj

                if disease_id:
                    case_diag = CaseDiagnosis(
                        case_id=case.id,
                        disease_id=disease_id,
                        rule_id=rule_id,
                        confidence=float(result.get("confidence", 0.0)),
                        matched_symptom_count=int(result.get("matched_count", 0)),
                        required_symptom_count=int(result.get("required_count", 0)),
                        rank=rank_idx,
                    )
                    db.session.add(case_diag)

        db.session.commit()
        return case
