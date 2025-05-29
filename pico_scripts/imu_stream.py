from machine import I2C, Pin
import utime
from pico_scripts.mpu9250 import MPU9250

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
imu = MPU9250(i2c)

print("ax,ay,az,gx,gy,gz")

while True:
    ax, ay, az = imu.acceleration
    gx, gy, gz = imu.gyro

    print(f"{ax:.3f},{ay:.3f},{az:.3f},{gx:.3f},{gy:.3f},{gz:.3f}")
    utime.sleep(0.05)
