from flask import Blueprint, request, jsonify
from models import db, Data
from flask_login import login_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/insert', methods=['POST'])
def insert_value():
    data = request.get_json()
    temp = data.get('temperature')
    if temp is None:
        return jsonify({"error": "Missing temperature"}), 400
    new_entry = Data(temperature=temp)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"success": True, "id": new_entry.id}), 201

@api_bp.route('/latest', methods=['GET'])
def get_latest():
    latest = Data.query.order_by(Data.timestamp.desc()).first()
    if not latest:
        return jsonify({"error": "No data"}), 404
    return jsonify({
        "id": latest.id,
        "temperature": latest.temperature,
        "timestamp": latest.timestamp.isoformat()
    })

@api_bp.route('/value/<int:id>', methods=['GET'])
def get_by_id(id):
    entry = Data.query.get(id)
    if not entry:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": entry.id,
        "temperature": entry.temperature,
        "timestamp": entry.timestamp.isoformat()
    })

@api_bp.route('/delete_oldest', methods=['DELETE'])
@login_required
def delete_oldest():
    oldest = Data.query.order_by(Data.timestamp.asc()).first()
    if not oldest:
        return jsonify({"error": "No data"}), 404
    db.session.delete(oldest)
    db.session.commit()
    return jsonify({"success": True})

@api_bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_by_id(id):
    entry = Data.query.get(id)
    if not entry:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"success": True})

# BONUS endpoint
@api_bp.route('/all', methods=['GET'])
def get_all():
    sort = request.args.get('sort', 'asc')
    order = Data.timestamp.asc() if sort == 'asc' else Data.timestamp.desc()
    all_data = Data.query.order_by(order).all()
    return jsonify([{
        "id": d.id,
        "temperature": d.temperature,
        "timestamp": d.timestamp.isoformat()
    } for d in all_data])
