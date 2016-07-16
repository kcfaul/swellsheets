from flask import abort
from core.models import Category, Product, User
from core.parsers import ProductParser
from core.controllers.base import ModelResource
from extensions import db


class ProductApi(ModelResource):

    Model = Product
    init_fields = ['name', ]
    parser = ProductParser()
    put_parser = ProductParser().put
    delete_parser = ProductParser().delete

    def get(self, product_id=None):
        return super(ProductApi, self).get(obj_id=product_id)

    def post(self, product_id=None):
        return super(ProductApi, self).post(obj_id=product_id)

    def put(self, product_id=None):
        if not product_id:
            abort(400)

        product = Product.query.get(product_id)
        if not product:
            abort(404)

        args = self.parser.put.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])

        if not user:
            abort(401)

        # if user.role not User.ADMIN:
        #     abort(403)

        if args['name']:
            product.name = args['name']

        if args['description']:
            product.description = args['description']

        if args['category_id']:
            category = Category.query.get(args['category_id'])
            if not category:
                abort(404, "No Matching Category Found")

            product.add_category(category)

        if args['skus']:
            # loop through existing skus and update or add
            pass

        db.session.add(product)
        db.session.commit()
        return product.id, 201

    def delete(self, product_id=None):
        if not product_id:
            abort(400)

        product = Product.query.get(product_id)
        if not product:
            abort(404)

        args = self.parser.delete.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])

        if not user:
            abort(401)

        # if user.role not User.ADMIN:
        #     abort(403)

        db.session.delete(product)
        db.session.commit()
        return "", 204
