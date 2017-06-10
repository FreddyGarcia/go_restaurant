from flask import Blueprint, redirect

from app import app

routes = Blueprint('routes', __name__, url_prefix='/')

@routes.route("")
def works():
    return redirect("/admin")

app.register_blueprint(routes)

