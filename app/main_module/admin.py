from flask import redirect, render_template, url_for, request
from flask_admin import Admin, BaseView, expose, AdminIndexView, form
from flask_admin.base import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from jinja2 import Markup
from os import path as os_path, remove as os_remove
from werkzeug.utils import secure_filename

from app import app, db
from app.main_module.models import Restaurant, Rating, Category, User

# Administration Site
class CustomModelView(ModelView):
	pass
	# def is_accessible(self):
	#     if not current_user.is_active or not current_user.is_authenticated:
	#         return False


class RestaurantModelView(CustomModelView):
	column_list = ('name', 'category', 'thumbnail')
	form_excluded_columns = ['lat', 'lng', 'rating']
	column_labels = dict(name='Nombre', category='Categoria', thumbnail='Miniatura')

	def prefix_name(obj, file_data):
	    parts = os_path.splitext(file_data.filename)
	    return secure_filename('file-%s%s' % parts)

	form_extra_fields = {
		'thumbnail' : form.ImageUploadField('Miniatura',
										base_path=app.config['UPLOAD_IMG_FOLDER'],
										namegen=prefix_name,
										thumbnail_size=(100,100, True))
	}


	def _list_thumbnail(view, contet, model, name):
		if not model.thumbnail:
			return Markup('<img width=28 src="/static/default.ico" />')

		return Markup('<img width=28  src="%s" />' %  url_for('static',filename=form.thumbgen_filename(model.thumbnail)))

	column_formatters = {
		'thumbnail' : _list_thumbnail
	}

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

		restaurants = Restaurant.query.all()
		return self.render('admin/index.html', restaurants=restaurants)

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


