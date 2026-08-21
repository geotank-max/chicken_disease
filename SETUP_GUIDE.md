# Chicken Disease Diagnosis System - Setup & Run Guide

## Prerequisites

1. **Python 3.8+** installed
2. **PostgreSQL 12+** installed and running
3. **pgAdmin** for database management (already configured in your case)

## Setup Steps

### Step 1: Install Python Dependencies

```powershell
cd D:\Norton Y3S2\chicken_desease\NU_Chicken_Diagnoses_TT-KSN
pip install -r requirements.txt
```

### Step 2: Verify PostgreSQL Connection

Your database is already created in pgAdmin:
- **Database Name**: `chicken_diagnoses`
- **Owner**: `postgres`
- **Host**: localhost
- **Port**: 5432

The application will use these credentials:
- **Username**: postgres
- **Password**: 123456789

If your credentials are different, update [config.py](config.py) with your actual values.

### Step 3: Initialize the Database

Run the database initialization script to create tables and seed data:

```powershell
python init_db.py
```

This will:
- Create all database tables (Users, Roles, Permissions, Symptoms, Diseases, Rules, Cases, Audit Logs)
- Create default roles: Admin, Doctor, User
- Create admin user with credentials:
  - **Username**: `admin`
  - **Password**: `Admin@123`
- Seed expert system data (symptoms, diseases, diagnosis rules)

### Step 4: Run the Application

```powershell
python run.py
```

The application will start on: **http://localhost:5000**

## Default Login Credentials

- **Username**: `admin`
- **Password**: `Admin@123`

## Features

Once logged in, you can:

- **Expert System**
  - Create/Manage symptoms
  - Create/Manage diseases
  - Create/Manage diagnosis rules
  - Run chicken disease diagnosis
  - View case history

- **User Management**
  - Create and manage users
  - Assign roles (Admin, Doctor, User)

- **Role Management**
  - Define roles with specific permissions

- **Audit Trail**
  - View all system activities and changes

## Troubleshooting

### Database Connection Error
1. Verify PostgreSQL is running
2. Check pgAdmin shows the `chicken_diagnoses` database
3. Verify your credentials in `config.py`
4. Test connection: `psql -U postgres -h localhost -d chicken_diagnoses`

### Module Not Found Error
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### Permission Denied on init_db.py
```powershell
python init_db.py  # Should work without explicit execution rights
```

### Reset Database
To reset the database and re-seed from scratch:

```powershell
$env:RESET_DB="1"
python run.py
# Then Ctrl+C to stop
$env:RESET_DB="0"
python run.py
```

## Project Structure

- `app/` - Main Flask application
  - `models/` - SQLAlchemy database models
  - `routes/` - Flask blueprints and URL routes
  - `services/` - Business logic
  - `forms/` - WTForms for web forms
  - `templates/` - HTML templates
  - `static/` - CSS and JavaScript
  
- `config.py` - Configuration settings
- `extensions.py` - Flask extensions (SQLAlchemy, CSRF, Login Manager)
- `run.py` - Application entry point
- `init_db.py` - Database initialization script
- `requirements.txt` - Python dependencies

## Next Steps

1. Create additional users with different roles
2. Author expert system rules for disease diagnosis
3. Test the diagnosis system
4. Review audit logs for system activities
