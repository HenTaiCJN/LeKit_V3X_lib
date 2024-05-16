from machine import Pin, SoftI2C,I2C

from educore import pin
from qmc5883l_micropython import qmc5883l


class qmc5883:
    def __init__(self, sda=None, scl=None, port=None):
        if sda is None and scl is None and port is None:
            self.scl = Pin(22)
            self.sda = Pin(21)
        elif port is not None:
            print('不支持端口')
            return
        else:
            if isinstance(sda, pin):
                self.sda = sda.get_pin()
            else:
                self.sda = pin(sda).get_pin()

            if isinstance(scl, pin):
                self.scl = scl.get_pin()
            else:
                self.scl = pin(scl).get_pin()

        if sda is None and scl is None:
            self.i2c = I2C(0, sda=self.sda, scl=self.scl)
        else:
            self.i2c = SoftI2C(sda=self.sda, scl=self.scl)

        self.qmc = qmc5883l.QMC5883L(self.i2c)

    def adjust(self):
        print('adjusting...')
        self.qmc.calibrate(5)
        print('adjust success')

    def direction(self):
        x, y, z, t = self.qmc.read_scaled()

        return self.qmc.get_angle(x, y) % 360

    def getx(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_x

    def gety(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_y

    def getz(self):
        mag_x, mag_y, mag_z = self.qmc.read_raw()
        return mag_z
