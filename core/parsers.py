from flask_restful import fields, reqparse

product_fields = {
    'id': fields.Integer(),
    # 'sku_code': fields.String(),
    'name': fields.String(),
    'description': fields.String(),
    'category_id': fields.Integer(),
    # 'prices': fields.List(fields.Nested(nested_price_fields)),
}


class ParserField(object):

    def __init__(self, *args, **kwargs):
        self._kwargs = kwargs


class ApiParser(object):

    def __new__(cls):
        obj = super(ApiParser, cls).__new__(cls)
        obj._fields = {key: value for key, value
                       in cls.__dict__.items()
                       if type(value) is ParserField}

        return obj

    def _create_parser(self, method_name):
        parser = reqparse.RequestParser()

        for key, value in self._fields.items():
            kwargs = value._kwargs
            if "required" in kwargs:
                try:
                    if method_name not in kwargs["required"]:
                        del kwargs["required"]
                    else:
                        kwargs["required"] = True
                except TypeError:
                    if kwargs["required"] is not True:
                        del kwargs["required"]

            parser.add_argument(key, **kwargs)

        return parser

    @property
    def get(self):
        raise NotImplementedError

    @property
    def post(self):
        return self._create_parser('POST')

    @property
    def put(self):
        return self._create_parser('PUT')

    @property
    def delete(self):
        return self._create_parser('DELETE')
# END GENARICS #


class AuthParser(ApiParser):
    email = ParserField(type=str, required=True)
    password = ParserField(type=str, required=True)


class ProductParser(ApiParser):
    name = ParserField(type=str, required=['POST'],
                       help="`name` is required")
    description = ParserField(type=str, required=['POST'],
                              help="`description` is required")
    category_id = ParserField(type=str, required=['POST'],
                              help="`category_id` is required")
    skus = ParserField(type=list, action='append',)
    token = ParserField(type=str, required=True,
                        help="Auth Token is required to create products")

    @property
    def get(self):

        nested_price_fields = {
            'id': fields.Integer(),
            'price': fields.Float(),
        }

        product_fields = {
            'id': fields.Integer(),
            # 'sku_code': fields.String(),
            'name': fields.String(),
            'description': fields.String(),
            'category_id': fields.Integer(),
            # 'prices': fields.List(fields.Nested(nested_price_fields)),
        }
        return product_fields


class CategoryProductList(fields.Raw):
    def format(self, value):
        return [val.id for val in value]


class CategoryParser(ApiParser):
    name = ParserField(type=str, required=['POST'],
                       help="`name` is required")
    description = ParserField(type=str, required=['POST'],
                              help="`description` is required")
    products = ParserField(type=list, action='append',)
    token = ParserField(type=str, required=True,
                        help="Auth Token is required to create products")

    @property
    def get(self):
        category_fields = {
            'id': fields.Integer(),
            'name': fields.String(),
            'description': fields.String(),
            'products': CategoryProductList(),
        }
        return category_fields

    @property
    def get_single(self):
        category_fields = {
            'id': fields.Integer(),
            'name': fields.String(),
            'description': fields.String(),
            'products': fields.List(fields.Nested(product_fields)),
        }
        return category_fields
