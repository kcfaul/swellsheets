from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import abort, current_app
from flask_restful import Resource
from sqlalchemy.orm.exc import NoResultFound

from core.models import User
from core.parsers import AuthParser
from extensions import db

parser = AuthParser()


class BaseAuthApi(Resource):

    def _generate_token(self, user):
        s = Serializer(
            current_app.config['SECRET_KEY'],
            expires_in=6000
        )

        return s.dumps({'id': user.id})

    def create_user(self):
        args = parser.post.parse_args()

        try:
            user = User(email=args['email'])
            user.set_password(args['password'])

            db.session.add(user)
            db.session.commit()

            return {'email': user.email,
                    'token': self._generate_token(user)}

        except KeyError:
            return {'error': "Please provide an `email` and `password`"
                             " to create a new user"}
        abort(500)

    def verify_user(self):
        args = parser.post.parse_args()
        email = args['email']
        try:
            user = User.query.filter_by(
                email=email
            ).one()
        except NoResultFound:
            abort(404, "No user with email {} found".format(email))

        if user.check_password(args['password']):
            return {'token': self._generate_token(user)}
        else:
            abort(401)


class CreateUserApi(BaseAuthApi):
    def post(self):
        return self.create_user()


class AuthApi(BaseAuthApi):
    def post(self):
        return self.verify_user()
