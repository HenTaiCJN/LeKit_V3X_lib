from machine import Pin, PWM

from educore import pin


def linear_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


class parrot:
    M1 = 1
    M2 = 2

    def __init__(self, ch=None, in0=None, in1=None):
        self.ch = ch
        self.in0 = in0
        self.in1 = in1
        self.is_onboard = False

        self.motor_pin1 = None
        self.motor_pin2 = None
        self.motor_pwm = None
        self.speed = None

        if self.in0 is None or self.in1 is None:
            self.init_onboard_motor()
        else:
            self.init_external_motor()

    def init_onboard_motor(self):
        if self.ch == 1:
            self.motor_pin1 = Pin(5, mode=Pin.OUT, pull=Pin.PULL_UP)
            self.motor_pin2 = Pin(18, mode=Pin.OUT, pull=Pin.PULL_UP)
        else:
            self.motor_pin1 = Pin(25, mode=Pin.OUT, pull=Pin.PULL_UP)
            self.motor_pin2 = Pin(27, mode=Pin.OUT, pull=Pin.PULL_UP)

        self.motor_pwm = PWM(self.motor_pin2)

    def init_external_motor(self):
        if isinstance(self.in0, int):
            self.motor_pin1 = pin(self.in0).get_pin()
        else:
            self.motor_pin1 = self.in0.get_pin()

        if isinstance(self.in1, int):
            self.motor_pin2 = pin(self.in1).get_pin()
        else:
            self.motor_pin2 = self.in1.get_pin()

        self.motor_pin1.init(mode=Pin.OUT, pull=Pin.PULL_UP)
        self.motor_pin2.init(mode=Pin.OUT, pull=Pin.PULL_UP)
        self.motor_pwm = PWM(self.motor_pin2)

    def set_speed(self, speed=None):

        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100

        self.speed = speed
        self.updata_onboard()

    def updata_onboard(self):
        self.motor_pwm.deinit()
        self.motor_pwm = PWM(self.motor_pin2, freq=50000)
        if self.speed > 0:
            self.motor_pin1.value(1)
            mapped_value = linear_map(self.speed, 1, 100, 70, 100)
            self.motor_pwm.duty(int((100 - mapped_value) * 10.23))
        elif self.speed < 0:
            self.motor_pin1.value(0)
            mapped_value = linear_map(self.speed, -1, -100, -75, -100)
            self.motor_pwm.duty(int(-mapped_value * 10.23))
        else:
            self.motor_pin1.value(0)
            self.motor_pwm.duty(0)
