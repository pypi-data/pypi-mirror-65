from typing import List
from ..pin import PWMPin
from ..device import Bulb


class KS_RGB(Bulb):

    def __init__(self):
        super().__init__()
        self.red: PWMPin = None
        self.green: PWMPin = None
        self.blue: PWMPin = None

    def on_attached(self):
        for pin in self.pins:
            setattr(self, pin.tag, pin)
            pin.change_frequency(70)
            pin.start()

    def change_color(self, color: List[int]):
        if self.red:
            self.red.change_duty_cycle((int)(color[0]/255*100))
        if self.green:
            self.green.change_duty_cycle((int)(color[1]/255*100))
        if self.blue:
            self.blue.change_duty_cycle((int)(color[2]/255*100))
