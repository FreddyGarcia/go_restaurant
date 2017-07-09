# app.models
from sqlalchemy.sql import func
from collections import namedtuple

from app import db

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


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	username = db.Column(db.String(80), unique=True)

	rating = db.relationship('Rating', backref='user')

	def __init__(self, username=None, email=None):
		self.username = username
		self.email = email

		if not email:
			self.email = self.username + '@gmail.com'

 	def __unicode__(self):
		return '%r' % str(self.username)

db.drop_all()
db.create_all()
# '''
# POPULATE DB

u_albelto = User('albelto')
u_freddy = User('freddy')
u_mafer = User('mafer')
u_nick = User('nick')
u_eddy = User('eddy')

category_fast_fo = Category('Comida Rapida')
category_chinese = Category('Comida China')
category_italian = Category('Comida Italiana')
category_pizza = Category('pizeria')

r_papa_johns = Restaurant('Papa John' , category_pizza, (18.4847289, -69.919273))
r_buen_sabor = Restaurant('Buen Sabor', category_fast_fo, (18.5048942, -69.8862213))
r_pizzahut = Restaurant('Pizzahut', category_pizza, (18.3048942, -69.8812213))
r_tropical = Restaurant('Adrian Tropical', category_italian, (18.5048942, -69.8862213))
r_teriyaki = Restaurant('Teriyaki', category_chinese, (18.2048942, -69.8662213))
r_dominos = Restaurant('Dominos', category_pizza, (18.4048942, -69.8462213))
r_mofongo = Restaurant('Mofonfo', category_fast_fo, (18.6048942, -69.8832213))

# users
db.session.add(u_nick)
db.session.add(u_mafer)
db.session.add(u_freddy)
db.session.add(u_eddy)
db.session.add(u_albelto)

# restaurants
db.session.add(r_papa_johns)
db.session.add(r_buen_sabor)
db.session.add(r_pizzahut)
db.session.add(r_tropical)
db.session.add(r_teriyaki)
db.session.add(r_dominos)
db.session.add(r_mofongo)

# categories
db.session.add(category_fast_fo)
db.session.add(category_chinese)
db.session.add(category_italian)
db.session.add(category_pizza)

# rating
# rating between 1 and 5
# db.session.add(Rating(r_pizzahut, 2))

db.session.add(Rating(u_freddy, r_teriyaki, 2))
db.session.add(Rating(u_freddy, r_buen_sabor, 3))
db.session.add(Rating(u_freddy, r_pizzahut, 5))

db.session.add(Rating(u_albelto, r_papa_johns, 1))
db.session.add(Rating(u_albelto, r_pizzahut, 4))
db.session.add(Rating(u_albelto, r_buen_sabor, 1))

db.session.add(Rating(u_mafer, r_pizzahut, 4))
db.session.add(Rating(u_mafer, r_teriyaki, 4))
db.session.add(Rating(u_mafer, r_pizzahut, 5))
db.session.add(Rating(u_mafer, r_tropical, 5))
db.session.add(Rating(u_mafer, r_mofongo, 5))
db.session.add(Rating(u_mafer, r_dominos, 5))

db.session.add(Rating(u_eddy, r_dominos, 5))

db.session.add(Rating(u_nick, r_tropical, 5))
db.session.add(Rating(u_nick, r_teriyaki, 3))
db.session.add(Rating(u_nick, r_pizzahut, 4))

db.session.commit()
# '''