from flask_security.utils import encrypt_password

from app import app
from app.main_module.models import *


db.drop_all()
db.create_all()

with app.app_context():
	user_role = Role(name='user')
	super_user_role = Role(name='superuser')
	db.session.add(user_role)
	db.session.add(super_user_role)
	db.session.commit()

	user_datastore.create_user(
	    first_name='Admin',
	    username='Administrator',
	    email='admin',
	    password=encrypt_password('admin'),
	    roles=[user_role, super_user_role]
	)

	u_albelto = User(username='albelto',password=encrypt_password('test'),roles=[user_role, super_user_role])
	u_freddy = User(username='freddy',password=encrypt_password('test'))
	u_mafer = User(username='mafer',password=encrypt_password('test'))
	u_nick = User(username='nick',password=encrypt_password('test'))
	u_eddy = User(username='eddy',password=encrypt_password('test'))

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

	# # users
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
	# rating between 1 and 3
	db.session.add(Rating(u_freddy, r_teriyaki, 2))
	db.session.add(Rating(u_freddy, r_buen_sabor, 3))
	db.session.add(Rating(u_freddy, r_pizzahut, 3))

	db.session.add(Rating(u_albelto, r_papa_johns, 1))
	db.session.add(Rating(u_albelto, r_pizzahut, 3))
	db.session.add(Rating(u_albelto, r_buen_sabor, 1))
	db.session.add(Rating(u_albelto, r_dominos, 2))

	db.session.add(Rating(u_mafer, r_teriyaki, 3))
	db.session.add(Rating(u_mafer, r_pizzahut, 3))
	db.session.add(Rating(u_mafer, r_tropical, 2))
	db.session.add(Rating(u_mafer, r_mofongo, 1))
	db.session.add(Rating(u_mafer, r_dominos, 2))

	db.session.add(Rating(u_eddy, r_dominos, 2))

	db.session.add(Rating(u_nick, r_tropical, 2))
	db.session.add(Rating(u_nick, r_buen_sabor, 1))

	db.session.commit()
	# '''

