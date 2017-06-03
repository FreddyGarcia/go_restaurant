# application
from flask_restless import APIManager

from app_db import app, db
from models import Restaurant

# registering apis
manager = APIManager(app, flask_sqlalchemy_db = db)
manager.create_api(Restaurant, methods=['GET', 'POST', 'DELETE', 'PUT'])
