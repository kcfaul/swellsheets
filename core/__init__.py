from flask import Flask
from core.models import db
from extensions import login_manager, rest_api, bcrypt
from core.controllers.auth import AuthApi
from core.controllers.product import ProductApi
from core.controllers.category import CategoryApi


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    rest_api.add_resource(ProductApi,
                          '/api/1/product',
                          '/api/1/product/<int:product_id>',
                          endpoint='product')

    rest_api.add_resource(CategoryApi,
                          '/api/1/category',
                          '/api/1/category/<int:category_id>',
                          endpoint='category')

    rest_api.add_resource(AuthApi,
                          '/api/1/auth',
                          endpoint='auth',)

    rest_api.init_app(app)

    return app
