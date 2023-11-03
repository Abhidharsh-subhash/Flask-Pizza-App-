from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .orders.views import orders_namespace

def create_app():
    app=Flask(__name__)
    api=Api(app)
    api.add_namespace(orders_namespace,'/')
    api.add_namespace(auth_namespace,'/auth')
    return app