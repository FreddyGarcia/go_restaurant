from flask_restless import APIManager
from flask_admin.contrib.geoa import ModelView

from app import app, db
from app.main_module.models import Restaurant, Rating

manager = APIManager(app, flask_sqlalchemy_db = db)
manager.create_api(Rating, methods=['POST', 'GET', 'PUT'])
manager.create_api(Restaurant, methods=['POST', 'GET', 'PUT'])
