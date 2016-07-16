from flask import abort
from core.models import Category, User
from core.parsers import CategoryParser

from extensions import db

from core.controllers.base import ModelResource


class CategoryApi(ModelResource):
    Model = Category
    init_fields = ['name', ]
    parser = CategoryParser()
    put_parser = CategoryParser().put
    delete_parser = CategoryParser().delete

    def get(self, category_id=None):
        if category_id:
            self.resource_fields = self.parser.get_single
        return super(CategoryApi, self).get(obj_id=category_id)

    def post(self, category_id=None):
        return super(CategoryApi, self).post(obj_id=category_id)

    def put(self, category_id=None):
        if not category_id:
            abort(400)

        category = Category.query.get(category_id)
        if not category:
            abort(404)

        args = self.parser.put.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])

        if not user:
            abort(401)

        # if user.role not User.ADMIN:
        #     abort(403)

        if args['name']:
            category.name = args['name']

        if args['description']:
            category.description = args['description']

        if args['products']:
            # loop through existing products and update or add
            pass

        db.session.add(category)
        db.session.commit()
        return category.id, 201

    def delete(self, category_id=None):
        if not category_id:
            abort(400)

        category = Category.query.get(category_id)
        args = self.parser.delete.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])

        if not user:
            abort(401)

        db.session.delete(category)
        db.session.commit()
        return "", 204
