from abc import ABC, abstractmethod, abstractproperty
from typing import Callable, Dict, List, Type, TypeVar
from . import behavior
from .engine import Engine
from .pin import IOType, Pin
from .util import generate_id

TA = TypeVar('TA', bound='Attachable')
TB = TypeVar('TB', bound='Behavior')


class Device(ABC):

    def __init__(self):
        super().__init__()
        self.id = ''
        self.name = ''
        self.behaviors: List[behavior.Behavior] = []

    def __str__(self):
        return 'Id:%s Name:%s' % (self.id, self.name)

    @abstractproperty
    def engine(self) -> Engine:
        pass

    def destory(self):
        self.id = ''
        self.name = ''
        for beh in self.behaviors[:]:
            self.engine.destory_behavior(beh)
        self.behaviors = []

    def attach_behavior(self, klass: Type[TB]) -> TB:
        beh = self.engine.spawn_behavior(klass)
        if isinstance(beh, behavior.DeviceBehavior):
            beh.device = self
        self.behaviors.append(beh)
        return beh

    def detatch_behavior(self, beh: behavior.Behavior):
        self.behaviors.remove(beh)
        self.engine.destory_behavior(beh)

    def get_behavior(self, klass: Type[TB]) -> TB:
        for beh in self.behaviors:
            if isinstance(beh, klass):
                return beh

    def get_behaviors(self, klass: Type[TB]) -> List[TB]:
        behs = []
        for beh in self.behaviors:
            if isinstance(beh, klass):
                behs.append(beh)
        return behs


class Attachable(Device):

    def __init__(self):
        super().__init__()
        self.host: Board = None
        self.pins: List[Pin] = []

    @property
    def engine(self) -> Engine:
        return self.host.engine

    def on_attached(self):
        pass

    def on_detatched(self):
        pass

    def get_behavior_include_host(self, klass: Type[TB]) -> TB:
        beh = self.get_behavior(klass)
        if not beh:
            if isinstance(self.host, Attachable):
                beh = self.host.get_behavior_include_host(klass)
            elif self.host:
                beh = self.host.get_behavior(klass)
        return beh

    def get_behaviors_include_host(self, klass: Type[TB]) -> TB:
        behs = []
        behs.extend(self.get_behaviors(klass))
        if isinstance(self.host, Attachable):
            behs.extend(self.host.get_behaviors_include_host(klass))
        elif self.host:
            behs.extend(self.host.get_behaviors(klass))
        return beh


class Board(Attachable):

    def __init__(self):
        super().__init__()
        self.slots: List[Pin] = []
        self.devices: List[Device] = []

    def __str__(self):
        return 'Name:%s Slots:%s Devices:%s' % (self.name, self.slots, len(self.devices))

    def is_slot_available(self, *pins: Pin) -> bool:
        for pin in pins:
            if pin and pin not in self.slots:
                return False
        return True

    def is_serial_pin(self, pin: Pin) -> bool:
        return pin.type == IOType.SCL or pin.type == IOType.SDA

    def attatch_device(self, klass: Type[TA], name: str = None, *pins: Pin, inherit_slots: bool = False) -> TA:
        assert self.is_slot_available(*pins), 'Slot not available'
        assert not inherit_slots or inherit_slots and issubclass(
            klass, Board), 'Only Board can inherit host slots'
        dev = klass()
        dev.id = generate_id(klass)
        dev.name = name or klass.__name__
        dev.host = self
        dev.pins = pins
        for pin in pins:
            if not pin:
                continue
            if not self.is_serial_pin(pin):
                self.slots.remove(pin)
            pin.on_setup(self)
        if inherit_slots:
            dev.slots.extend(self.slots)
        self.devices.append(dev)
        dev.on_attached()
        return dev

    def detatch_device(self, dev: Device):
        self.devices.remove(dev)
        self.slots.extend(dev.pins)
        dev.on_detatched()
        dev.destory()

    def get_behavior_include_attachments(self, klass: Type[TB]) -> TB:
        beh = self.get_behavior(klass)
        if not beh:
            for dev in self.devices:
                if isinstance(dev, Board):
                    beh = dev.get_behavior_include_attachments(klass)
                else:
                    beh = dev.get_behavior(klass)
                if beh:
                    break
        return beh

    def get_behaviors_include_attachments(self, klass: Type[TB]) -> TB:
        behs = []
        behs.extend(self.get_behaviors(klass))
        for dev in self.devices:
            if isinstance(dev, Board):
                behs.extend(dev.get_behaviors_include_attachments(klass))
            else:
                behs.extend(dev.get_behaviors(klass))
        return behs

    def destory(self):
        super().destory()
        for dev in self.devices:
            dev.on_detatched()
            dev.destory()
        self.devices = []


class RCU(Board):

    def __init__(self):
        super().__init__()
        self.num_of_cores = 1
        self._config = None
        self._engine = Engine()

    @property
    def engine(self) -> Engine:
        return self._engine

    def spin(self, max_threads: int = None):
        max_threads = max_threads or self.num_of_cores
        assert max_threads <= self.num_of_cores, 'Invalid max threads'
        self.engine.spin(max_threads)

    def shutdown(self):
        self.engine.shutdown()

    def destory(self):
        self.shutdown()
        super().destory()


class Sensor(Attachable):

    def __init__(self):
        super().__init__()
        self.probe_angle = 0.0

    @abstractmethod
    def detect(self, timeout: float = 0.001) -> bool:
        pass


class Ranged(Sensor):

    def __init__(self):
        super().__init__()
        self.max_val = 255.0
        self.min_val = 0.0
        self.value = 0.0


class Infrared(Ranged):

    def __init__(self):
        super().__init__()


class CompoundEye(Infrared):

    def __init__(self):
        super().__init__()
        self.num_of_channels = 0
        self.max_ir = 0
        self.max_ir_dir = 0.0


class GrayScale(Ranged):

    def __init__(self):
        super().__init__()
        self.ctr = 1.0


class Ultrasonic(Ranged):

    def __init__(self):
        super().__init__()
        self.accuracy = 0.0


class Compass(Ranged):

    def __init__(self):
        super().__init__()
        self.max_val = 360.0
        self.min_val = 0.0
        self.declination = 0
        self.calibration = [[1.0, 0.0, 0.0],
                            [0.0, 1.0, 0.0],
                            [0.0, 0.0, 1.0]]


class Color(Sensor):

    def __init__(self):
        super().__init__()
        self.channels = 0
        self.value: List[int] = []


class Motor(Attachable):

    def __init__(self):
        super().__init__()
        self.direction = 0

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class Servo(Motor):

    def __init__(self):
        super().__init__()
        self.speed = 0.0


class Bulb(Attachable):

    def __init__(self):
        super().__init__()
        self.color: List[int] = []

    @abstractmethod
    def change_color(self, color: List[int]):
        pass


class Switch(Attachable):

    @abstractmethod
    def read_state(self) -> int:
        pass
