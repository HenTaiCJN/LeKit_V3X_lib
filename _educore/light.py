from machine import Pin, ADC

from educore import pin


class light:
    def __init__(self, ch=None, port=None):
        if port is not None:
            print('暂不支持端口')
            return
        elif ch is not None:
            if ch is None:
                s_pin = Pin(34)
            elif isinstance(ch, pin):
                s_pin = ch.get_pin()
            else:
                s_pin = pin(ch).get_pin()
        else:
            s_pin = Pin(34, mode=Pin.IN)

        s_pin.init(mode=Pin.IN)
        try:
            self.s_adc = ADC(s_pin)
        except:
            print('开启wifi的情况下，非板载光敏传感器请使用0号口或1号口')
            return
        self.s_adc.width(ADC.WIDTH_12BIT)
        self.s_adc.atten(ADC.ATTN_11DB)

    def read(self):
        return self.s_adc.read()
