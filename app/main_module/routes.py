from flask import Blueprint, jsonify

from app import app, db

routes = Blueprint('routes', __name__, url_prefix='/')

@routes.route("works")
def works():
	return "It works!"

app.register_blueprint(routes)

