from flask import abort
from flask_restful import Resource, fields, marshal_with
from core.models import Product

nested_price_fields = {
    'id': fields.Integer(),
    'price': fields.Float(),
}

product_fields = {
    'id': fields.Integer(),
    'sku_code': fields.String(),
    'name': fields.String(),
    'description': fields.String(),
    'prices': fields.List(fields.Nested(nested_price_fields)),
}


class ProductApi(Resource):

    @marshal_with(product_fields)
    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            if not product:
                abort(404)
            return product

        else:
            products = Product.query.all()
            return products
