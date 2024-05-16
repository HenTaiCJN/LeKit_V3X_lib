import time

from machine import Pin, I2C, SoftI2C

from adxl import adxl345
from educore import pin


class accelerometer:
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
            i2c = I2C(0, sda=self.sda, scl=self.scl, freq=10000)
        else:
            i2c = SoftI2C(sda=self.sda, scl=self.scl, freq=10000)

        self.snsr = adxl345(i2c)

    @property
    def X(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return x

    @property
    def Y(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return y

    @property
    def Z(self):
        if self.snsr is not None:
            x, y, z = self.snsr.readXYZ()
            time.sleep(0.5)
            return z

    def shake(self):
        if self.snsr is not None:
            x1, y1, z1 = self.snsr.readXYZ()
            time.sleep(0.5)
            x2, y2, z2 = self.snsr.readXYZ()
            time.sleep(0.5)
            if abs(x1 - x2) > 20 or abs(y1 - y2) > 20 or abs(z1 - z2) > 20:
                return True
            else:
                return False
