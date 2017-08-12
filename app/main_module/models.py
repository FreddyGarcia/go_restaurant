# app.models
from collections import namedtuple
from flask_admin import form
from flask_admin import helpers as admin_helpers
from flask_security.utils import verify_password
from flask_security import Security, SQLAlchemyUserDatastore, \
	UserMixin, RoleMixin, login_required, current_user
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from os import path as os_path
from sqlalchemy.sql import func

from app import app, db

class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, server_default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),)
	restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
	rating = db.Column(db.Integer, nullable=False)
	__table_args__ = (db.UniqueConstraint("user_id", "restaurant_id"),)

	def __init__(self, user, restaurant, rating):
		self.restaurant = restaurant
		self.rating = rating
		self.user = user

	@staticmethod
	def get_recomendation_by_id(user_id, minimal_rate = 0):
		# call get_recomended stored procedure
		result = db.session.execute('call get_recomended({0},{1})'.format(user_id, minimal_rate))
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
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	lat = db.Column(db.NUMERIC(20,8), nullable=False)
	lng = db.Column(db.NUMERIC(20,8), nullable=False)
	thumbnail = db.Column(db.Unicode(128))
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

	rating = db.relationship('Rating', backref='restaurant')

	def __init__(self, name=None, category=None, location=None):
		self.name = name
		self.category = category
		self.lat = location[0] if location is not None else 0
		self.lng = location[1] if location is not None else 0

	def __unicode__(self):
		return '%r' % str(self.name)

@db.event.listens_for(Restaurant, 'after_delete')
def del_image(mapper, connection, target):
	if target.thumbnail:
		# delete image
		try:
			os_remove(os_path.join(app.config['UPLOAD_IMG_FOLDER'], target.thumbnail))
		except Exception as e:
			pass

		try:
			os_remove(os_path.join(app.config['UPLOAD_IMG_FOLDER'],
					form.thumbgen_filename(target.thumbnail)))
		except Exception as e:
			pass


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True, nullable=False)
	restaurant = db.relationship('Restaurant', backref='category')

	def __init__(self, name=None):
		self.name = name

	def __str__(self):
		return str(self.name)

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

	def verify_password(self, password):
		return verify_password(password, self.password)

	def generate_auth_token(self, expiration=120):
		serializer = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
		return serializer.dumps({ 'id' : self.id})

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		self.email = kwargs.get('email', kwargs.get('username', '')) + '@gmail.com'

	def __unicode__(self):
		return '%r' % str(self.username)

	@staticmethod
	def verify_auth_token(token):
		serializer = Serializer(app.config['SECRET_KEY'])

		try:
			data = serializer.loads(token)
		except SignatureExpired: # valid but expired
			return None
		except BadSignature: # invalid
			return None

		user = User.query.filter_by(id=data.get('id')).first()
		return user


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

