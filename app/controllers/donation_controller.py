from flask import Blueprint, request, jsonify
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.user import User
from app.models.donation import Donation
from app.extensions import db
from datetime import datetime

donation_bp = Blueprint('donation_bp', __name__, url_prefix='/api/v1/donation')


# Create a donation (without JWT authentication)
@donation_bp.route('/create', methods=['POST'])
def create_donation():
    data = request.json

    amount = data.get('amount')
    message = data.get('description')  # Use 'description' field from JSON data
    name = data.get('name')
    contact = data.get('contact')
    user_id = data.get('user_id')  # Extract 'user_id' from JSON data

    if not amount or not name or not user_id:
        return jsonify({"error": "Amount, name, and user ID are required"}), HTTP_400_BAD_REQUEST

    try:
        new_donation = Donation(
            user_id=user_id,
            amount=amount,
            name=name,
            message=message,
            contact=contact
        )

        db.session.add(new_donation)
        db.session.commit()

        return jsonify({
            "message": "Donation created successfully",
            "donation": {
                "id": new_donation.id,
                "amount": new_donation.amount,
                "message": new_donation.message,
                "date": new_donation.donation_date.strftime("%Y-%m-%d"),
                "user_id": new_donation.user_id,
                "name": new_donation.name,
                "contact": new_donation.contact
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the donation", "details": str(e)}), HTTP_400_BAD_REQUEST
# Update a donation (without JWT authentication)
@donation_bp.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
def update_donation(id):
    data = request.json

    amount = data.get('amount')
    message = data.get('message')  # Change 'description' to 'message'
    name = data.get('name')
    contact = data.get('contact')

    try:
        donation = Donation.query.get(id)
        if not donation:
            return jsonify({"error": "Donation not found"}), HTTP_404_NOT_FOUND

        if amount:
            donation.amount = amount
        if message:
            donation.message = message
        if name:
            donation.name = name
        if contact:
            donation.contact = contact

        db.session.commit()

        return jsonify({
            "message": "Donation updated successfully",
            "donation": {
                "id": donation.id,
                "amount": donation.amount,
                "message": donation.message,  # Include 'message' in response
                "date": donation.donation_date.strftime("%Y-%m-%d"),
                "user_id": donation.user_id,
                "name": donation.name,
                "contact": donation.contact
            }
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the donation", "details": str(e)}), HTTP_400_BAD_REQUEST

# Delete a donation (without JWT authentication)
@donation_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_donation(id):
    try:
        donation = Donation.query.get(id)
        if not donation:
            return jsonify({"error": "Donation not found"}), HTTP_404_NOT_FOUND

        db.session.delete(donation)
        db.session.commit()

        return jsonify({"message": "Donation deleted successfully"}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the donation", "details": str(e)}), HTTP_400_BAD_REQUEST

# Get all donations (without JWT authentication)
@donation_bp.route('/', methods=['GET'])
def get_all_donations():
    try:
        donations = Donation.query.all()

        donations_data = []
        for donation in donations:
            donations_data.append({
                "id": donation.id,
                "amount": donation.amount,
                "message": donation.message,  # Include 'message' in response
                "date": donation.donation_date.strftime("%Y-%m-%d"),
                "user_id": donation.user_id,
                "name": donation.name,
                "contact": donation.contact
            })

        return jsonify({"donations": donations_data}), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving donations", "details": str(e)}), HTTP_400_BAD_REQUEST
