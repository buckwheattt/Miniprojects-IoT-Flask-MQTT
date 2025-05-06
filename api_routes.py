from flask import Blueprint, request, jsonify
from models import db, Data
from flask_login import login_required
from datetime import datetime


api_bp = Blueprint('api', __name__)

# Insert new value
@api_bp.route('/insert', methods=['POST'])
def insert_value():
    data = request.get_json()
    temp = data.get('temperature')
    timestamp_measurement = data.get('timestamp_measurement')
    timestamp_send = data.get('timestamp_send')

    if temp is None or timestamp_measurement is None or timestamp_send is None:
        return jsonify({"error": "Missing data"}), 400

    new_entry = Data(
        temperature=temp,
        timestamp_measurement=datetime.fromtimestamp(timestamp_measurement),
        timestamp_send=datetime.fromtimestamp(timestamp_send),
        timestamp_received=datetime.utcnow()
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"success": True, "id": new_entry.id}), 201

# Get latest value
@api_bp.route('/latest', methods=['GET'])
def get_latest():
    latest = Data.query.order_by(Data.timestamp_measurement.desc()).first()
    if not latest:
        return jsonify({"error": "No data"}), 404
    return jsonify({
        "id": latest.id,
        "temperature": latest.temperature,
        "timestamp_measurement": latest.timestamp_measurement.isoformat(),
        "timestamp_send": latest.timestamp_send.isoformat(),
        "timestamp_received": latest.timestamp_received.isoformat()
    })

# Get value by ID
@api_bp.route('/value/<int:id>', methods=['GET'])
def get_by_id(id):
    entry = Data.query.get(id)
    if not entry:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": entry.id,
        "temperature": entry.temperature,
        "timestamp_measurement": entry.timestamp_measurement.isoformat(),
        "timestamp_send": entry.timestamp_send.isoformat(),
        "timestamp_received": entry.timestamp_received.isoformat()
    })

# Delete oldest value
@api_bp.route('/delete_oldest', methods=['DELETE'])
@login_required
def delete_oldest():
    oldest = Data.query.order_by(Data.timestamp_measurement.asc()).first()
    if not oldest:
        return jsonify({"error": "No data"}), 404
    db.session.delete(oldest)
    db.session.commit()
    return jsonify({"success": True})

# Delete value by ID
@api_bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_by_id(id):
    entry = Data.query.get(id)
    if not entry:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"success": True})

# BONUS: Get all values, sorted
@api_bp.route('/all', methods=['GET'])
def get_all():
    sort = request.args.get('sort', 'asc')
    order = Data.timestamp_measurement.asc() if sort == 'asc' else Data.timestamp_measurement.desc()
    all_data = Data.query.order_by(order).all()
    return jsonify([
        {
            "id": d.id,
            "temperature": d.temperature,
            "timestamp_measurement": d.timestamp_measurement.isoformat(),
            "timestamp_send": d.timestamp_send.isoformat(),
            "timestamp_received": d.timestamp_received.isoformat()
        } for d in all_data
    ])
