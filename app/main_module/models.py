# app.models
from collections import namedtuple
from flask_admin import helpers as admin_helpers
from flask_security.utils import verify_password
from flask_security import Security, SQLAlchemyUserDatastore, \
	UserMixin, RoleMixin, login_required, current_user
from sqlalchemy.sql import func

from app import app, db

class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, server_default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
	restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
	rating = db.Column(db.Integer, nullable=False)

	def __init__(self, user, restaurant, rating):
		self.restaurant = restaurant
		self.rating = rating
		self.user = user

	@staticmethod
	def get_recomendation_by_id(user_id):
		# call get_recomended stored procedure
		result = db.session.execute('call get_recomended({0})'.format(user_id))
		Record = namedtuple('Record', result.keys())
		records = [Record(*r)._asdict() for r in result.fetchall()]
		return records

	@staticmethod
	def get_top_rated():
		# call get_recomended stored procedure
		result = db.session.execute('select * from top_rated')
		Record = namedtuple('Record', result.keys())
		records = [Record(*r)._asdict() for r in result.fetchall()]
		return records



class Restaurant(db.Model):
	id 	= db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	lat = db.Column(db.NUMERIC(20,8), nullable=False)
	lng = db.Column(db.NUMERIC(20,8), nullable=False)
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

	rating = db.relationship('Rating', backref='restaurant')

	def __init__(self, name=None, category=None, location=None):
		self.name = name
		self.category = category
		self.lat = location[0] if location is not None else 0
		self.lng = location[1] if location is not None else 0

	def __unicode__(self):
		return '%r' % str(self.name)


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True, nullable=False)
	restaurant = db.relationship('Restaurant', backref='category')

	def __init__(self, name=None):
		self.name = name

	def __unicode__(self):
		return '%r' % str(self.name)

# Define models
roles_users = db.Table(
	'roles_users',
	db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
	db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

	def __unicode__(self):
		return self.name

	def __str__(self):
		return self.name


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(30))
	last_name = db.Column(db.String(30))
	email = db.Column(db.String(30), unique=True)
	username = db.Column(db.String(20), unique=True)
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	roles = db.relationship('Role', secondary=roles_users,
							backref=db.backref('users', lazy='dynamic'))
	rating = db.relationship('Rating', backref='user')

	def verify_pass(self, password):
		return verify_password(password, self.password)

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		self.email = kwargs.get('email', kwargs.get('username', '')) + '@gmail.com'

	def __unicode__(self):
		return '%r' % str(self.username)


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

