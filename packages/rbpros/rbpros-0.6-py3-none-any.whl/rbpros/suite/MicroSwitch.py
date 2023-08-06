from ..pin import DIGPin
from ..device import Switch


class MicroSwitch(Switch):

    def __init__(self):
        super().__init__()
        self.pin: DIGPin = None

    def on_attached(self):
        self.pin = self.pins[0]
        assert self.pin, 'Invalid Pin'

    def read_state(self):
        return self.pin.input()
