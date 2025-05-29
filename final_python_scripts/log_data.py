import serial
import time
import csv

PORT = 'COM4'
BAUDRATE = 115200
LABEL = input("which gesture are we recording? (ex.: left)? ")

ser = serial.Serial(PORT, BAUDRATE)
time.sleep(2)

filename = f"{LABEL}_{int(time.time())}.csv"
with open(filename, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'label'])

    print("recording started... Ctrl+C to stop")

    try:
        count = 0
        while count < 200:
            raw = ser.readline()
            print("RAW BYTES:", raw)
            try:
                line = raw.decode(errors='ignore').strip()
            except:
                continue

            print("DECODED:", line)

            if not line or line.startswith("ax"):
                continue

            parts = line.split(',')
            if len(parts) == 6:
                parts.append(LABEL)
                writer.writerow(parts)
                print("OK:", parts)
                count += 1
            else:
                print("SKIPPED:", parts)

    except KeyboardInterrupt:
        print("recording complete")