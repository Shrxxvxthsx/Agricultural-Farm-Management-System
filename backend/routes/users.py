from flask import Blueprint, jsonify, request
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
import re

users_bp = Blueprint('users', __name__)

@users_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Validate email format
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, data['email']):
            return jsonify({"error": "Invalid email format"}), 400
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 409
        
        # Validate password strength
        if len(data['password']) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data.get('role', 'Farmer')
        )
        
        # Save to database
        db.session.add(user)
        db.session.commit()
        
        # Return user data without password
        return jsonify(user.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        
        # Check if user exists and password is correct
        if not user or not check_password_hash(user.password_hash, data['password']):
            return jsonify({"error": "Invalid email or password"}), 401
        
        # In a real app, you would generate a JWT token here
        # For simplicity, we'll just return the user data
        return jsonify({
            "message": "Login successful",
            "user": user.to_dict()
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify(user.to_dict())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        data = request.json
        
        # Update fields
        if 'name' in data:
            user.name = data['name']
        
        if 'email' in data:
            # Validate email format
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, data['email']):
                return jsonify({"error": "Invalid email format"}), 400
            
            # Check if email already exists for another user
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user and existing_user.id != user_id:
                return jsonify({"error": "Email already registered"}), 409
            
            user.email = data['email']
        
        if 'password' in data:
            # Validate password strength
            if len(data['password']) < 8:
                return jsonify({"error": "Password must be at least 8 characters long"}), 400
            
            user.password_hash = generate_password_hash(data['password'])
        
        if 'role' in data:
            user.role = data['role']
        
        # Save changes
        db.session.commit()
        
        return jsonify(user.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
