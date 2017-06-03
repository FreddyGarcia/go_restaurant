from flask_restless import APIManager

from app import app, db
from app.main_module.models import Restaurant

manager = APIManager(app, flask_sqlalchemy_db = db)
manager.create_api(Restaurant, methods=['GET', 'POST', 'DELETE', 'PUT'])
