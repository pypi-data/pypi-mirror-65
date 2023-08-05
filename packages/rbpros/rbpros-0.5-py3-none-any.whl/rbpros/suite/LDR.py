from ..pin import ANAPin
from ..device import GrayScale


class LDR(GrayScale):

    def __init__(self):
        super().__init__()
        self.ctr = 0.6
        self.pin: ANAPin = None

    def on_attached(self):
        self.pin = self.pins[0]
        assert self.pin, 'Invalid Pin'

    def detect(self) -> bool:
        v = self.pin.input()
        self.value = self.normalize(v)
        return True

    def normalize(self, val: float) -> float:
        min_val = self.max_val * self.ctr
        return max(0, (val - min_val) / 100.0 * self.max_val)
