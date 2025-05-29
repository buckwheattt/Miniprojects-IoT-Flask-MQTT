from mpu6050 import MPU6050

class MPU9250:
    def __init__(self, i2c, addr=0x68):
        self.mpu = MPU6050(i2c, addr)

    @property
    def acceleration(self):
        return self.mpu.accel()

    @property
    def gyro(self):
        return self.mpu.gyro()
