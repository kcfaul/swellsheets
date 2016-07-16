from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import abort, current_app
from flask_restful import Resource

from core.models import User

from core.parsers import AuthParser

parser = AuthParser()


class AuthApi(Resource):
    def post(self):
        args = parser.post.parse_args()
        user = User.query.filter_by(
            email=args['email']
        ).one()

        if user.check_password(args['password']):
            s = Serializer(
                current_app.config['SECRET_KEY'],
                expires_in=6000
            )

            return {'token': s.dumps({'id': user.id})}
        else:
            abort(401)
