from flask import abort
from flask_restful import Resource, marshal
from core.models import User
from extensions import db


class ModelResource(Resource):
    Model = None
    init_fields = None
    parser = None
    put_parser = None
    delete_parser = None
    resource_fields = None

    def _initialize_object(self, args):
        return self.Model(*[args[k] for k in self.init_fields])

    def get(self, obj_id=None):
        if obj_id:
            obj = self.Model.query.get(obj_id)
            if not obj:
                abort(404)
        else:
            obj = self.Model.query.all()

        if self.resource_fields is None:
            self.resource_fields = self.parser.get
        return marshal(obj, self.resource_fields), 200

    def post(self, obj_id=None):
        if obj_id:
            abort(405, "this route does not support post, have you tried put?")
        else:
            args = self.parser.post.parse_args(strict=True)

            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)

            # if user.role not User.ADMIN:
            #     abort(403)

            new_obj = self._initialize_object(args)
            for key in args:
                if args[key]:
                    setattr(new_obj, key, args[key])

            db.session.add(new_obj)
            db.session.commit()

            return new_obj.id, 201

    def put(self, obj_id=None):
        if not obj_id:
            abort(400)

        obj = self.Model.query.get(obj_id)
        if not obj:
            abort(404)

        args = self.parser.put.parse_args(strict=True)
        user = User.verify_auth_token(args.pop('token'))

        if not user:
            abort(401)

        # if user.role not User.ADMIN:
        #     abort(403)

        for key in args:
            if args[key]:
                setattr(obj, key, args[key])

        db.session.add(obj)
        db.session.commit()
        return obj.id, 201

    def delete(self, obj_id=None):
        if not obj_id:
            abort(400, "Please specificy the object you wish to delete"
                  "e.g. /api/1/<resource>/<OBJ_ID>, OBJ_ID is missing")

        obj = self.Model.query.get(obj_id)
        if not obj:
            abort(404)

        args = self.parser.delete.parse_args(strict=True)
        user = User.verify_auth_token(args['token'])

        if not user:
            abort(401)

        # if user.role not User.ADMIN:
        #     abort(403)

        db.session.delete(obj)
        db.session.commit()
        return "", 204
