from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
# get_jwt_identity which helps us to provide the identity of the user which created the token
from flask_jwt_extended import create_refresh_token, create_access_token, jwt_required, get_jwt_identity
from werkzeug.exceptions import Conflict, BadRequest

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

login_model = auth_namespace.model(
    'Login', {
        'email': fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password')
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
        if user_exist:
            response = {
                'message': 'email already exists'
            }
            return response, HTTPStatus.BAD_REQUEST
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
            # raise Conflict(f'User with the email {data.get('email')} exists')
        return new_user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """
        Generate a JWT pair
        """
        data = request.get_json()
        password = data.get('password')
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if (user is not None) and (check_password_hash(user.password_hash, password)):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
            return response, HTTPStatus.OK
        # response = {
        #     'message': 'Invalid Username or Password'
        # }
        # return response, HTTPStatus.BAD_REQUEST
        raise BadRequest('Invalid username or password')


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, HTTPStatus.OK
