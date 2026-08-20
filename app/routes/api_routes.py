# app/routes/api_routes.py
"""
Public JSON API endpoints for PWA/offline support.
"""
from flask import Blueprint, jsonify
from flask_login import login_required
from app.models.expert_system import Category, Symptom, Disease, Rule

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/knowledge-base")
@login_required
def knowledge_base():
    """
    Returns the full knowledge base (symptoms, diseases, rules, categories)
    as JSON so the client can cache it in IndexedDB for offline diagnosis.
    """
    categories = Category.query.order_by(Category.name).all()
    symptoms = Symptom.query.order_by(Symptom.name).all()
    diseases = Disease.query.order_by(Disease.name).all()
    rules = Rule.query.all()

    return jsonify({
        "categories": [
            {"id": c.id, "name": c.name, "description": c.description}
            for c in categories
        ],
        "symptoms": [
            {
                "id": s.id,
                "name": s.name,
                "description": s.description,
                "category_id": s.category_id,
                "category_name": s.category.name if s.category else None,
            }
            for s in symptoms
        ],
        "diseases": [
            {
                "id": d.id,
                "name": d.name,
                "description": d.description,
                "treatment": d.treatment,
                "prevention": d.prevention,
                "severity": d.severity,
                "is_contagious": d.is_contagious,
                "category_name": d.category.name if d.category else None,
            }
            for d in diseases
        ],
        "rules": [
            {
                "id": r.id,
                "title": r.title,
                "disease_id": r.disease_id,
                "confidence": r.confidence,
                "priority": r.priority,
                "symptom_ids": [s.id for s in r.symptoms],
            }
            for r in rules
        ],
    })
