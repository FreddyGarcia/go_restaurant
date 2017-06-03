from flask import Blueprint, jsonify, json, request, render_template, session, url_for

from app import app, db

routes = Blueprint('routes', __name__, url_prefix='/')

@routes.route("/works")
def logout():
	return "It works!"

app.register_blueprint(routes)

