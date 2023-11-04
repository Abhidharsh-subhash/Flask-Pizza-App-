from flask_restx import Namespace, Resource

orders_namespace = Namespace('orders', description='a namespace for orders')

# @orders_namespace.route('/')
# class HelloOrders(Resource):
#     def get(self):
#         return {'message':'hello orders'}


@orders_namespace.route('/orders')
class OrderGetCreate(Resource):
    def get(self):
        """
        Get all orders
        """
        pass

    def post(self):
        """
        Create new order
        """
        pass


@orders_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):
    def get(self, order_id):
        """
        Retrieve an order by id
        """
        pass

    def put(self, order_id):
        """
        Update an order by id
        """
        pass

    def delete(self, order_id):
        """
        Delete an order by id
        """
        pass


@orders_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    def get(self, user_id, order_id):
        """
        Get a user's specific order  
        """
        pass


@orders_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    def get(self, user_id):
        """
        Get all orders by a specific users
        """
        pass


@orders_namespace.route('/order/status/<int:order_id>')
class UpdateOrderStatus(Resource):
    def patch(self, order_id):
        """
        Update the order status
        """
        pass
