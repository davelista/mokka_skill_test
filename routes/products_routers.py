from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from models.db_manager import  SessionLocal
from models.products import Product
from models.orders import Order, OrderDetails
from routes.auth_routes import check_admin

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    session = SessionLocal()
    products = session.query(Product).all()
    session.close()
    return jsonify([product.to_dict() for product in products])

@products_bp.route('/products/top_revenue', methods=['GET'])
@jwt_required()
def get_top_revenue_product():

    session = SessionLocal()

    try:
        is_admin = check_admin()
        if isinstance(is_admin, tuple):
            return is_admin

        top_revenue_product = (session.query(
            Product,
            func.sum(OrderDetails.price * OrderDetails.quantity).label('total_revenue'))
                               .join(OrderDetails, Product.id == OrderDetails.product_id)
                               .join(Order, Order.id == OrderDetails.order_id)
                               .filter(Order.status != "cancelled")
                               .group_by(Product.id)
                               .order_by(func.sum(OrderDetails.price * OrderDetails.quantity).desc())
                               .first())

        if not top_revenue_product:
            return jsonify({"message": "No products with revenue yet"}), 404

        product, total_revenue = top_revenue_product

        return jsonify({
            "product_id": product.id,
            "product_name": product.model,
            "total_revenue": round(total_revenue, 2)
        }), 200

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session.close()
