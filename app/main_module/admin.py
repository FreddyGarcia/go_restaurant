from flask import redirect, render_template, url_for
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.base import MenuLink
from flask_admin.contrib.geoa import ModelView
from flask_login import current_user

from app import app, db
from app.main_module.models import Restaurant, Rating, Category, User

# Administration Site

class CustomModelView(ModelView):
	pass
	# def is_accessible(self):
	#     if not current_user.is_active or not current_user.is_authenticated:
	#         return False


class RestaurantModelView(CustomModelView):
	column_list = ('name', 'category')
	form_excluded_columns = ['latitude', 'longitude', 'rating']
	column_labels = dict(name='Nombre', category='Categoria')


class UserModelView(CustomModelView):
	column_list = ('email', 'username')
	column_labels = dict(email='Correo', username='Nombre de usuario')
	form_excluded_columns = ['rating']


class CategoryModelView(CustomModelView):
	column_labels = dict(name='Nombre', restaurant='Restaurante')


class RestaurantLocationView(BaseView):
	@expose('/')
	def index(self):
		return self.render('admin/restaurant/locate.html')

# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):

	@expose('/')
	def index(self):
		if not current_user.is_authenticated:
			return redirect(url_for('login'))
		top_rated = Rating.get_top_rated()
		return self.render('admin/index.html', top_rated=top_rated)
		# return super(MyAdminIndexView, self).index()

	# @expose('/login/', methods=('GET', 'POST'))
	# def login_view(self):
	#     # handle user login
	#     form = LoginForm(request.form)
	#     if helpers.validate_form_on_submit(form):
	#         user = form.get_user()
	#         login_user(user)

	#     if current_user.is_authenticated:
	#         return redirect(url_for('.index'))
	#     link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
	#     self._template_args['form'] = form
	#     self._template_args['link'] = link
	#     return super(MyAdminIndexView, self).index()

	# @expose('/register/', methods=('GET', 'POST'))
	# def register_view(self):
	#     form = RegistrationForm(request.form)
	#     if helpers.validate_form_on_submit(form):
	#         user = User()

	#         form.populate_obj(user)
	#         # we hash the users password to avoid saving it as plaintext in the db,
	#         # remove to use plain text:
	#         user.password = generate_password_hash(form.password.data)

	#         db.session.add(user)
	#         db.session.commit()

	#         login_user(user)
	#         return redirect(url_for('.index'))
	#     link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
	#     self._template_args['form'] = form
	#     self._template_args['link'] = link
	#     return super(MyAdminIndexView, self).index()

	# @expose('/logout/')
	# def logout_view(self):
	#     logout_user()
	#     return redirect(url_for('.index'))


admin = Admin(app, name='Top Restaurants', template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(RestaurantModelView(Restaurant, db.session, 'Restaurantes'))
admin.add_view(CategoryModelView(Category, db.session, 'Categorias'))
admin.add_view(UserModelView(User, db.session, 'Usuarios'))

admin.add_view(RestaurantLocationView(name='Localizar Restaurante', endpoint='restaurantposition'))
admin.add_link(MenuLink(name='Cerrar Sesion', url='/logout'))


