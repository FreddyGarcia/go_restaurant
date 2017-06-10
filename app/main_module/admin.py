from flask_admin import Admin
from flask_admin.contrib.geoa import ModelView

from app import app, db
from app.main_module.models import Restaurant, Rating, Location, User, Category


# Administration Site
admin = Admin(app, name='Top Restaurants', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session, 'Usuarios'))
admin.add_view(ModelView(Location, db.session, 'Localizaciones'))
admin.add_view(ModelView(Restaurant, db.session, 'Restaurantes'))
admin.add_view(ModelView(Category, db.session, 'Categorias'))


