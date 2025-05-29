from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
devices = i2c.scan()

if devices:
    print("Found device with I2C:")
    for d in devices:
        print(hex(d))
else:
    print("Nothing found!")