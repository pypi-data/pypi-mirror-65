from rclpy.executors import Task
from rclpy.node import Node, Publisher, Subscription
from typing import Callable, Coroutine, Dict, Generic, List, Type, TypeVar, Union
from . import device
from .util import generate_id
import time

T = TypeVar('T')
TB = TypeVar('TB', bound='Behavior')
TD = TypeVar('TD', bound='Device')


class Behavior(Node):

    def __init__(self):
        id = generate_id(type(self))
        super().__init__(id)
        self.id = id
        self._enabled = True
        self._engine = None
        self._update = 'on_update' in type(self).__dict__

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, val: bool):
        self._enabled = val
        if self._enabled:
            self.on_enable()
        else:
            self.on_disable()

    def run_task(self, callback: Union[Callable, Coroutine]) -> Task:
        return self._engine.execute(callback, isinstance(callback, Coroutine))

    async def delay(self, sec: int):
        if sec == 0:
            await self.run_task(lambda: None)
        else:
            start = time.time()
            while time.time() - start < sec:
                await self.run_task(lambda: None)

    def on_awake(self):
        pass

    def on_start(self):
        pass

    def on_enable(self):
        pass

    def on_disable(self):
        pass

    def on_update(self):
        pass

    def on_destory(self):
        pass


class EventBehavior(Behavior):

    def __init__(self):
        super().__init__()
        self._pubrs: Dict[str, Publisher] = {}
        self._subrs: Dict[Callable, List[Subscription]] = {}

    def publish(self, topic: str, msg_type: Type[T], msg: T):
        pubr = self._pubrs.get(topic)
        if not pubr:
            pubr = self.create_publisher(msg_type, topic, 10)
            self._pubrs[topic] = pubr
        pubr.publish(msg)

    def subscribe(self, topic: str, msg_type: Type[T], handler: Callable[[T], None]):
        subrs = self._subrs.get(handler)
        if not subrs:
            self._subrs[handler] = subrs = []
        subr = self.create_subscription(msg_type, topic, handler, 10)
        subrs.append(subr)

    def unsubscribe(self, handler: Callable):
        subrs = self._subrs.get(handler)
        if subrs:
            for subr in subrs:
                self.destroy_subscription(subr)
            self._subrs.pop(handler)


class DeviceBehavior(EventBehavior, Generic[TD]):

    def __init__(self):
        super().__init__()
        self.device: U = None

    @property
    def device_name(self) -> str:
        return self.device.name

    def attach_behavior(self, klass: Type[TB]) -> TB:
        return self.device.attach_behavior(klass)

    def detatch_behavior(self, beh: Behavior):
        self.device.detatch_behavior(beh)

    def get_behavior(self, klass: Type[TB], include_host: bool = False, include_attachments: bool = False) -> TB:
        beh = self.device.get_behavior(klass)
        if not beh and include_host and isinstance(self.device, device.Attachable):
            beh = self.device.get_behavior_include_host(klass)
        if not beh and include_attachments and isinstance(self.device, device.Board):
            beh = self.device.get_behavior_include_attachments(klass)
        return beh

    def get_behaviors(self, klass: Type[TB], include_host: bool = False, include_attachments: bool = False) -> List[TB]:
        behs = []
        behs.extend(self.device.get_behaviors(klass))
        if include_host and isinstance(self.device, device.Attachable):
            behs.extend(self.device.get_behaviors_include_host(klass))
        if include_attachments and isinstance(self.device, device.Board):
            behs.extend(self.device.get_behaviors_include_attachments(klass))
        return behs
