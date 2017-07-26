from flask import Blueprint, redirect, jsonify, request, render_template, url_for, flash, g
from http import HTTPStatus

import flask_login
from app import app, login_manager, auth
from app.main_module.models import db, Rating, User, Restaurant

routes = Blueprint('routes', __name__, url_prefix='/')

@routes.route("")
def works():
	return redirect("/admin")


# # # # # # # # # # # # # # # # # # # # #
 # # # # # # # authentication # # # # #
# # # # # # # # # # # # # # # # # # # # #
@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('authentication/login.html')

	email = request.form['email']
	passw = request.form['password']
	user = User.query.filter_by(email=email).first()

	if user:
		if user.verify_pass(passw):
			flask_login.login_user(user)
			return redirect('/admin')
		else:
			flash('Password invalido', 'login_error')
	else:
		flash('Usuario no encontrado', 'login_error')

	return render_template('authentication/login.html')


@app.route('/api/token')
@auth.login_required
def get_auth_token():
	token = g.user.generate_auth_token()
	return jsonify(token=token.decode('ascii'))


@app.route('/api')
@auth.login_required
def it_works():
	return 'It Works!'


@auth.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)

    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/protected')
@flask_login.login_required
def protected():
	return 'Logged in as: ' + str(flask_login.current_user.id)


@app.route('/logout')
def logout():
	flask_login.logout_user()
	return redirect(url_for('login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
	return 'Unauthorized'

# # # # # # # # # # # # # # # # # # # # #
 # # # # # # # recomendations # # # # #
# # # # # # # # # # # # # # # # # # # # #
@routes.route("api/recomendation/<user_id>")
def recomended(user_id):
	recomendations = Rating.get_recomendation_by_id(user_id)
	return  jsonify(data=recomendations)


@routes.route("api/top_rated")
def top_rated():
	top_rated = Rating.get_top_rated()
	return jsonify(top_rated)


@routes.route("api/give_recomendation/<restaurant_id>/<rate>", methods=['GET', 'POST'])
def give_recomendation(restaurant_id, rate):
	restaurant = Restaurant.query.filter_by(id=restaurant_id).one()
	existing_rate = Rating.query.filter_by(user_id=flask_login.current_user.id, restaurant_id=restaurant_id).first()

	if 	existing_rate:
		existing_rate.rating = rate
	else:
		rating = Rating(flask_login.current_user, restaurant, rate)
		db.session.add(rating)

	db.session.commit()
	return jsonify(True)

app.register_blueprint(routes)



