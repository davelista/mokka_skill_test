from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from models.db_manager import SessionLocal
from models.users import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return jsonify([user.__dict__ for user in users])

@users_bp.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    session = SessionLocal()
    new_user = User(
        email=data["email"],
        username=data["username"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        is_admin=data.get("is_admin", 0)
    )
    new_user.set_password(data["password"])

    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({"message": "Utente aggiunto"}), 201

@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def modify_user(user_id):
    data = request.get_json()
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "Utente non trovato"}), 404
    user.firstname = data.get("firstname", user.firstname)
    user.lastname = data.get("lastname", user.lastname)
    session.commit()
    session.close()
    return jsonify({"message": "Utente aggiornato"})

@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "Utente non trovato"}), 404
    session.delete(user)
    session.commit()
    session.close()
    return jsonify({"message": "Utente eliminato"})
