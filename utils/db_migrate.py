"""Lightweight schema migrations for existing PostgreSQL databases."""
from sqlalchemy import inspect, text
from extensions import db


def _column_exists(inspector, table: str, column: str) -> bool:
    return column in {c["name"] for c in inspector.get_columns(table)}


def migrate_schema() -> None:
    """Add new Tier-1 columns to existing tables without dropping data."""
    inspector = inspect(db.engine)
    alterations = []

    if inspector.has_table("tbl_symptoms") and not _column_exists(inspector, "tbl_symptoms", "category_id"):
        alterations.append(
            "ALTER TABLE tbl_symptoms ADD COLUMN category_id INTEGER REFERENCES tbl_categories(id)"
        )

    disease_cols = {
        "prevention": "VARCHAR(500)",
        "severity": "VARCHAR(50)",
        "is_contagious": "BOOLEAN DEFAULT FALSE",
    }
    if inspector.has_table("tbl_diseases"):
        for col, col_type in disease_cols.items():
            if not _column_exists(inspector, "tbl_diseases", col):
                alterations.append(f"ALTER TABLE tbl_diseases ADD COLUMN {col} {col_type}")

    case_cols = {
        "flock_size": "INTEGER",
        "bird_age": "VARCHAR(80)",
        "breed": "VARCHAR(80)",
        "location": "VARCHAR(120)",
        "notes": "TEXT",
        "status": "VARCHAR(20) DEFAULT 'pending'",
        "reviewed_by_id": "INTEGER REFERENCES tbl_users(id)",
        "reviewed_at": "TIMESTAMP",
        "doctor_notes": "TEXT",
        "override_disease_id": "INTEGER REFERENCES tbl_diseases(id)",
        "feedback_rating": "INTEGER",
        "feedback_text": "TEXT",
        "feedback_at": "TIMESTAMP",
    }
    if inspector.has_table("tbl_cases"):
        for col, col_type in case_cols.items():
            if not _column_exists(inspector, "tbl_cases", col):
                alterations.append(f"ALTER TABLE tbl_cases ADD COLUMN {col} {col_type}")

    for sql in alterations:
        db.session.execute(text(sql))
    if alterations:
        db.session.commit()
