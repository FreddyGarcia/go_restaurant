from flask_restless import APIManager

from app import app, db
from app.main_module.models import Restaurant, Rating, User

manager = APIManager(app, flask_sqlalchemy_db = db)
manager.create_api(User, methods=['GET'])
manager.create_api(Rating, methods=['POST', 'GET', 'PUT'])
manager.create_api(Restaurant, methods=['POST', 'GET', 'PUT'])
