# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_babel import Babel

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
babel = Babel()