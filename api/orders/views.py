from flask_restx import Namespace,Resource

orders_namespace=Namespace('orders',description='a namespace for orders')

@orders_namespace.route('/')
class HelloOrders(Resource):
    def get(self):
        return {'message':'hello orders'}