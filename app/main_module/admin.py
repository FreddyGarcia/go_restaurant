from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.geoa import ModelView

from app import app, db
from app.main_module.models import Restaurant, Rating, Category, User

# Administration Site


class RestaurantModelView(ModelView):
	column_list = ('name', 'category')
	form_excluded_columns = ['latitude', 'longitude', 'rating']
	column_labels = dict(name='Nombre', category='Categoria')

class UserModelView(ModelView):
	column_list = ('email', 'username')
	column_labels = dict(email='Correo', username='Nombre de usuario')
	form_excluded_columns = ['rating']

class CategoryModelView(ModelView):
	column_labels = dict(name='Nombre', restaurant='Restaurante')


class RestaurantLocationView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/restaurant/locate.html')

admin = Admin(app, name='Top Restaurants', template_mode='bootstrap3')
admin.add_view(RestaurantModelView(Restaurant, db.session, 'Restaurantes'))
admin.add_view(CategoryModelView(Category, db.session, 'Categorias'))
admin.add_view(UserModelView(User, db.session, 'Usuarios'))
admin.add_view(RestaurantLocationView(name='Localizar Restaurante', endpoint='analytics'))

