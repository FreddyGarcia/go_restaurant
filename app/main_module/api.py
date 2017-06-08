from flask_restless import APIManager
from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.geoa import ModelView

from app import app, db
from app.main_module.models import Restaurant, Rating, Location, User, Category, Point
from app.main_module.models import Point, MultiPoint, Polygon, MultiPolygon, LineString, MultiLineString

manager = APIManager(app, flask_sqlalchemy_db = db)


manager.create_api(Rating, methods=['POST', 'GET'])
manager.create_api(Location	, methods=['PUT', 'GET'])
manager.create_api(Restaurant, methods=['GET', 'POST', 'DELETE', 'PUT'])
manager.create_api(User, methods=['GET', 'POST', 'DELETE', 'PUT'])



# Administration Site
admin = Admin(app, name='site_recommendations', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Restaurant, db.session))
admin.add_view(ModelView(Category, db.session))




admin.add_view(ModelView(Point, db.session, category='Points'))
admin.add_view(ModelView(MultiPoint, db.session, category='Points'))
admin.add_view(ModelView(Polygon, db.session, category='Polygons'))
admin.add_view(ModelView(MultiPolygon, db.session, category='Polygons'))
admin.add_view(ModelView(LineString, db.session, category='Lines'))
admin.add_view(ModelView(MultiLineString, db.session, category='Lines'))