from flask import Blueprint, request, jsonify
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.contact import Contact
from app.extensions import db
import validators

contact_bp = Blueprint('contact_bp', __name__, url_prefix='/api/v1/contacts')

# create contact
@contact_bp.route('/create', methods=['POST'])
def create_contact():
    data = request.json

    # Extract fields
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    user_id = data.get('user_id')  # Optional: Extract user_id if provided

    # Validate input
    if not name or not email or not message:
        return jsonify({"error": "Name, email, and message are required"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error": "Invalid email address"}), HTTP_400_BAD_REQUEST

    try:
        new_contact = Contact(name=name, email=email, message=message, user_id=user_id)
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the contact", "details": str(e)}), 400

    return jsonify({
        "message": "Contact created successfully",
        "contact": {
            "id": new_contact.id,
            "name": new_contact.name,
            "email": new_contact.email,
            "message": new_contact.message,
            "date": new_contact.date.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": new_contact.user_id
        }
    }), HTTP_200_OK

# update contact
@contact_bp.route('edit/<int:id>', methods=['PUT', 'PATCH'])
def update_contact(id):
    data = request.json

    try:
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"error": "Contact not found"}), HTTP_404_NOT_FOUND

        # Update fields if present
        if 'name' in data:
            contact.name = data['name']
        if 'email' in data:
            if not validators.email(data['email']):
                return jsonify({"error": "Invalid email address"}), HTTP_400_BAD_REQUEST
            contact.email = data['email']
        if 'message' in data:
            contact.message = data['message']

        db.session.commit()

        return jsonify({
            "message": "Contact updated successfully",
            "contact": {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "message": contact.message,
                "date": contact.date.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the contact", "details": str(e)}), HTTP_400_BAD_REQUEST

#delete a contact
@contact_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_contact(id):
    try:
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"error": "Contact not found"}), HTTP_404_NOT_FOUND

        db.session.delete(contact)
        db.session.commit()

        return jsonify({"message": "Contact deleted successfully"}), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the contact", "details": str(e)}), HTTP_400_BAD_REQUEST


# get all contact
@contact_bp.route('/', methods=['GET'])
def get_all_contacts():
    try:
        contacts = Contact.query.all()

        contacts_data = []

        for contact in contacts:
            contact_info = {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "message": contact.message,
                "date": contact.date.strftime("%Y-%m-%d %H:%M:%S")
            }
            contacts_data.append(contact_info)

        return jsonify({"contacts": contacts_data}), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving contacts", "details": str(e)}), HTTP_400_BAD_REQUEST


#get a contact
@contact_bp.route('/<int:id>', methods=['GET'])
def get_contact(id):
    try:
        contact = Contact.query.get(id)
        if not contact:
            return jsonify({"error": "Contact not found"}), HTTP_404_NOT_FOUND

        return jsonify({
            "contact": {
                "id": contact.id,
                "name": contact.name,
                "email": contact.email,
                "message": contact.message,
                "date": contact.date.strftime("%Y-%m-%d %H:%M:%S")
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the contact", "details": str(e)}), HTTP_400_BAD_REQUEST
