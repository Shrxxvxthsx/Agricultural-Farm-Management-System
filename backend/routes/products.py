from flask import Blueprint, jsonify, request
from models import db, Product
from sqlalchemy import or_

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    try:
        # Get query parameters
        category = request.args.get('category')
        search = request.args.get('search')
        sort = request.args.get('sort')
        
        # Start with base query
        query = Product.query
        
        # Apply category filter
        if category:
            query = query.filter(Product.category == category)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Apply sorting
        if sort:
            if sort == 'price-low':
                query = query.order_by(Product.price.asc())
            elif sort == 'price-high':
                query = query.order_by(Product.price.desc())
            elif sort == 'name':
                query = query.order_by(Product.name.asc())
        else:
            # Default sort by name
            query = query.order_by(Product.name.asc())
        
        # Execute query
        products = query.all()
        
        # Convert to dict
        result = [product.to_dict() for product in products]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@products_bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        return jsonify(product.to_dict())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@products_bp.route('/featured', methods=['GET'])
def get_featured_products():
    try:
        # In a real app, you might have a featured flag or use other criteria
        # For now, just return the first 3 products
        products = Product.query.limit(3).all()
        
        result = [product.to_dict() for product in products]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@products_bp.route('/', methods=['POST'])
def create_product():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'price', 'category']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new product
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=data['price'],
            category=data['category'],
            stock_quantity=data.get('stock_quantity', 0),
            image_url=data.get('image_url')
        )
        
        # Save to database
        db.session.add(product)
        db.session.commit()
        
        return jsonify(product.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@products_bp.route('/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        data = request.json
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'price' in data:
            product.price = data['price']
        if 'category' in data:
            product.category = data['category']
        if 'stock_quantity' in data:
            product.stock_quantity = data['stock_quantity']
        if 'image_url' in data:
            product.image_url = data['image_url']
        
        # Save changes
        db.session.commit()
        
        return jsonify(product.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@products_bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({"message": "Product deleted successfully"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
