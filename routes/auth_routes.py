from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from models.db_manager import SessionLocal
from models.users import User

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session = SessionLocal()
        data = request.get_json()

        user = session.query(User).filter_by(email=data['email']).first()

        if user:
            if user.check_password(data['password']):
                print("DEBUG: correct password")
                # Generate JWT token
                access_token = create_access_token(identity=user.email)
                return jsonify(access_token=access_token), 200
            else:
                return jsonify({'message': 'wrong password'}), 401
        return jsonify({"error": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "Login page"}), 200