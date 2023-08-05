import time
from ..device import Ultrasonic
from ..pin import DIGPin


class HC_SR04(Ultrasonic):

    def __init__(self):
        super().__init__()
        self.probe_angle = 15
        self.min_val = 2.0
        self.max_val = 450.0
        self.accuracy = 0.2
        self.trig: DIGPin = None
        self.echo: DIGPin = None

    def on_attached(self):
        for pin in self.pins:
            setattr(self, pin.tag, pin)
        assert self.trig and self.echo, 'Invalid Pins'

    def detect(self, timeout: float = 0.01) -> bool:
        self.trig.output(1)
        time.sleep(0.00001)
        self.trig.output(0)
        init = start = stop = time.time()
        while self.echo.input() == 0:
            start = time.time()
            if start - init > timeout:
                return False
        while self.echo.input() == 1:
            stop = time.time()
            if stop - init > timeout:
                return False
        elapsed = stop - start
        self.value = elapsed * 343 * 100 / 2
        return True
