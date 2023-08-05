from typing import Union
from ..device import Servo
from ..pin import DIGPin, PWMPin


class Servo2Wire(Servo):

    def __init__(self):
        super().__init__()
        self.prev_speed = self.speed
        self.prev_direction = self.direction
        self.pos: Union[PWMPin, DIGPin] = None
        self.neg: Union[PWMPin, DIGPin] = None

    def on_attached(self):
        for pin in self.pins:
            setattr(self, pin.tag, pin)
        assert self.pos and self.neg, 'Invalid Pins'
        self.pos.change_frequency(60)

    def on_detatched(self):
        self.stop()

    def move(self):
        self.speed <= 1.0, 'Invalid Speed'
        if self.speed != self.prev_speed:
            self.prev_speed = self.speed
            self.pos.change_duty_cycle(self.speed * 100)
        if self.direction != self.prev_direction:
            self.prev_direction = self.direction
            if self.direction == 1:
                self.pos.output(1)
                self.neg.output(0)
            elif self.direction == -1:
                self.pos.output(0)
                self.neg.output(1)

    def stop(self):
        self.pos.stop()
