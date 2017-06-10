from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# App Instance
app = Flask(__name__)

# Configuration
app.config.from_object('config')

# db instance
db = SQLAlchemy(app)

# registre routes
from app.main_module.routes import routes

# registre apis
from app.main_module import api

# administration
from app.main_module.admin import admin