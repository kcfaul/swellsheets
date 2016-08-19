from core.models import Category
from core.parsers import CategoryParser

from core.controllers.base import ModelResource


class CategoryApi(ModelResource):
    Model = Category
    init_fields = ['name', ]
    parser = CategoryParser()

    def get(self, category_id=None):
        # if category_id:
        #    self.resource_fields = self.parser.get_single
        return super(CategoryApi, self).get(obj_id=category_id)

    def post(self, category_id=None):
        return super(CategoryApi, self).post(obj_id=category_id)

    def put(self, category_id=None):
        return super(CategoryApi, self).put(obj_id=category_id)

    def delete(self, category_id=None):
        return super(CategoryApi, self).delete(obj_id=category_id)
