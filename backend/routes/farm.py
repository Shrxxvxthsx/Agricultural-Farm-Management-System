from flask import Blueprint, jsonify, request
from models import db, Farm, Crop, SoilRecord, Equipment
from datetime import datetime

farm_bp = Blueprint('farm', __name__)

# Farm endpoints
@farm_bp.route('/', methods=['GET'])
def get_farms():
    try:
        # Get query parameters
        owner_id = request.args.get('owner_id')
        
        # Start with base query
        query = Farm.query
        
        # Apply owner filter
        if owner_id:
            query = query.filter(Farm.owner_id == owner_id)
        
        # Execute query
        farms = query.all()
        
        # Convert to dict
        result = [farm.to_dict() for farm in farms]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farm_bp.route('/<farm_id>', methods=['GET'])
def get_farm(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        
        if not farm:
            return jsonify({"error": "Farm not found"}), 404
        
        return jsonify(farm.to_dict())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farm_bp.route('/', methods=['POST'])
def create_farm():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'location', 'size', 'owner_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new farm
        farm = Farm(
            name=data['name'],
            location=data['location'],
            size=data['size'],
            owner_id=data['owner_id']
        )
        
        # Save to database
        db.session.add(farm)
        db.session.commit()
        
        return jsonify(farm.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Crop endpoints
@farm_bp.route('/<farm_id>/crops', methods=['GET'])
def get_crops(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        
        if not farm:
            return jsonify({"error": "Farm not found"}), 404
        
        crops = Crop.query.filter_by(farm_id=farm_id).all()
        result = [crop.to_dict() for crop in crops]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farm_bp.route('/<farm_id>/crops', methods=['POST'])
def create_crop(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        
        if not farm:
            return jsonify({"error": "Farm not found"}), 404
        
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'area']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Parse dates if provided
        planted_date = None
        if 'planted_date' in data and data['planted_date']:
            try:
                planted_date = datetime.strptime(data['planted_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid planted_date format. Use YYYY-MM-DD"}), 400
        
        harvest_date = None
        if 'harvest_date' in data and data['harvest_date']:
            try:
                harvest_date = datetime.strptime(data['harvest_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid harvest_date format. Use YYYY-MM-DD"}), 400
        
        # Create new crop
        crop = Crop(
            farm_id=farm_id,
            name=data['name'],
            area=data['area'],
            status=data.get('status', 'Planning'),
            planted_date=planted_date,
            harvest_date=harvest_date
        )
        
        # Save to database
        db.session.add(crop)
        db.session.commit()
        
        return jsonify(crop.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Soil record endpoints
@farm_bp.route('/<farm_id>/soil', methods=['GET'])
def get_soil_records(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        
        if not farm:
            return jsonify({"error": "Farm not found"}), 404
        
        # Get the latest soil record
        soil_record = SoilRecord.query.filter_by(farm_id=farm_id).order_by(SoilRecord.record_date.desc()).first()
        
        if not soil_record:
            return jsonify({"error": "No soil records found"}), 404
        
        return jsonify(soil_record.to_dict())
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farm_bp.route('/<farm_id>/soil', methods=['POST'])
def create_soil_record(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        
        if not farm:
            return jsonify({"error": "Farm not found"}), 404
        
        data = request.json
        
        # Validate required fields
        required_fields = ['ph', 'nitrogen', 'phosphorus', 'potassium', 'organic_matter']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Parse record date if provided
        record_date = datetime.utcnow().date()
        if 'record_date' in data and data['record_date']:
            try:
                record_date = datetime.strptime(data['record_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid record_date format. Use YYYY-MM-DD"}), 400
        
        # Create new soil record
        soil_record = SoilRecord(
            farm_id=farm_id,
            ph=data['ph'],
            nitrogen=data['nitrogen'],
            phosphorus=data['phosphorus'],
            potassium=data['potassium'],
            organic_matter=data['organic_matter'],
            record_date=record_date
        )
        
        # Save to database
        db.session.add(soil_record)
        db.session.commit()
        
        return jsonify(soil_record.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Equipment endpoints
@farm_bp.route('/<farm_id>/equipment', methods=['GET'])
def get_equipment(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        
        if not farm:
            return jsonify({"error": "Farm not found"}), 404
        
        equipment_list = Equipment.query.filter_by(farm_id=farm_id).all()
        result = [equipment.to_dict() for equipment in equipment_list]
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@farm_bp.route('/<farm_id>/equipment', methods=['POST'])
def create_equipment(farm_id):
    try:
        farm = Farm.query.get(farm_id)
        
        if not farm:
            return jsonify({"error": "Farm not found"}), 404
        
        data = request.json
        
        # Validate required fields
        if 'name' not in data:
            return jsonify({"error": "Missing required field: name"}), 400
        
        # Parse dates if provided
        last_maintenance = None
        if 'last_maintenance' in data and data['last_maintenance']:
            try:
                last_maintenance = datetime.strptime(data['last_maintenance'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid last_maintenance format. Use YYYY-MM-DD"}), 400
        
        next_maintenance = None
        if 'next_maintenance' in data and data['next_maintenance']:
            try:
                next_maintenance = datetime.strptime(data['next_maintenance'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "Invalid next_maintenance format. Use YYYY-MM-DD"}), 400
        
        # Create new equipment
        equipment = Equipment(
            farm_id=farm_id,
            name=data['name'],
            status=data.get('status', 'Operational'),
            last_maintenance=last_maintenance,
            next_maintenance=next_maintenance
        )
        
        # Save to database
        db.session.add(equipment)
        db.session.commit()
        
        return jsonify(equipment.to_dict()), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
