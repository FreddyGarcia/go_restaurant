from flask import Flask, render_template
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# App Instance
app = Flask(__name__)

# Http Auth Instance
auth = HTTPBasicAuth()

# Login manager instance
login_manager = LoginManager()

# Configuration
app.config.from_object('config')

# db instance
db = SQLAlchemy(app)

# login manager (duh!)
login_manager.init_app(app)

# registre routes
from app.main_module.routes import routes

# registre apis
from app.main_module import api

# administration
from app.main_module.admin import admin

# authentication
from app.main_module import authentication

# populate db
from app.main_module import populate_db


