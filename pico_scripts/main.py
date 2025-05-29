from machine import I2C, Pin, PWM
from mpu9250 import MPU9250
import utime
import sys
import select

# I2C + IMU
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
imu = MPU9250(i2c)

# RGB
r = PWM(Pin(15))
g = PWM(Pin(14))
b = PWM(Pin(13))
for led in (r, g, b):
    led.freq(1000)

def set_color(red, green, blue):
    r.duty_u16(red * 257)
    g.duty_u16(green * 257)
    b.duty_u16(blue * 257)

def off():
    set_color(0, 0, 0)

# UART poll init
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

print("ax,ay,az,gx,gy,gz")
last_check = utime.ticks_ms()

while True:
    now = utime.ticks_ms()
    if utime.ticks_diff(now, last_check) > 50:
        ax, ay, az = imu.acceleration
        gx, gy, gz = imu.gyro
        print(f"{ax:.3f},{ay:.3f},{az:.3f},{gx:.3f},{gy:.3f},{gz:.3f}")
        last_check = now

    if poller.poll(0):
        cmd = sys.stdin.readline().strip()
        if cmd == 'R':
            set_color(255, 0, 0)
        elif cmd == 'G':
            set_color(0, 255, 0)
        elif cmd == 'B':
            set_color(255, 255, 0)
        elif cmd == '0':
            off()

