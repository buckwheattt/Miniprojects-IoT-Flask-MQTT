from machine import I2C, Pin, PWM
import time
from mpu9250 import MPU9250

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
imu = MPU9250(i2c)

r = PWM(Pin(15))
g = PWM(Pin(14))
b = PWM(Pin(13))

r.freq(1000)
g.freq(1000)
b.freq(1000)

def set_color(red, green, blue):
    r.duty_u16(red * 257)
    g.duty_u16(green * 257)
    b.duty_u16(blue * 257)

def off():
    set_color(0, 0, 0)

ACC_THRESHOLD = 1.2

while True:
    ax, ay, az = imu.acceleration

    if ay > ACC_THRESHOLD:
        print("UP - RED")
        set_color(255, 0, 0)
    elif ax > ACC_THRESHOLD:
        print("RIGHT - GREEN")
        set_color(0, 255, 0)
    elif ax < -ACC_THRESHOLD:
        print("LEFT - YELLOW")
        set_color(255, 255, 0)
    elif ay < -ACC_THRESHOLD:
        print("DOWN - OFF")
        off()
    else:
        pass

    time.sleep(0.2)