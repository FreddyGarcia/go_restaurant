# app.models
from sqlalchemy.sql import func
# from geoalchemy2 import Geometry
from geoalchemy2.types import Geometry

from app import db

class Rating(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, server_default=func.now())
	user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, unique=True)
	rating = db.Column(db.Integer, nullable=False)
	restaurant = db.Column(db.Integer, db.ForeignKey('restaurant.id'), unique=True)

	def __init__(self, restaurant=None, rating=None, user=None):
 		self.rating = rating
		self.user = user
		self.restaurant = restaurant

class Location(db.Model):
	key = db.Column(db.Integer, primary_key=True)
	latitude = db.Column(db.Integer, nullable=False)
	longitude = db.Column(db.Integer, nullable=False)
	description = db.Column(db.Text, nullable=False)
	restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

	def __init__(self, description=None, coordinate=None, restaurant=None):
		self.description = description
		self.latitude = coordinate[0]
		self.longitude = coordinate[1]
		self.restaurant_id = restaurant.id

	def __repr__(self):
		return '<Location %r>' % self.description[:10]

categories = db.Table('restaurant_categories',
	db.Column('restaurant', db.Integer, db.ForeignKey('restaurant.id') ),
	db.Column('category', db.Integer, db.ForeignKey('category.id') )
)

class Restaurant(db.Model):
	id 	= db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	categories = db.relationship('Category', secondary=categories, backref=db.backref('categories', lazy='dynamic'))
	locations = db.relationship('Location', backref='restaurant', lazy='dynamic')

	def __init__(self, name=None):
		self.name = name

	def __repr__(self):
		return '<Restaurant %r>' % self.name


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True, nullable=False)

	def __init__(self, name=None):
		self.name = name

	def __repr__(self):
		return '<Category %r>' % self.name

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	username = db.Column(db.String(80), unique=True)

	def __init__(self, username=None, email=None):
		self.username = username
		self.email = email

		if not email:
			self.email = self.username + '@gmail.com'

 	def __repr__(self):
		return '<User %r>' % self.username




class Point(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    point = db.Column(Geometry("POINT"))


class MultiPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    point = db.Column(Geometry("MULTIPOINT"))


class Polygon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    point = db.Column(Geometry("POLYGON"))


class MultiPolygon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    point = db.Column(Geometry("MULTIPOLYGON"))


class LineString(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    point = db.Column(Geometry("LINESTRING"))


class MultiLineString(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    point = db.Column(Geometry("MULTILINESTRING"))




db.drop_all()
db.create_all()
# '''
# POPULATE DB
# users
db.session.add(User('nick'))

# categories
db.session.add(Category('Comida Rapida'))
db.session.add(Category('Comida China'))
db.session.add(Category('Comida Italiana'))

# restaurants
db.session.add(Restaurant('Buen Sabor'))
db.session.add(Restaurant('Chino'))
db.session.add(Restaurant('Sabor'))
db.session.add(Restaurant('Buen'))

# locations
db.session.add(Location('27 de febrero', (1,2), Restaurant.query.filter_by(name='Buen Sabor').one()))
db.session.add(Location('Por la Gomez', (1,2), Restaurant.query.filter_by(name='Buen Sabor').one()))
db.session.add(Location('Villa Faro', (1,2), Restaurant.query.filter_by(name='Sabor').one()))
db.session.add(Location('Zona Colonial', (1,2), Restaurant.query.filter_by(name='Chino').one()))

db.session.commit()
# '''
