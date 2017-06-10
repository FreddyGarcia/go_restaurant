from flask_restless import APIManager
# from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.geoa import ModelView

from app import app, db
from app.main_module.models import Restaurant, Rating, Location, User, Category
# from app.main_module.models import Point, MultiPoint, Polygon, MultiPolygon, LineString, MultiLineString

manager = APIManager(app, flask_sqlalchemy_db = db)


manager.create_api(Rating, methods=['POST', 'GET'])
manager.create_api(Location	, methods=['PUT', 'GET'])
manager.create_api(Restaurant, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'])

