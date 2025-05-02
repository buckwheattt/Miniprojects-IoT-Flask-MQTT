# -*- coding: utf-8 -*-

import json
import traceback
from datetime import datetime
import paho.mqtt.client as mqtt
from app import app, db
from models import Data # импортируем из твоего Flask-приложения

# MQTT настройки
MQTT_BROKER = 'broker.hivemq.com'
MQTT_TOPIC = 'pico/temperature'

def on_connect(client, userdata, flags, rc):
    print('MQTT connected with code', rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f'message recieved: {msg.payload.decode()}')

    try:
        data = json.loads(msg.payload.decode())
        temperature = data['temperature']
        timestamp_measurement = datetime.fromtimestamp(data['timestamp_measurement'])
        timestamp_send = datetime.fromtimestamp(data['timestamp_send'])
        timestamp_received = datetime.now()

        new_record = Data(
            temperature=temperature,
            timestamp_measurement=timestamp_measurement,
            timestamp_send=timestamp_send,
            timestamp_received=timestamp_received
        )

        with app.app_context():
            db.session.add(new_record)
            db.session.commit()
        
        print('data has been written to db')
    except Exception as e:
        print("Exception while handling message:")
        traceback.print_exc()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, 1883, 60)
client.loop_forever()
