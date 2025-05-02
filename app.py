# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Data
from api_routes import api_bp
from datetime import datetime
import paho.mqtt.publish as publish
MQTT_BROKER = "broker.hivemq.com"  # или свой адрес брокера


app = Flask(__name__)
app.secret_key = "supersecretkey"

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# API blueprint
app.register_blueprint(api_bp, url_prefix="/api")

# Создание таблиц при первом запуске
with app.app_context():
    db.create_all()

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============ ROUTES ============

@app.route("/")
@login_required
def dashboard():
    num_values = request.args.get("num", session.get("num", 15), type=int)
    sort = request.args.get("sort", session.get("sort", "desc"))

    num_values = max(1, min(num_values, Data.query.count()))
    session["num"] = num_values
    session["sort"] = sort

    order = Data.timestamp_measurement.desc() if sort == "desc" else Data.timestamp_measurement.asc()
    data = Data.query.order_by(order).limit(num_values).all()
    last_value = data[-1] if sort == "asc" else data[0] if data else None

    return render_template("dashboard.html",
                           data=data,
                           last_value=last_value,
                           total_records=Data.query.count(),
                           num_values=num_values,
                           sort=sort)

@app.route("/delete_oldest", methods=["POST"])
@login_required
def delete_oldest():
    oldest = Data.query.order_by(Data.timestamp_measurement.asc()).first()
    if oldest:
        db.session.delete(oldest)
        db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if User.query.filter_by(username=username).first():
            return "Username already exists", 400

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/led/on', methods=['POST'])
def led_on():
    print("publish is:", publish)
    publish.single("pico/control/led", "ON", hostname=MQTT_BROKER)
    return redirect(url_for('dashboard'))

@app.route('/led/off', methods=['POST'])
def led_off():
    publish.single("pico/control/led", "OFF", hostname=MQTT_BROKER)
    return redirect(url_for('dashboard'))

@app.route('/measure/start', methods=['POST'])
def measure_start():
    publish.single("pico/control/measure", "START", hostname=MQTT_BROKER)
    return redirect(url_for('dashboard'))

@app.route('/measure/stop', methods=['POST'])
def measure_stop():
    publish.single("pico/control/measure", "STOP", hostname=MQTT_BROKER)
    return redirect(url_for('dashboard'))

@app.route('/set_interval', methods=['POST'])
def set_interval():
    interval = request.form.get('interval')
    if interval and interval.isdigit() and int(interval) > 0:
        publish.single("pico/control/interval", interval, hostname=MQTT_BROKER)
    return redirect(url_for('dashboard'))

# ============ START ============
if __name__ == "__main__":
    app.run(debug=True)
