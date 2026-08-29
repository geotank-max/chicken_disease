# NU Chicken Disease Diagnosis Expert System (IDNS)

A Flask-based expert system for diagnosing chicken diseases using rule-based inference. Built for veterinarians, doctors, and farmers in Cambodia with Khmer language support.

## Features

- **Diagnosis Wizard** - 3-step process: flock info, symptom selection, results
- **Knowledge Base** - 11 diseases, 30 symptoms, 12 diagnostic rules (Khmer)
- **Doctor Review Workflow** - Pending / Confirmed / Rejected status with override
- **Dashboard** - Chart.js visualizations (cases/day, top diseases, status breakdown)
- **PDF/Print Reports** - Export case reports for farmers and vets
- **CSV Export** - Bulk export filtered cases for analysis
- **Feedback Loop** - Users rate diagnosis accuracy (1-5 stars)
- **Pagination & Filters** - Filter cases by status, disease, date range
- **Role-Based Access** - Admin, Doctor, User roles with granular permissions
- **Audit Logging** - Track all system actions

## Tech Stack

- **Backend:** Flask 2.3, SQLAlchemy, Flask-Login, Flask-WTF
- **Database:** PostgreSQL
- **Frontend:** Bootstrap 5, Chart.js, Jinja2
- **PDF:** xhtml2pdf

---

## Prerequisites

- Python 3.10+
- PostgreSQL 12+

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/geotank-max/chicken_disease.git
cd chicken_disease
git checkout project/refactor
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL database

Open `psql` or pgAdmin and create the database:

```sql
CREATE DATABASE chicken_diagnoses;
```

### 5. Configure environment variables

You can either set environment variables or edit `config.py` directly.

**Option A: Environment variables (recommended)**

```bash
# Windows PowerShell
$env:DB_USER = "postgres"
$env:DB_PASSWORD = "your_password"
$env:DB_HOST = "localhost"
$env:DB_PORT = "5432"
$env:DB_NAME = "chicken_diagnoses"
$env:SECRET_KEY = "your-secret-key-here"
```

```bash
# Linux/Mac
export DB_USER=postgres
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=chicken_diagnoses
export SECRET_KEY=your-secret-key-here
```

**Option B: Edit config.py directly**

Update the default values in `config.py`:

```python
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_password")
DB_NAME = os.environ.get("DB_NAME", "chicken_diagnoses")
```

### 6. Run the application

```bash
python run.py
```

The app will:
1. Create all database tables automatically
2. Seed default roles, permissions, and admin user
3. Seed the knowledge base (categories, symptoms, diseases, rules)
4. Start the development server

### 7. Access the application

Open your browser and go to:

```
http://127.0.0.1:5000
```

---

## Default Login

| Role  | Username | Password   |
|-------|----------|------------|
| Admin | admin    | Admin@123  |

The admin account can:
- Create Doctor and User accounts
- Manage the full knowledge base
- Review diagnosis cases
- View dashboard and audit logs

---

## Project Structure

```
.
├── app/
│   ├── __init__.py            # App factory
│   ├── forms/                 # WTForms definitions
│   ├── models/                # SQLAlchemy models
│   ├── routes/                # Blueprint routes
│   ├── services/              # Business logic layer
│   ├── static/                # CSS, JS, images
│   └── templates/             # Jinja2 HTML templates
├── utils/
│   ├── db_migrate.py          # Schema migration utility
│   └── decorators.py          # Permission decorators
├── config.py                  # App configuration
├── extensions.py              # Flask extensions (db, csrf, login)
├── run.py                     # Entry point
└── requirements.txt           # Python dependencies
```

---

## Resetting the Database

To drop all tables and re-seed from scratch:

```bash
# Windows PowerShell
$env:RESET_DB = "1"
python run.py
# Then stop the server and unset:
$env:RESET_DB = "0"
```

```bash
# Linux/Mac
RESET_DB=1 python run.py
```

---

## User Roles

| Role   | Permissions |
|--------|-------------|
| Admin  | Full system access (users, roles, permissions, knowledge base, dashboard, audit) |
| Doctor | Manage knowledge base, review cases, run diagnosis, view dashboard |
| User   | Run diagnosis, view own case history |

New users registered via the UI get the **User** role by default. Admins can promote users to Doctor via the Users management page.

---

## License

This project is developed for academic purposes at Norton University.
