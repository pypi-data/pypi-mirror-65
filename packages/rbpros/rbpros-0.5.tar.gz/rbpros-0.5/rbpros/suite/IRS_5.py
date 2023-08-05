from typing import List
from ..device import Infrared


class IRS_5(Infrared):

    def __init__(self):
        super().__init__()
        self.probe_angle = 120
        self.max_ir = 0.0
        self.max_ir_dir = 0
        self.ir_vals: List[Tuple[int, int]] = []

    def on_attached(self):
        assert sum(p is not None for p in self.pins) > 0, 'Invalid Pins'

    def detect(self) -> bool:
        self.ir_vals.clear()
        self.value = 0
        for pin in self.pins:
            if not pin:
                continue
            num = pin.num
            val = pin.input()
            if val > self.value:
                self.value = self.max_ir = val
                self.max_ir_dir = num
            self.ir_vals.append((num, val))
        return True
