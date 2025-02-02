from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db_manager import SessionLocal
from models.users import User

users_bp = Blueprint("users", __name__)

@users_bp.route("/users", methods=["GET"])
def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return jsonify([user.to_dict() for user in users])

@users_bp.route("/users", methods=["POST"])
@jwt_required()
def add_user():
    session = SessionLocal()

    try:
        data = request.get_json()
        current_user_email = get_jwt_identity()
        current_user = session.query(User).filter_by(email=current_user_email).first()

        if not current_user or not current_user.is_admin:
            return jsonify({"error": "Access deny. Only admin can create users."}), 403

        required_fields = ["email", "username", "firstname", "lastname", "password"]
        for field in required_fields:
            if field not in data:
                return jsonify({"message": "Required {field} are missing"}), 400

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
        return jsonify({"message": "User added"}), 201

    except Exception as e:
        session.rollback()  # Annulla le modifiche in caso di errore
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@users_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def modify_user(user_id):
    session = SessionLocal()
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400  # Se il corpo della richiesta è vuoto

        current_user_email = get_jwt_identity()
        current_user = session.query(User).filter_by(email=current_user_email).first()

        if not current_user or not current_user.is_admin:
            return jsonify({"error": "Access denied. Only admins can modify users."}), 403

        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Aggiorna solo i campi forniti
        user.firstname = data.get("firstname", user.firstname)
        user.lastname = data.get("lastname", user.lastname)
        user.username = data.get("username", user.username)
        user.email = data.get("email", user.email)

        session.commit()

        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        session.rollback()  # Annulla le modifiche in caso di errore
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    session = SessionLocal()

    try:
        current_user_email = get_jwt_identity()
        current_user = session.query(User).filter_by(email=current_user_email).first()

        # Check if the user is admin
        if not current_user or not current_user.is_admin:
            return jsonify({"error": "Access denied. Only admins can delete users."}), 403

        # Check if the user exist
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        session.delete(user)
        session.commit()

        return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        session.rollback()  # Annulla le modifiche in caso di errore
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()  # Close the session

