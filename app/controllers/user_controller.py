from flask import Blueprint, request, jsonify
from app.statuscodes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_404_NOT_FOUND,HTTP_200_OK
from app.models.user import User
from app.extensions import db, bcrypt
import validators
from flask_jwt_extended import create_access_token,jwt_required, get_jwt_identity, unset_jwt_cookies
from datetime import datetime



# user blueprint
user_bp = Blueprint('user_bp', __name__, url_prefix='/api/v1/user')

# Define user roles
USER_ROLES = ['user', 'admin']

# Admin default credentials
ADMIN_EMAIL = "admin@default.com"
ADMIN_PASSWORD = "admin@default.com"


# Define user roles (replace with your actual roles)
USER_ROLES = ['user', 'admin']


# Admin default credentials (replace with secure values)
ADMIN_EMAIL = "admin@default.com",
ADMIN_PASSWORD = "AdminPass123"

 
# user registration
@user_bp.route('/register', methods=['POST'])
def register_user():
    data = request.json

    # Extracting fields
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    join_date = data.get('join_date')
    membership_status = data.get('membership_status')
    user_type = data.get('user_type')  # Corrected user_type extraction

    # Validation
    if not first_name or not last_name or not contact or not email or not password or not join_date or not membership_status or not user_type:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), HTTP_400_BAD_REQUEST
    if not validators.email(email):
        return jsonify({"error": "Invalid email address"}), HTTP_400_BAD_REQUEST

    # Check if user already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "Email already exists"}), HTTP_400_BAD_REQUEST

    # Hashing the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Creating a new user
    try:
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            email=email,
            password=hashed_password,
            join_date=join_date,
            membership_status=membership_status,
            user_type=user_type
        )
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while creating the user", "details": str(e)}), HTTP_400_BAD_REQUEST

    return jsonify({
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "join_date": new_user.join_date,
            "membership_status": new_user.membership_status,
            "user_type": new_user.user_type  # Added user_type in response
        }
    }), HTTP_201_CREATED

# User login
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.json

    # Extract credentials
    email = data.get('email')
    password = data.get('password')

    # Validate input
    if not email or not password:
        return jsonify({"error": "Email and password are required"}), HTTP_400_BAD_REQUEST

    # Check for default admin credentials
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        user = User.query.filter_by(email=ADMIN_EMAIL).first()
        if not user:
            # Create admin user if it doesn't exist
            try:
                user = User(
                    first_name="Admin",  # Provide a default name for admin
                    last_name="User",
                    contact="0000000000",  # Provide a default contact for admin
                    email=ADMIN_EMAIL,
                    password=bcrypt.generate_password_hash(ADMIN_PASSWORD).decode('utf-8'),
                    join_date=datetime.utcnow(),  # Use current date as join_date
                    membership_status="Active",  # Provide a default status
                    user_type='admin'
                )
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({"error": "An error occurred while creating the admin user", "details": str(e)}), HTTP_400_BAD_REQUEST

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), HTTP_400_BAD_REQUEST

    # Create access token
    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "User logged in successfully",
        "user": {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "join_date": user.join_date.strftime("%Y-%m-%d"),
            "membership_status": user.membership_status,
            "user_type": user.user_type
        },
        "access_token": access_token
    }), HTTP_200_OK



# get a user
@user_bp.route('/user/<int:id>', methods=['GET'])
@jwt_required()  # Requires a valid access token to access this route
def get_user(id):
    try:
        # Retrieve the user by ID
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), HTTP_404_NOT_FOUND

        # Ensure join_date is converted to string only if it's a datetime object
        join_date_str = user.join_date.strftime("%Y-%m-%d") if isinstance(user.join_date, datetime) else user.join_date

        # Return user details
        return jsonify({
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "contact": user.contact,
                "email": user.email,
                "join_date": join_date_str,
                "membership_status": user.membership_status,
                "user_type": user.user_type
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the user", "details": str(e)}), HTTP_400_BAD_REQUEST

# get all users
@user_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        # Retrieve all users
        users = User.query.all()

        users_data = []

        for user in users:
            # Convert join_date to string if it's a datetime object
            join_date_str = user.join_date.strftime("%Y-%m-%d") if isinstance(user.join_date, datetime) else user.join_date

            user_info = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "contact": user.contact,
                "email": user.email,
                "join_date": join_date_str,
                "membership_status": user.membership_status,
                "user_type": user.user_type
            }

            users_data.append(user_info)

        return jsonify({"users": users_data}), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving users", "details": str(e)}), HTTP_400_BAD_REQUEST
# update a user
@user_bp.route('/edit/<int:id>', methods=['PUT','PATCH'])
@jwt_required()
def update_user(id):
    data = request.json

    try:
        # Retrieve the user by ID
        user = User.query.get(id)
        if not user:
            return jsonify({"error": "User not found"}), HTTP_404_NOT_FOUND

        # Extract and validate fields if present
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'contact' in data:
            user.contact = data['contact']
        if 'email' in data:
            if not validators.email(data['email']):
                return jsonify({"error": "Invalid email address"}), HTTP_400_BAD_REQUEST
            user.email = data['email']
        if 'password' in data:
            if len(data['password']) < 8:
                return jsonify({"error": "Password must be at least 8 characters long"}), HTTP_400_BAD_REQUEST
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        if 'join_date' in data:
            user.join_date = data['join_date']  # Assuming join_date is provided in a correct format
        if 'membership_status' in data:
            user.membership_status = data['membership_status']
        if 'user_type' in data:
            user.user_type = data['user_type']

        # Commit changes to the database
        db.session.commit()

        return jsonify({
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "contact": user.contact,
                "email": user.email,
                "join_date": user.join_date.strftime("%Y-%m-%d"),
                "membership_status": user.membership_status,
                "user_type": user.user_type
            }
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the user", "details": str(e)}), HTTP_400_BAD_REQUEST
