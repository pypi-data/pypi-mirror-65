import rclpy
from rclpy.executors import Executor, SingleThreadedExecutor, MultiThreadedExecutor, Task
from typing import Callable, Coroutine, List, Type, TypeVar, Union
from . import behavior

TB = TypeVar('TB', bound='Behavior')


class Engine():

    def __init__(self):
        self.spinning = False
        self.behaviors: List[behavior.Behavior] = []
        self.main_executor: Executor = None
        self.co_executor: Executor = None
        rclpy.init()

    def execute(self, callback: Union[Callable, Coroutine], main_thread: bool = True) -> Task:
        return self.main_executor.create_task(callback) if main_thread else self.co_executor.create_task(callback)

    def spin(self, max_threads: int = 1):
        if self.spinning:
            return
        self.spinning = True
        self.main_executor = SingleThreadedExecutor()
        self.co_executor = MultiThreadedExecutor(max_threads)
        for beh in self.behaviors:
            self.init_behavior(beh)
        self.main_executor.spin_once(0)
        try:
            while self.spinning:
                for beh in self.behaviors:
                    if beh._update and beh.enabled:
                        self.execute(lambda b=beh: b.on_update())
                self.main_executor.spin_once(0)
                self.co_executor.spin_once(0)
        finally:
            self.shutdown()

    def shutdown(self):
        if not self.spinning:
            return
        self.spinning = False
        for beh in self.behaviors:
            beh.enabled = False
            beh.on_destory()
            beh._engine = None
        self.behaviors = []
        self.main_executor.shutdown()
        self.co_executor.shutdown()

    def init_behavior(self, beh: behavior.Behavior):
        beh.on_awake()
        if beh.enabled:
            self.execute(lambda: beh.on_start())
        self.co_executor.add_node(beh)

    def spawn_behavior(self, klass: Type[TB]) -> TB:
        beh = klass()
        beh._engine = self
        beh.enabled = True
        self.behaviors.append(beh)
        if self.spinning:
            self.init_behavior(beh)
        return beh

    def destory_behavior(self, beh: behavior.Behavior):
        if beh not in self.behaviors:
            return
        if self.spinning:
            self.co_executor.remove_node(beh)
        self.behaviors.remove(beh)
        beh.enabled = False
        beh.on_destory()
        beh._engine = None
