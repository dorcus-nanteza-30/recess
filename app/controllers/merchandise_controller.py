from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.merchandise import Merchandise
from app.models.user import User
from app.extensions import db

merchandise_bp = Blueprint('merchandise_bp', __name__, url_prefix='/api/v1/merchandise')

# Create merchandise
@merchandise_bp.route('/create', methods=['POST'])
@jwt_required()
def create_merchandise():
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # Check if user is logged in as admin
    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can create merchandise"}), HTTP_400_BAD_REQUEST

    # Extract data and perform basic validation
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')
    image = data.get('image')
    category = data.get('category')

    if not name or not description or not price or not stock or not image or not category:
        return jsonify({"message": "All fields (name, description, price, stock, image, category) are required"}), HTTP_400_BAD_REQUEST

    try:
        price = float(price)
    except ValueError:
        return jsonify({"message": "Invalid price format (must be a number)"}), HTTP_400_BAD_REQUEST

    try:
        stock = int(stock)
    except ValueError:
        return jsonify({"message": "Invalid stock format (must be an integer)"}), HTTP_400_BAD_REQUEST

    # Create new merchandise
    new_merchandise = Merchandise(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image=image,
        category=category
    )

    try:
        db.session.add(new_merchandise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the merchandise", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Merchandise created successfully"}), HTTP_201_CREATED

# Get a merchandise item
@merchandise_bp.route('/merchandise/<int:id>', methods=['GET'])
@jwt_required()
def get_merchandise(id):
    try:
        merchandise = Merchandise.query.get(id)
        if not merchandise:
            return jsonify({"error": "Merchandise not found"}), HTTP_404_NOT_FOUND

        return jsonify({
            "merchandise": {
                "id": merchandise.id,
                "name": merchandise.name,
                "description": merchandise.description,
                "price": merchandise.price,
                "stock": merchandise.stock,
                "image": merchandise.image,
                "category": merchandise.category
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the merchandise", "details": str(e)}), HTTP_400_BAD_REQUEST

# Get all merchandise items
@merchandise_bp.route('/merchandise', methods=['GET'])
@jwt_required()
def get_all_merchandise():
    try:
        merchandises = Merchandise.query.all()
        merchandise_list = [{
            "id": merchandise.id,
            "name": merchandise.name,
            "description": merchandise.description,
            "price": merchandise.price,
            "stock": merchandise.stock,
            "image": merchandise.image,
            "category": merchandise.category
        } for merchandise in merchandises]

        return jsonify({"merchandises": merchandise_list}), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the merchandise", "details": str(e)}), HTTP_400_BAD_REQUEST

# Update a merchandise item
@merchandise_bp.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_merchandise(id):
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # Check if user is logged in as admin
    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can update merchandise"}), HTTP_400_BAD_REQUEST

    # Retrieve the merchandise by ID
    merchandise = Merchandise.query.get(id)
    if not merchandise:
        return jsonify({"message": "Merchandise not found"}), HTTP_404_NOT_FOUND

    # Extract data and perform basic validation
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')
    image = data.get('image')
    category = data.get('category')

    if not name or not description or not price or not stock or not image or not category:
        return jsonify({"message": "All fields (name, description, price, stock, image, category) are required"}), HTTP_400_BAD_REQUEST

    try:
        price = float(price)
    except ValueError:
        return jsonify({"message": "Invalid price format (must be a number)"}), HTTP_400_BAD_REQUEST

    try:
        stock = int(stock)
    except ValueError:
        return jsonify({"message": "Invalid stock format (must be an integer)"}), HTTP_400_BAD_REQUEST

    # Update the merchandise
    merchandise.name = name
    merchandise.description = description
    merchandise.price = price
    merchandise.stock = stock
    merchandise.image = image
    merchandise.category = category

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the merchandise", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Merchandise updated successfully"}), HTTP_200_OK

# Delete a merchandise item
@merchandise_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_merchandise(id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can delete merchandise"}), HTTP_400_BAD_REQUEST

    merchandise = Merchandise.query.get(id)
    if not merchandise:
        return jsonify({"message": "Merchandise not found"}), HTTP_404_NOT_FOUND

    try:
        db.session.delete(merchandise)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the merchandise", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Merchandise deleted successfully"}), HTTP_200_OK
