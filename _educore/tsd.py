from machine import Pin

from educore import pin

class TSD:
    def __init__(self, ch=None, port=None):
        if ch is None and port is None:
            print('暂不支持板载功能')
            return
        if port is not None:
            print('不支持端口')
            return
        else:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()
        self.s_pin.init(mode=Pin.IN)


    def read(self):
        return self.s_pin.value()