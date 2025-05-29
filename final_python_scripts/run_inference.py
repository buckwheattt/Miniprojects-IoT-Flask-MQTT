import serial
import time
import numpy as np
import joblib

model = joblib.load("model.pkl")

PORT = 'COM4'
BAUD = 115200
WINDOW_SIZE = 50

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

buffer = []

print("Listening to IMU data...")

while True:
    try:
        line = ser.readline().decode(errors='ignore').strip()
        if not line or line.startswith("ax"):
            continue

        parts = line.split(',')
        if len(parts) != 6:
            continue

        data = [float(x) for x in parts]
        buffer.append(data)

        if len(buffer) == WINDOW_SIZE:
            flat = np.array(buffer).flatten().reshape(1, -1)
            gesture = model.predict(flat)[0]
            print("GESTURE:", gesture)

            if gesture == 'left':
                ser.write(b'B\n')
            elif gesture == 'right':
                ser.write(b'G\n')
            elif gesture == 'up':
                ser.write(b'R\n')
            elif gesture == 'down' or gesture == 'idle':
                ser.write(b'0\n')

            buffer = []

    except KeyboardInterrupt:
        print("Exit")
        break
