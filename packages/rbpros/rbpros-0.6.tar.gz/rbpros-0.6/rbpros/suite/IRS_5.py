from typing import List
from ..device import CompoundEye

MAX_VOLT = 5.0


class IRS_5(CompoundEye):

    def __init__(self):
        super().__init__()
        self.probe_angle = 120
        self.num_of_channels = 5
        self.min_val = 0
        self.max_val = 255
        self.ir_vals: List[Tuple[int, int]] = []

    def on_attached(self):
        assert sum(p is not None for p in self.pins) > 0, 'Invalid Pins'

    def get_val(self, val: float) -> int:
        return min(val/MAX_VOLT*self.max_val, self.max_val)

    def detect(self) -> bool:
        self.ir_vals.clear()
        self.value = 0
        for pin in self.pins:
            if not pin:
                continue
            num = pin.num
            val = self.get_val(pin.input())
            if val > self.value:
                self.value = self.max_ir = val
                self.max_ir_dir = num
            self.ir_vals.append((num, val))
        return True
