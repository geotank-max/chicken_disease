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

    # ── tbl_users: email verification & password reset ──────────
    user_new_cols = {
        "email_verified": "BOOLEAN DEFAULT FALSE NOT NULL",
        "email_verify_token_hash": "VARCHAR(255)",
        "email_verify_token_expires": "TIMESTAMP",
        "reset_token_hash": "VARCHAR(255)",
        "reset_token_expires": "TIMESTAMP",
        "oauth_provider": "VARCHAR(50)",
        "oauth_id": "VARCHAR(255)",
    }
    if inspector.has_table("tbl_users"):
        for col, col_type in user_new_cols.items():
            if not _column_exists(inspector, "tbl_users", col):
                alterations.append(f"ALTER TABLE tbl_users ADD COLUMN {col} {col_type}")
        # Make password_hash nullable for OAuth users
        alterations.append(
            "ALTER TABLE tbl_users ALTER COLUMN password_hash DROP NOT NULL"
        )

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
        "follow_up_status": "VARCHAR(30) DEFAULT 'none' NOT NULL",
        "follow_up_updated_at": "TIMESTAMP",
        "treatment_checked_steps": "TEXT",
        # Extended diagnosis context (all optional)
        "sick_bird_count": "INTEGER",
        "dead_bird_count": "INTEGER",
        "symptom_duration": "VARCHAR(80)",
        "vaccination_status": "VARCHAR(20)",
        "egg_production_drop": "INTEGER",
        "feed_or_water_changed": "VARCHAR(10)",
        "new_birds_added": "VARCHAR(10)",
        "nearby_farms_sick": "VARCHAR(10)",
        "coop_condition": "VARCHAR(20)",
        "appetite_level": "VARCHAR(20)",
        "water_intake_level": "VARCHAR(20)",
    }
    if inspector.has_table("tbl_cases"):
        for col, col_type in case_cols.items():
            if not _column_exists(inspector, "tbl_cases", col):
                alterations.append(f"ALTER TABLE tbl_cases ADD COLUMN {col} {col_type}")

    for sql in alterations:
        db.session.execute(text(sql))
    if alterations:
        db.session.commit()


def _table_exists(inspector, table: str) -> bool:
    return inspector.has_table(table)


def migrate_create_tables() -> None:
    """Create brand-new tables that did not exist in the original schema.

    Each block is fully idempotent: it checks for the table before issuing
    any DDL, so re-running on an already-migrated database is safe.
    """
    inspector = inspect(db.engine)

    # ── tbl_case_photos ─────────────────────────────────────────────────────
    # Stores symptom photos uploaded by farmers when submitting a diagnosis case.
    if not _table_exists(inspector, "tbl_case_photos"):
        db.session.execute(text("""
            CREATE TABLE tbl_case_photos (
                id               SERIAL PRIMARY KEY,
                case_id          INTEGER NOT NULL
                                     REFERENCES tbl_cases(id) ON DELETE CASCADE,
                file_path        VARCHAR(255) NOT NULL,
                original_filename VARCHAR(255),
                category         VARCHAR(50)  NOT NULL DEFAULT 'other',
                uploaded_at      TIMESTAMP    NOT NULL DEFAULT NOW()
            )
        """))
        db.session.execute(text(
            "CREATE INDEX ix_tbl_case_photos_case_id ON tbl_case_photos (case_id)"
        ))
        db.session.commit()

    # ── tbl_case_messages ───────────────────────────────────────────────────
    # Doctor <-> farmer follow-up comment thread, one row per message on a case.
    if not _table_exists(inspector, "tbl_case_messages"):
        db.session.execute(text("""
            CREATE TABLE tbl_case_messages (
                id          SERIAL PRIMARY KEY,
                case_id     INTEGER NOT NULL
                                REFERENCES tbl_cases(id) ON DELETE CASCADE,
                author_id   INTEGER NOT NULL
                                REFERENCES tbl_users(id),
                body        TEXT      NOT NULL,
                is_doctor   BOOLEAN   NOT NULL DEFAULT FALSE,
                created_at  TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        db.session.execute(text(
            "CREATE INDEX ix_tbl_case_messages_case_id ON tbl_case_messages (case_id)"
        ))
        db.session.commit()

    # ── tbl_treatment_steps ─────────────────────────────────────────────────
    # Doctor/admin-authored, ordered treatment steps belonging to a disease.
    if not _table_exists(inspector, "tbl_treatment_steps"):
        db.session.execute(text("""
            CREATE TABLE tbl_treatment_steps (
                id             SERIAL PRIMARY KEY,
                disease_id     INTEGER NOT NULL
                                   REFERENCES tbl_diseases(id) ON DELETE CASCADE,
                position       INTEGER   NOT NULL DEFAULT 0,
                text           VARCHAR(500) NOT NULL,
                note           VARCHAR(500),
                created_by_id  INTEGER REFERENCES tbl_users(id),
                created_at     TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        db.session.execute(text(
            "CREATE INDEX ix_tbl_treatment_steps_disease_id ON tbl_treatment_steps (disease_id)"
        ))
        db.session.commit()

    # ── tbl_case_treatment_progress ─────────────────────────────────────────
    # Per-case completion state for a structured treatment step.
    if not _table_exists(inspector, "tbl_case_treatment_progress"):
        db.session.execute(text("""
            CREATE TABLE tbl_case_treatment_progress (
                id           SERIAL PRIMARY KEY,
                case_id      INTEGER NOT NULL
                                 REFERENCES tbl_cases(id) ON DELETE CASCADE,
                step_id      INTEGER NOT NULL
                                 REFERENCES tbl_treatment_steps(id) ON DELETE CASCADE,
                done         BOOLEAN   NOT NULL DEFAULT FALSE,
                completed_at TIMESTAMP,
                CONSTRAINT uq_case_step UNIQUE (case_id, step_id)
            )
        """))
        db.session.execute(text(
            "CREATE INDEX ix_tbl_case_treatment_progress_case_id ON tbl_case_treatment_progress (case_id)"
        ))
        db.session.commit()
