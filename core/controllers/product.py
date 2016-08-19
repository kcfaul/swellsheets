from core.models import Product
from core.parsers import ProductParser
from core.controllers.base import ModelResource


class ProductApi(ModelResource):

    Model = Product
    init_fields = ['name', ]
    parser = ProductParser()

    def get(self, product_id=None):
        return super(ProductApi, self).get(obj_id=product_id)

    def post(self, product_id=None):
        return super(ProductApi, self).post(obj_id=product_id)

    def put(self, product_id=None):
        return super(ProductApi, self).put(obj_id=product_id)

    def delete(self, product_id=None):
        return super(ProductApi, self).delete(obj_id=product_id)
