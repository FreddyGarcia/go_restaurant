from flask import Blueprint, redirect
from simplejson import dumps as json_encode

from app import app
from app.main_module.models import Rating

routes = Blueprint('routes', __name__, url_prefix='/')

@routes.route("")
def works():
    return redirect("/admin")

@routes.route("api/recommendation/<user_id>")
def recommended(user_id):
	recommendations = Rating.get_recomendation_by_id(user_id)
	json = json_encode(recommendations)
	return json

app.register_blueprint(routes)

