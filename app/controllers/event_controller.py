from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.event import Event
from app.models.user import User
from app.extensions import db
from datetime import datetime

event_bp = Blueprint('event_bp', __name__, url_prefix='/api/v1/event')

# Create an event
@event_bp.route('/create', methods=['POST'])
@jwt_required()
def create_event():
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can create events"}), HTTP_400_BAD_REQUEST

    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    location = data.get('location')

    if not name or not description or not date or not location:
        return jsonify({"message": "All fields (name, description, date, location) are required"}), HTTP_400_BAD_REQUEST

    try:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"message": "Invalid date format (must be YYYY-MM-DD HH:MM:SS)"}), HTTP_400_BAD_REQUEST

    new_event = Event(
        name=name,
        description=description,
        date=date,
        location=location
    )

    try:
        db.session.add(new_event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the event", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Event created successfully"}), HTTP_201_CREATED

# Update an event
@event_bp.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_event(id):
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can update events"}), HTTP_400_BAD_REQUEST

    event = Event.query.get(id)
    if not event:
        return jsonify({"message": "Event not found"}), HTTP_404_NOT_FOUND

    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    location = data.get('location')
    

    if not name or not description or not date or not location :
        return jsonify({"message": "All fields (name, description, date, location) are required"}), HTTP_400_BAD_REQUEST

    try:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({"message": "Invalid date format (must be YYYY-MM-DD HH:MM:SS)"}), HTTP_400_BAD_REQUEST

    event.name = name
    event.description = description
    event.date = date
    event.location = location
    

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the event", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Event updated successfully"}), HTTP_200_OK

# Delete an event
@event_bp.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can delete events"}), HTTP_400_BAD_REQUEST

    event = Event.query.get(id)
    if not event:
        return jsonify({"message": "Event not found"}), HTTP_404_NOT_FOUND

    try:
        db.session.delete(event)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the event", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({"message": "Event deleted successfully"}), HTTP_200_OK
