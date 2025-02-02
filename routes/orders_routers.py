from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db_manager import SessionLocal
from models.orders import Order, OrderDetails
from models.products import Product
from models.users import User
from routes.auth_routes import check_admin
from sqlalchemy import func

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    session = SessionLocal()

    try:

        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        orders = session.query(Order).all()

        order_counts = (session.query(Order.status, func.count(Order.id).label("count"))
                        .group_by(Order.status).all())

        status_counts = {f"{status}: ": count for status, count in order_counts}

        return jsonify({
            "total_orders": len(orders),
            "order_status_counts": status_counts,
            "orders": [order.to_dict() for order in orders]
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@orders_bp.route('/orders/<string:status>', methods=['GET'])
@jwt_required()
def get_orders_by_status(status):
    session = SessionLocal()
    try:
        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        valid_statuses = ["pending", "shipped", "delivered", "cancelled"]
        if status not in valid_statuses:
            return jsonify({"error": f"Invalid status. Allowed values: {valid_statuses}"}), 400

        orders = session.query(Order).filter(Order.status == status).all()
        return jsonify({
            "status": status,
            "total_orders": len(orders),
            "orders": [order.to_dict() for order in orders]
        }), 200


    finally:
        session.close()


@orders_bp.route('/orders_details/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_analyitics(product_id):
    session = SessionLocal()
    try:

        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        analytics_product = (session.query(
            func.count(OrderDetails.id).label('total_orders'),
            func.sum(OrderDetails.price).label('total_revenue'),
            func.avg(OrderDetails.price).label('average_revenue'),
            Product.model.label('product_name'))
                             .join(Product, Product.id == OrderDetails.product_id)
                             .join(Order, Order.id == OrderDetails.order_id)
                             .filter(OrderDetails.product_id == product_id)
                             .filter(Order.status != "cancelled"))

        result = analytics_product.one_or_none()

        if not result:
            return jsonify({"error": "Product not found or no orders for this product"}), 404

        return jsonify({
            "product_id": product_id,
            "product_name": result.product_name,
            "total_orders": result.total_orders or 0,
            "total_revenue": round(float(result.total_revenue or 0.0), 2),
            "average_revenue": round(float(result.average_revenue or 0.0), 2)
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@orders_bp.route('/orders/best_buyer', methods=['GET'])
@jwt_required()
def get_best_buyer():
    session = SessionLocal()
    try:
        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        best_buyer = (session.query(
            User,
            func.count(Order.id).label('total_orders'))
                      .join(Order, User.id == Order.user_id)
                      .group_by(User.id)
                      .order_by(func.count(Order.id).desc())
                      .first())

        if not best_buyer:
            return jsonify({"message": "No users with orders found"}), 404

        user, total_orders = best_buyer

        return jsonify({
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "total_orders": total_orders
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@orders_bp.route('/orders/user_orders', methods=['GET'])
@jwt_required()
def get_orders_per_user():
    session = SessionLocal()
    try:
        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        user_orders = (session.query(
            User.id, User.username,
            func.count(Order.id).label('total_orders'))
                       .join(Order, User.id == Order.user_id)
                       .group_by(User.id)
                       .all())

        return jsonify([
            {"user_id": row.id, "username": row.username, "total_orders": row.total_orders}
            for row in user_orders
        ]), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@orders_bp.route('/orders/average_orders', methods=['GET'])
@jwt_required()
def get_average_orders_per_user():
    session = SessionLocal()
    try:
        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        # Calculate number of orders per user
        user_order_counts = (session.query(
            User.id, func.count(Order.id).label("order_count"))
                             .join(Order, User.id == Order.user_id)
                             .group_by(User.id).subquery())  # Transform query in subquery

        # Calculate the avg count of users' order
        avg_orders = session.query(func.avg(user_order_counts.c.order_count)).scalar()

        return jsonify({
            "average_orders_per_user": round(avg_orders, 2) if avg_orders else 0
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()


@orders_bp.route('/orders/month', methods=['GET'])
@jwt_required()
def get_revenue_per_month():
    session = SessionLocal()
    try:
        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        revenue_per_month = (session.query(
            func.strftime('%Y-%m', Order.created_at).label('month'),
            func.sum(OrderDetails.price * OrderDetails.quantity).label('total_revenue'))
                             .join(OrderDetails, Order.id == OrderDetails.order_id)
                             .group_by(func.strftime('%Y-%m', Order.created_at))
                             .order_by(func.strftime('%Y-%m', Order.created_at))
                             .all())

        return jsonify([
            {"month": row.month, "total_revenue": round(row.total_revenue, 2)}
            for row in revenue_per_month
        ]), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()
