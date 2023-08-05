
from ..pin import DIGPin, IOFlow, PWMPin, MISOPin, MOSIPin, SCLPin, SCLKPin, SDAPin
from ..device import Board, RCU
from ..engine import Engine
import RPi.GPIO as GPIO


class RBP_GPIO(DIGPin):

    def on_setup(self, host: Board):
        if self.flow == IOFlow.OUT:
            GPIO.setup(self.num, GPIO.OUT)
        elif self.flow == IOFlow.IN:
            if self.tag == 'pull_up':
                GPIO.setup(self.num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            elif self.tag == 'pull_down':
                GPIO.setup(self.num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                GPIO.setup(self.num, GPIO.IN)

    def input(self) -> int:
        assert self.flow == IOFlow.IN, 'Invalid IOFlow'
        return GPIO.input(self.num)

    def output(self, val: int):
        assert self.flow == IOFlow.OUT, 'Invalid IOFlow'
        GPIO.output(self.num, val)


class RBP_PWM(PWMPin):

    def on_setup(self, host: Board):
        GPIO.setup(self.num, GPIO.OUT)
        self.pwm = GPIO.PWM(self.num, 50)

    def start(self, dc=0):
        self.pwm.start(dc)

    def stop(self):
        self.pwm.stop()

    def change_frequency(self, freq):
        self.pwm.ChangeFrequency(freq)

    def change_duty_cycle(self, dc):
        self.pwm.ChangeDutyCycle(dc)


RBP_SLOTS = [SDAPin(2), SCLPin(3), RBP_GPIO(4), RBP_GPIO(5),
             RBP_GPIO(6), RBP_GPIO(7), RBP_GPIO(8), MOSIPin(9),
             MISOPin(10), SCLKPin(11), RBP_PWM(12), RBP_PWM(13),
             RBP_GPIO(14), RBP_GPIO(15), RBP_GPIO(16), RBP_GPIO(17),
             RBP_GPIO(18), RBP_GPIO(19), RBP_GPIO(20), RBP_GPIO(21),
             RBP_GPIO(22), RBP_GPIO(23), RBP_GPIO(24), RBP_GPIO(25)]


class RBP_34(RCU):

    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.num_of_cores = 4
        self.name = 'Raspberry Pi'
        self.slots = RBP_SLOTS.copy()

    def destory(self):
        super().destory()
        GPIO.cleanup()
