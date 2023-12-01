import time
import RPi.GPIO as GPIO

class Buzzer:
    HIGH_FREQ = 400
    LOW_FREQ = 200

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(32, GPIO.OUT)
        self.buzz = GPIO.PWM(32, 440)
        self.curr_freq = 50.0
        # self.max_freq = 

    def lost(self):
        self.start()
        self.buzz.start(50)
        self.buzz.ChangeFrequency(self.HIGH_FREQ)
        time.sleep(.2)
        self.buzz.ChangeFrequency(self.LOW_FREQ)
        time.sleep(.2)
        self.stop()

    def found(self):
        self.start()
        self.buzz.ChangeFrequency(self.LOW_FREQ)
        time.sleep(.2)
        self.buzz.ChangeFrequency(self.HIGH_FREQ)
        time.sleep(.2)
        self.stop()

    def start(self):
        self.buzz.start(50)

    def stop(self):
        self.buzz.stop()

    def close(self):
        GPIO.cleanup()


if __name__ == '__main__':
    buzz = Buzzer()
    buzz.start()
    buzz.close()