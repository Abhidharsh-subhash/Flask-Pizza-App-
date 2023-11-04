from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .orders.views import orders_namespace
from .config.config import config_dict

# create_app function is responsible for creating and configuring the Flask application.


def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app)
    api.add_namespace(orders_namespace)
    api.add_namespace(auth_namespace, path='/auth')
    return app
