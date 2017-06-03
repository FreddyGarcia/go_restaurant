# app.models
from app import db

class Location(db.Model):
	key = db.Column(db.Integer, primary_key=True)
	latitude = db.Column(db.Integer, nullable=False)
	longitude = db.Column(db.Integer, nullable=False)
	description = db.Column(db.Text, nullable=False)
	restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

	def __init__(self, description, coordinate, restaurant):
		self.description = description
		self.latitude = coordinate[0]
		self.longitude = coordinate[1]
		self.restaurant_id = restaurant.id

	def __repr__(self):
		return '<Location %r>' % self.description[:10]

class Restaurant(db.Model):
	id 	= db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), unique=True, nullable=False)
	locations = db.relationship('Location', backref='restaurant', lazy='dynamic')

	def __init__(self, name, **kwargs):
		self.name = name

	def __repr__(self):
		return '<Restaurant %r>' % self.name

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return '<User %r>' % self.username


# db.drop_all()
# db.create_all()

# # restaurants
# db.session.add(Restaurant('Buen Sabor'))
# db.session.add(Restaurant('Chino'))
# db.session.add(Restaurant('Sabor'))
# db.session.add(Restaurant('Buen'))
# db.session.commit()

# # locations
# db.session.add(Location('27 de febrero', (1,2), Restaurant.query.filter_by(name='Buen Sabor').one()))
# db.session.add(Location('Por la Gomez', (1,2), Restaurant.query.filter_by(name='Buen Sabor').one()))
# db.session.add(Location('Villa Faro', (1,2), Restaurant.query.filter_by(name='Sabor').one()))
# db.session.add(Location('Zona Colonial', (1,2), Restaurant.query.filter_by(name='Chino').one()))
# db.session.commit()

# manager = APIManager(app, flask_sqlalchemy_db = db)

# manager.create_api(Restaurant, methods=['GET', 'POST', 'DELETE'])
# # # # # # # # # # # # # # # # # # # # # # # # #
