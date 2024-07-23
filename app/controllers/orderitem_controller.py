from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.orderitem import OrderItem
from app.models.user import User
from app.extensions import db

orderitem_bp = Blueprint('orderitem_bp', __name__, url_prefix='/api/v1/orderitem')

# Create an order item
@orderitem_bp.route('/create', methods=['POST'])
@jwt_required()
def create_order_item():
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # Check if user is logged in
    if not current_user:
        return jsonify({"message": "Access forbidden: Only logged-in users can create order items"}), HTTP_400_BAD_REQUEST

    # Extract data and perform basic validation
    order_id = data.get('order_id')
    merchandise_id = data.get('merchandise_id')
    quantity = data.get('quantity')
    price_of_item = data.get('price_of_item')

    if not order_id or not merchandise_id or not quantity or not price_of_item:
        return jsonify({"message": "All fields (order_id, merchandise_id, quantity, price_of_item) are required"}), HTTP_400_BAD_REQUEST

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "Invalid quantity format (must be an integer)"}), HTTP_400_BAD_REQUEST

    try:
        price_of_item = float(price_of_item)
    except ValueError:
        return jsonify({"message": "Invalid price_of_item format (must be a number)"}), HTTP_400_BAD_REQUEST

    # Create new order item
    new_order_item = OrderItem(
        order_id=order_id,
        merchandise_id=merchandise_id,
        quantity=quantity,
        price_of_item=price_of_item
    )

    try:
        db.session.add(new_order_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the order item", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Order item created successfully"}), HTTP_201_CREATED

# Update an order item
@orderitem_bp.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_order_item(id):
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # Check if user is logged in
    if not current_user:
        return jsonify({"message": "Access forbidden: Only logged-in users can update order items"}), HTTP_400_BAD_REQUEST

    # Retrieve the order item by ID
    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({"message": "Order item not found"}), HTTP_404_NOT_FOUND

    # Extract data and perform basic validation
    quantity = data.get('quantity', order_item.quantity)
    price_of_item = data.get('price_of_item', order_item.price_of_item)

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "Invalid quantity format (must be an integer)"}), HTTP_400_BAD_REQUEST

    try:
        price_of_item = float(price_of_item)
    except ValueError:
        return jsonify({"message": "Invalid price_of_item format (must be a number)"}), HTTP_400_BAD_REQUEST

    # Update the order item
    order_item.quantity = quantity
    order_item.price_of_item = price_of_item
    order_item.total_amount = quantity * price_of_item

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the order item", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Order item updated successfully"}), HTTP_200_OK

# Delete an order item
@orderitem_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_order_item(id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user:
        return jsonify({"message": "Access forbidden: Only logged-in users can delete order items"}), HTTP_400_BAD_REQUEST

    order_item = OrderItem.query.get(id)
    if not order_item:
        return jsonify({"message": "Order item not found"}), HTTP_404_NOT_FOUND

    try:
        db.session.delete(order_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the order item", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Order item deleted successfully"}), HTTP_200_OK
