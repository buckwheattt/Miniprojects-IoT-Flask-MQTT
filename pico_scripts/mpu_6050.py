from struct import unpack

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x6B, b'\x00')  # Wake up

    def read_accel_raw(self):
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 6)
        return unpack('>hhh', data)

    def read_gyro_raw(self):
        data = self.i2c.readfrom_mem(self.addr, 0x43, 6)
        return unpack('>hhh', data)

    def accel(self):
        x, y, z = self.read_accel_raw()
        return (x / 16384, y / 16384, z / 16384)

    def gyro(self):
        x, y, z = self.read_gyro_raw()
        return (x / 131, y / 131, z / 131)
