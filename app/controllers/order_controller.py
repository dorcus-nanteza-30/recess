from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.order import Order
from app.models.user import User
from app.extensions import db

order_bp = Blueprint('order_bp', __name__, url_prefix='/api/v1/orders')

# Create an order
@order_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order():
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"message": "Access forbidden: Only logged-in users can create orders"}), HTTP_400_BAD_REQUEST

    status_of_order = data.get('status_of_order')
    address_of_delivery = data.get('address_of_delivery')

    if not status_of_order or not address_of_delivery:
        return jsonify({"message": "All fields (status_of_order, address_of_delivery) are required"}), HTTP_400_BAD_REQUEST

    new_order = Order(
        user_id=user_id,
        status_of_order=status_of_order,
        address_of_delivery=address_of_delivery
    )

    try:
        db.session.add(new_order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the order", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Order created successfully"}), HTTP_201_CREATED

# Update an order
@order_bp.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_order(id):
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"message": "Access forbidden: Only logged-in users can update orders"}), HTTP_400_BAD_REQUEST

    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), HTTP_404_NOT_FOUND

    if order.user_id != user_id:
        return jsonify({"message": "Access forbidden: You can only update your own orders"}), HTTP_400_BAD_REQUEST

    status_of_order = data.get('status_of_order', order.status_of_order)
    address_of_delivery = data.get('address_of_delivery', order.address_of_delivery)

    order.status_of_order = status_of_order
    order.address_of_delivery = address_of_delivery

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the order", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Order updated successfully"}), HTTP_200_OK

# Delete an order
@order_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order(id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"message": "Access forbidden: Only logged-in users can delete orders"}), HTTP_400_BAD_REQUEST

    order = Order.query.get(id)
    if not order:
        return jsonify({"message": "Order not found"}), HTTP_404_NOT_FOUND

    if order.user_id != user_id:
        return jsonify({"message": "Access forbidden: You can only delete your own orders"}), HTTP_400_BAD_REQUEST

    try:
        db.session.delete(order)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the order", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Order deleted successfully"}), HTTP_200_OK
