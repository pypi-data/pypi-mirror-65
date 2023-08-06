from ..device import Board
from ..pin import DIGPin, I2C, IOType, PWMPin, SCLPin, SDAPin
import math
import time

SUBADR1 = 0x02
SUBADR2 = 0x03
SUBADR3 = 0x04
MODE1 = 0x00
PRESCALE = 0xFE
LED0_ON_L = 0x06
LED0_ON_H = 0x07
LED0_OFF_L = 0x08
LED0_OFF_H = 0x09
ALLLED_ON_L = 0xFA
ALLLED_ON_H = 0xFB
ALLLED_OFF_L = 0xFC
ALLLED_OFF_H = 0xFD


class HATPin(PWMPin, DIGPin):

    def __init__(self, num: int, tag=''):
        super().__init__(num, tag)
        self.pwm: int = 0
        self.hat: HAT = None

    def on_setup(self, host: Board):
        if self.num == 1 or self.num == 2:
            self.pwm = 0
        if self.num == 3 or self.num == 4:
            self.pwm = 5
        self.hat = host

    def input(self) -> int:
        pass

    def output(self, val: int):
        self.hat.set_level(self.num, val)

    def start(self, dc=0):
        self.change_duty_cycle(dc)

    def stop(self):
        self.change_duty_cycle(0)

    def change_frequency(self, freq):
        self.hat.set_frequency(freq)

    def change_duty_cycle(self, dc):
        self.hat.set_duty_cycle(self.pwm, dc)


HAT_SLOTS = [HATPin(1), HATPin(2), HATPin(3), HATPin(4)]


class HAT(Board):
    # PCA9685

    RBP_PINS = (SDAPin(2), SCLPin(3))

    def __init__(self):
        super().__init__()
        self.i2c = I2C(0x40)
        self.slots = HAT_SLOTS.copy()

    def on_attached(self):
        assert any(p.type == IOType.SCL for p in self.pins) and any(
            p.type == IOType.SDA for p in self.pins), 'Invalid Pins'
        self.i2c.write_byte(MODE1, 0x00)

    def set_frequency(self, freq: int):
        prescale = 25000000.0    # 25MHz
        prescale /= 4096.0       # 12-bit
        prescale /= float(freq)
        prescale -= 1.0
        prescale = math.floor(prescale + 0.5)
        oldmode = self.i2c.read_byte(MODE1)
        newmode = (oldmode & 0x7F) | 0x10        # sleep
        self.i2c.write_byte(MODE1, newmode)        # go to sleep
        self.i2c.write_byte(PRESCALE, prescale)
        self.i2c.write_byte(MODE1, oldmode)
        time.sleep(0.005)
        self.i2c.write_byte(MODE1, oldmode | 0x80)

    def set_pwm(self, channel: int, on: int, off: int):
        self.i2c.write_byte(LED0_ON_L + 4*channel, on & 0xFF)
        self.i2c.write_byte(LED0_ON_H + 4*channel, on >> 8)
        self.i2c.write_byte(LED0_OFF_L + 4*channel, off & 0xFF)
        self.i2c.write_byte(LED0_OFF_H + 4*channel, off >> 8)
        time.sleep(0.05)

    def set_duty_cycle(self, channel: int, pulse: int):
        self.set_pwm(channel, 0, int(pulse * (4095 / 100)))

    def set_level(self, channel: int, value: int):
        if (value == 1):
            self.set_pwm(channel, 0, 4095)
        else:
            self.set_pwm(channel, 0, 0)
