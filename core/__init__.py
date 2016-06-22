from flask import Flask
from core.models import db
from extensions import login_manager, rest_api
from core.controllers.product import ProductApi


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    login_manager.init_app(app)

    rest_api.add_resource(ProductApi,
                          '/api/1/product',
                          '/api/1/product/<int:product_id>',
                          endpoint='api',
                          )
    rest_api.init_app(app)

    return app
