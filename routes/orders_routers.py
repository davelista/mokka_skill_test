from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.db_manager import SessionLocal
from models.orders import Order, OrderDetails
from models.products import Product
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

        order_counts = session.query(Order.status, func.count(Order.id).label("count")
                                     ).group_by(Order.status).all()

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

        analytics_product = session.query(
            func.count(OrderDetails.id).label('total_orders'),
            func.sum(OrderDetails.price).label('total_revenue'),
            func.avg(OrderDetails.price).label('average_revenue'),
            Product.model.label('product_name')
        ).join(Product, Product.id == OrderDetails.product_id) \
        .join(Order, Order.id == OrderDetails.order_id) \
        .filter(OrderDetails.product_id == product_id) \
        .filter(Order.status != "cancelled")

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

