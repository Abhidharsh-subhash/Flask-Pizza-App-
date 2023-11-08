from flask_restx import Namespace, Resource, fields
from ..models.orders import Order
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.users import User

orders_namespace = Namespace('orders', description='a namespace for orders')

# @orders_namespace.route('/')
# class HelloOrders(Resource):
#     def get(self):
#         return {'message':'hello orders'}

order_model = orders_namespace.model(
    'Order', {
        'id': fields.Integer(description='Primay key'),
        'size': fields.String(description='size of pizza', required=True, enum=['SMALL', 'MEDIUM', 'LARGE', 'EXTRA_LARGE']),
        'order_status': fields.String(description='status of the order', required=True, enum=['PENDING', 'IN_TRANSIT', 'DELIVERED']),
        'flavour': fields.String(description='flavour of the pizza')
    }
)


@orders_namespace.route('/orders')
class OrderGetCreate(Resource):
    @orders_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
        Get all orders
        """
        orders = Order.query.all()
        return orders, HTTPStatus.OK

    @orders_namespace.expect(order_model)
    @orders_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        Create new order
        """
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        if current_user is not None:
            data = orders_namespace.payload
            new_order = Order(
                size=data.get('size'),
                quantity=data.get('quantity'),
                flavour=data.get('flavour')
            )
            new_order.user = current_user.id
            new_order.save()
            return new_order, HTTPStatus.CREATED
        response = {
            'message': 'Something went wrong, Please try again'
        }
        return response, HTTPStatus.BAD_REQUEST


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
