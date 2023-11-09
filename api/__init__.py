from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .orders.views import orders_namespace
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

# create_app function is responsible for creating and configuring the Flask application.


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    api = Api(app)
    api.add_namespace(orders_namespace)
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def not_found(error):
        return {'error': 'Not Found'}, 404

    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'The current method is not allowed in this API'}, 405
    # above methods are the custom errorhandlers

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order
        }
    return app
