import dht
from machine import Pin

from educore import pin


class dht11:
    def __init__(self, ch=None, port=None):
        if ch is None and port is None:
            print('暂不支持板载功能')
            return
        if port is not None:
            print('暂不支持端口')
            return
        else:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()

        self.s_pin.init(mode=Pin.IN, pull=Pin.PULL_UP)
        self.dht_sensor = dht.DHT22(self.s_pin)

    def read(self):
        self.dht_sensor.measure()
        temperature = self.dht_sensor.temperature()
        humidity = self.dht_sensor.humidity()
        data = (temperature, humidity)
        return data
