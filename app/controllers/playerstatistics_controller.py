from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_200_OK
from app.models.playerstatistics import PlayerStatistic
from app.models.squad import Squad
from app.models.user import User
from app.extensions import db

playerstatistics_bp = Blueprint('playerstatistics_bp', __name__, url_prefix='/api/v1/playerstatistics')

# Create player statistics
@playerstatistics_bp.route('/create', methods=['POST'])
@jwt_required()
def create_player_statistic():
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can create player statistics"}), HTTP_400_BAD_REQUEST

    squad_id = data.get('squad_id')
    matches_played = data.get('matches_played')

    if not squad_id or not matches_played:
        return jsonify({"message": "Required fields (squad_id, matches_played) are missing"}), HTTP_400_BAD_REQUEST

    squad = Squad.query.get(squad_id)
    if not squad:
        return jsonify({"message": "Squad not found"}), HTTP_404_NOT_FOUND

    try:
        new_statistic = PlayerStatistic(
            squad_id=squad_id,
            matches_played=int(matches_played),
            tries_scored=int(data.get('tries_scored', 0)),
            conversions=int(data.get('conversions', 0)),
            penalties=int(data.get('penalties', 0)),
            yellow_cards=int(data.get('yellow_cards', 0)),
            red_cards=int(data.get('red_cards', 0)),
            minutes_played=int(data.get('minutes_played', 0))
        )

        db.session.add(new_statistic)
        db.session.commit()
        return jsonify({"message": "Player statistic created successfully"}), HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while creating the player statistic", "details": str(e)}), HTTP_400_BAD_REQUEST


# Get player statistic by squad ID
@playerstatistics_bp.route('/squad/<int:squad_id>', methods=['GET'])
@jwt_required()
def get_player_statistics_by_squad(squad_id):
    try:
        squad = Squad.query.get(squad_id)
        if not squad:
            return jsonify({"error": "Squad not found"}), HTTP_404_NOT_FOUND

        statistics = PlayerStatistic.query.filter_by(squad_id=squad_id).all()
        if not statistics:
            return jsonify({"error": "No player statistics found for this squad"}), HTTP_404_NOT_FOUND

        statistics_list = [
            {
                "id": stat.id,
                "squad_id": stat.squad_id,
                "matches_played": stat.matches_played,
                "tries_scored": stat.tries_scored,
                "conversions": stat.conversions,
                "penalties": stat.penalties,
                "yellow_cards": stat.yellow_cards,
                "red_cards": stat.red_cards,
                "minutes_played": stat.minutes_played
            } for stat in statistics
        ]

        return jsonify({"statistics": statistics_list}), HTTP_200_OK
    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the player statistics", "details": str(e)}), HTTP_400_BAD_REQUEST

# Get all player statistics by squad id 
@playerstatistics_bp.route('/playerstatistics', methods=['GET'])
@jwt_required()
def get_all_player_statistics():
    try:
        statistics = PlayerStatistic.query.all()
        statistics_list = [
            {
                "id": statistic.id,
                "squad_id": statistic.squad_id,
                "matches_played": statistic.matches_played,
                "tries_scored": statistic.tries_scored,
                "conversions": statistic.conversions,
                "penalties": statistic.penalties,
                "yellow_cards": statistic.yellow_cards,
                "red_cards": statistic.red_cards,
                "minutes_played": statistic.minutes_played
            } for statistic in statistics
        ]

        return jsonify({"statistics": statistics_list}), HTTP_200_OK
    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the player statistics", "details": str(e)}), HTTP_400_BAD_REQUEST

# Update player statistic by squad ID
@playerstatistics_bp.route('/edit/squad/<int:squad_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_player_statistics_by_squad(squad_id):
    data = request.json
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can update player statistics"}), HTTP_400_BAD_REQUEST

    squad = Squad.query.get(squad_id)
    if not squad:
        return jsonify({"message": "Squad not found"}), HTTP_404_NOT_FOUND

    statistics = PlayerStatistic.query.filter_by(squad_id=squad_id).all()
    if not statistics:
        return jsonify({"message": "No player statistics found for this squad"}), HTTP_404_NOT_FOUND

    updated_stats = []
    for stat in statistics:
        for field in ['matches_played', 'tries_scored', 'conversions', 'penalties', 'yellow_cards', 'red_cards', 'minutes_played']:
            if field in data:
                try:
                    setattr(stat, field, int(data[field]))
                except ValueError:
                    return jsonify({"message": f"Invalid value for {field} (must be a number)"}), HTTP_400_BAD_REQUEST
        updated_stats.append(stat)

    try:
        db.session.commit()
        return jsonify({"message": "Player statistics updated successfully", "statistics": updated_stats}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while updating the player statistics", "details": str(e)}), HTTP_400_BAD_REQUEST

# Delete player statistics by squad ID
@playerstatistics_bp.route('/delete/squad/<int:squad_id>', methods=['DELETE'])
@jwt_required()
def delete_player_statistics_by_squad(squad_id):
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    if not current_user or current_user.user_type != 'admin':
        return jsonify({"message": "Access forbidden: Only admins can delete player statistics"}), HTTP_400_BAD_REQUEST

    squad = Squad.query.get(squad_id)
    if not squad:
        return jsonify({"message": "Squad not found"}), HTTP_404_NOT_FOUND

    statistics = PlayerStatistic.query.filter_by(squad_id=squad_id).all()
    if not statistics:
        return jsonify({"message": "No player statistics found for this squad"}), HTTP_404_NOT_FOUND

    try:
        for stat in statistics:
            db.session.delete(stat)
        db.session.commit()
        return jsonify({"message": "Player statistics deleted successfully"}), HTTP_200_OK
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the player statistics", "details": str(e)}), HTTP_400_BAD_REQUEST
