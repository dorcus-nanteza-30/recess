from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.squad import Squad
from app.models.user import User
from app.extensions import db
from datetime import datetime

squad_bp = Blueprint('squad_bp', __name__, url_prefix='/api/v1/squad')

# Create a squad
@squad_bp.route('/create', methods=['POST'])
@jwt_required()
def create_squad():
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # Check if user is logged in as admin
    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can create squads"}), HTTP_400_BAD_REQUEST

    # Extract data and perform basic validation
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    position = data.get('position')
    jersey_number = data.get('jersey_number')
    biography = data.get('biography')
    image = data.get('image')
    weight = data.get('weight')
    height = data.get('height')
    date_of_birth = data.get('date_of_birth')

    if not first_name or not last_name or not position or not jersey_number or not biography or not image:
        return jsonify({"message": "All fields (first_name, last_name, position, jersey_number, biography, image) are required"}), HTTP_400_BAD_REQUEST

    # Try converting weight and height to numeric values (if present)
    try:
        if weight:
            weight = float(weight)
    except ValueError:
        return jsonify({"message": "Invalid weight format (must be a number)"}), HTTP_400_BAD_REQUEST

    try:
        if height:
            height = float(height)
    except ValueError:
        return jsonify({"message": "Invalid height format (must be a number)"}), HTTP_400_BAD_REQUEST

    # Create a new squad
    new_squad = Squad(
        first_name=first_name,
        last_name=last_name,
        position=position,
        jersey_number=jersey_number,
        biography=biography,
        image=image,
        weight=weight,
        height=height,
        date_of_birth=date_of_birth
    )

    try:
        db.session.add(new_squad)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the squad", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Squad created successfully"}), HTTP_201_CREATED

# Get a squad
@squad_bp.route('/squad/<int:id>', methods=['GET'])
@jwt_required()
def get_squad(id):
    try:
        # Retrieve the squad by ID
        squad = Squad.query.get(id)
        if not squad:
            return jsonify({"error": "Squad not found"}), HTTP_404_NOT_FOUND

        # Ensure date_of_birth is converted to string only if it's a datetime object
        date_of_birth_str = squad.date_of_birth.strftime("%Y-%m-%d") if isinstance(squad.date_of_birth, datetime) else squad.date_of_birth

        # Return squad details
        return jsonify({
            "squad": {
                "id": squad.id,
                "first_name": squad.first_name,
                "last_name": squad.last_name,
                "position": squad.position,
                "jersey_number": squad.jersey_number,
                "biography": squad.biography,
                "image": squad.image,
                "weight": squad.weight,
                "height": squad.height,
                "date_of_birth": date_of_birth_str
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the squad", "details": str(e)}), HTTP_400_BAD_REQUEST

# Get all squads
@squad_bp.route('/squads', methods=['GET'])
@jwt_required()
def get_all_squads():
    try:
        # Retrieve all squads
        squads = Squad.query.all()

        # Convert each squad object to a dictionary for JSON response
        squads_list = []
        for squad in squads:
            date_of_birth_str = squad.date_of_birth.strftime("%Y-%m-%d") if isinstance(squad.date_of_birth, datetime) else squad.date_of_birth
            squads_list.append({
                "id": squad.id,
                "first_name": squad.first_name,
                "last_name": squad.last_name,
                "position": squad.position,
                "jersey_number": squad.jersey_number,
                "biography": squad.biography,
                "image": squad.image,
                "weight": squad.weight,
                "height": squad.height,
                "date_of_birth": date_of_birth_str
            })

        # Return the list of squads
        return jsonify({"squads": squads_list}), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the squads", "details": str(e)}), HTTP_400_BAD_REQUEST

# Update a squad
@squad_bp.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_squad(id):
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # Check if user is logged in as admin
    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can update squads"}), HTTP_400_BAD_REQUEST

    # Retrieve the squad by ID
    squad = Squad.query.get(id)
    if not squad:
        return jsonify({"message": "Squad not found"}), HTTP_404_NOT_FOUND

    # Extract data and perform basic validation
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    position = data.get('position')
    jersey_number = data.get('jersey_number')
    biography = data.get('biography')
    image = data.get('image')
    weight = data.get('weight')
    height = data.get('height')
    date_of_birth = data.get('date_of_birth')

    if not first_name or not last_name or not position or not jersey_number or not biography or not image:
        return jsonify({"message": "All fields (first_name, last_name, position, jersey_number, biography, image) are required"}), HTTP_400_BAD_REQUEST

    # Try converting weight and height to numeric values (if present)
    try:
        if weight:
            weight = float(weight)
    except ValueError:
        return jsonify({"message": "Invalid weight format (must be a number)"}), HTTP_400_BAD_REQUEST

    try:
        if height:
            height = float(height)
    except ValueError:
        return jsonify({"message": "Invalid height format (must be a number)"}), HTTP_400_BAD_REQUEST

    # Update the squad
    squad.first_name = first_name
    squad.last_name = last_name
    squad.position = position
    squad.jersey_number = jersey_number
    squad.biography = biography
    squad.image = image
    squad.weight = weight
    squad.height = height

    if date_of_birth:
        try:
            # Parse the date_of_birth into a datetime object
            squad.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Invalid date_of_birth format (must be YYYY-MM-DD)"}), HTTP_400_BAD_REQUEST

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the squad", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Squad updated successfully"}), HTTP_200_OK

# Delete a squad
@squad_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_squad(id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can delete squads"}), HTTP_400_BAD_REQUEST

    squad = Squad.query.get(id)
    if not squad:
        return jsonify({"message": "Squad not found"}), HTTP_404_NOT_FOUND

    try:
        db.session.delete(squad)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the squad", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Squad deleted successfully"}), HTTP_200_OK