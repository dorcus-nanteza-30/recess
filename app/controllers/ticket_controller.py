from flask import Blueprint, request, jsonify
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND,HTTP_200_OK
from app.extensions import db
from app.models.ticket import Ticket
from flask_jwt_extended import jwt_required

ticket_bp = Blueprint('ticket_bp', __name__, url_prefix='/api/v1/ticket')


#create a ticket
@ticket_bp.route('/create', methods=['POST'])
@jwt_required()  # Ensure the user is authenticated
def create_ticket():
    data = request.get_json()
    try:
        event_id = data['event_id']
        price = data['price']
        section = data['section']
        row = data['row']
        seat = data['seat']
        
        new_ticket = Ticket(event_id=event_id, price=price, section=section, row=row, seat=seat)
        db.session.add(new_ticket)
        db.session.commit()
        
        return jsonify({"message": "Ticket created successfully", "ticket": repr(new_ticket)}), HTTP_201_CREATED
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), HTTP_400_BAD_REQUEST
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST

@ticket_bp.route('/tickets/<int:ticket_id>', methods=['DELETE'])
@jwt_required()  # Ensure the user is authenticated
def delete_ticket(ticket_id):
    try:
        ticket = Ticket.query.get_or_404(ticket_id)
        db.session.delete(ticket)
        db.session.commit()
        
        return jsonify({"message": "Ticket deleted successfully"}), HTTP_201_CREATED
    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_400_BAD_REQUEST
