from machine import I2C, Pin
import time
from mpu9250 import MPU9250

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
imu = MPU9250(i2c)

while True:
    accel = imu.acceleration
    gyro = imu.gyro
    print("Accel:", accel)
    print("Gyro:", gyro)
    time.sleep(0.2)