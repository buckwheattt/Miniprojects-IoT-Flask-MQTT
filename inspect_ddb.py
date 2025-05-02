from models import db, Data
from app import app

with app.app_context():
    records = Data.query.order_by(Data.id.desc()).limit(10).all()
    print("last:")
    for r in records:
        print(r.id, r.temperature, r.timestamp_measurement)
