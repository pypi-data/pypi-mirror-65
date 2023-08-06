from typing import List
from ..device import CompoundEye
from ..pin import ANAPin

MAX_VOLT = 3.0


class QX_Eye(CompoundEye):

    def __init__(self):
        super().__init__()
        self.probe_angle = 360
        self.num_of_channels = 14
        self.min_val = 0
        self.max_val = 255
        self.val_pin: ANAPin = None
        self.dir_pin: ANAPin = None

    def on_attached(self):
        self.val_pin = self.pins[0]
        self.dir_pin = self.pins[1]
        assert self.val_pin and self.dir_pin, 'Invalid Pins'

    def get_val(self) -> int:
        val = self.val_pin.input()
        return min(val / MAX_VOLT * self.max_val, self.max_val)

    def get_dir(self) -> int:
        val = self.dir_pin.input()
        return min(val / MAX_VOLT * 360, 360)

    def detect(self) -> bool:
        self.value = self.max_ir = self.get_val()
        self.max_ir_dir = self.get_dir()
        return True
