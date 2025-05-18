from flask import Flask, render_template, jsonify, request, send_from_directory
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, 
            static_folder='../frontend/static',
            template_folder='../frontend/templates')

# Enable CORS
CORS(app)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import routes after db is initialized to avoid circular imports
from routes.products import products_bp
from routes.farm import farm_bp
from routes.users import users_bp

# Register blueprints
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(farm_bp, url_prefix='/api/farm')
app.register_blueprint(users_bp, url_prefix='/api/users')

# Serve frontend static files
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Serve frontend HTML pages
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/products')
def products():
    return send_from_directory('../frontend', 'products.html')

@app.route('/farm-management')
def farm_management():
    return send_from_directory('../frontend', 'farm-management.html')

@app.route('/cart')
def cart():
    return send_from_directory('../frontend', 'cart.html')

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the app
    app.run(debug=os.getenv('FLASK_ENV') == 'development', host='0.0.0.0')
