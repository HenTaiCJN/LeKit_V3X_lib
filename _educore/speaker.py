import math
import time
from _educore._timer import _timer
from machine import Pin, PWM, DAC

from educore import pin,oled

class speaker:
    def __init__(self, ch=None, port=None):
        self.data = None
        self.sample_size = None
        self.sample_rate = None
        self.is_onboard = False
        if port is not None:
            print('不支持端口')
            return
        elif ch is not None:
            if isinstance(ch, pin):
                self.s_pin = ch.get_pin()
            else:
                self.s_pin = pin(ch).get_pin()
        elif port is None and ch is None:
            self.is_onboard = True
            self.s_pin = Pin(26)

        self.s_pin.init(mode=Pin.OUT)

        if self.is_onboard:
            self.dac = DAC(self.s_pin)
            self.dac.write(0)
        else:
            self.pwm = PWM(self.s_pin)
            self.pwm.duty(0)

    def tone(self, freq, durl=None, duty=512):
        if self.is_onboard:
            self.tone_onborad(freq, durl, duty)
        else:
            self.tone_ex(freq, durl, duty)

    def tone_onborad(self, freq, durl=150, duty=512):
        self.sample_rate = 6000  # 采样率
        self.sample_size = int(self.sample_rate * (durl or 1000) / 1000)  # 根据持续时间计算采样点数
        self.data = bytearray(self.sample_size)  # 用于存储声音数据的字节数组
        for f in freq:
            for i in range(self.sample_size):
                t = i / self.sample_rate
                self.data[i] += int(127.5 * math.sin(2 * math.pi * f * t))

        if durl is None:
            _timer.add(self._tone, 1100)
        else:
            for i in range(self.sample_size):
                self.dac.write(self.data[i])  # 写入 DAC 输出
                time.sleep_us(int(1000000 / self.sample_rate))
            self.dac.write(0)

    def _tone(self):
        for i in range(self.sample_size):
            self.dac.write(self.data[i])  # 写入 DAC 输出
            time.sleep_us(int(1000000 / self.sample_rate))

    def tone_ex(self, freq, durl=150, duty=512):
        if type(freq) == list:
            freq = freq[0]
        self.pwm.duty(duty)
        if durl == 0 or durl is None:
            self.pwm.freq(freq)
        else:
            self.pwm.freq(freq)
            time.sleep(durl / 1000)
            self.pwm.duty(0)

    def stop(self):
        if self.is_onboard:
            _timer.delete(self._tone)
            self.dac.write(0)
        else:
            self.pwm.duty(0)