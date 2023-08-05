import signal
import subprocess
import sys
import time
import RPi.GPIO as GPIO

SWITCH_PIN = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def main(args=sys.argv[1:]):
    while GPIO.input(SWITCH_PIN) != 0:
        time.sleep(0.05)
    start = time.time()
    proc = subprocess.Popen([sys.executable, args[0]])
    while proc.poll() is None:
        if GPIO.input(SWITCH_PIN) == 0 and time.time() - start > 1:
            break
        time.sleep(0.05)
    proc.send_signal(signal.SIGINT)
    time.sleep(0.5)
    proc.kill()
    main(args)


if __name__ == '__main__':
    main()
