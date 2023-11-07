from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus

auth_namespace = Namespace(
    'auth', description='a namespace for authentication')

# @auth_namespace.route('/')
# class HelloAuth(Resource):
#     def get(self):
#         return {'message':'hello auth'}

signup_model = auth_namespace.model(
    'SignUp', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password')
    }
)

user_model = auth_namespace.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email': fields.String(required=True, description='An email'),
        'password_hash': fields.String(required=True, description='A password'),
        'is_active': fields.Boolean(description='This shows that user is active'),
        'is_staff': fields.Boolean(description='This shows of user is staff')
    }
)


@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    # response from the POST request should be serialized using the user_model.
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Create a new user account
        """
        data = request.get_json()
        # filter_by is used for simple conditions and filter is used when there is complex conditions
        user_exist = User.query.filter_by(email=data.get('email')).first()
        print(user_exist)
        if user_exist:
            return user_exist, HTTPStatus.BAD_REQUEST
        print('after')
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password_hash=generate_password_hash(data.get('password')),
            is_staff=True,
            is_active=True
        )
        try:
            new_user.save()
        except Exception as e:
            return {'error': str(e)}, HTTPStatus.INTERNAL_SERVER_ERROR
        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        """
        Generate a JWT pair
        """
        pass
