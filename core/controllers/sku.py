from core.models import ProductSku
from core.parsers import ProductSkuParser

from core.controllers.base import ModelResource


class ProductSkuApi(ModelResource):
    Model = ProductSku
    parser = ProductSkuParser()
    init_fields = ['sku_code', 'description', ]

    def get(self, sku_id=None):
        return super(ProductSkuApi, self).get(obj_id=sku_id)

    def post(self, sku_id=None):
        return super(ProductSkuApi, self).post(obj_id=sku_id)

    def put(self, sku_id=None):
        return super(ProductSkuApi, self).put(obj_id=sku_id)

    def delete(self, sku_id=None):
        return super(ProductSkuApi, self).delete(obj_id=sku_id)
