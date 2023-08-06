from ..device import Servo
from ..pin import PWMPin


class SG90(Servo):

    def __init__(self):
        super().__init__()
        self.pwm: PWMPin = None
        self.angle = 0

    def on_attached(self):
        self.pwm = self.pins[0]
        assert self.pwm, 'Invalid Pins'
        self.pwm.change_frequency(50)
        self.pwm.start()

    def move(self):
        assert self.angle >= 0 and self.angle <= 180, 'Invalid Angle'
        self.pwm.change_duty_cycle(2.5 + 10 * self.angle / 180)

    def stop(self):
        self.pos.stop()
