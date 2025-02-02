from flask import Blueprint, jsonify, request
from models.db_manager import  SessionLocal
from models.products import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/products', methods=['GET'])
def get_products():
    session = SessionLocal()
    products = session.query(Product).all()
    session.close()
    return jsonify([product.to_dict() for product in products])