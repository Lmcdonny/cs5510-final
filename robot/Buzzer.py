'''Class responsible for controlling the hardware buzzer'''
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
        self.speak(self.HIGH_FREQ, .2)
        self.speak(self.LOW_FREQ, .2)
        self.stop()

    def found(self):
        self.start()
        self.speak(self.LOW_FREQ, .2)
        self.speak(self.HIGH_FREQ, .2)
        self.stop()

    def start(self):
        self.buzz.start(50)

    def startup(self):
        self.start()
        self.speak(self.LOW_FREQ, .1)
        self.stop()
        time.sleep(0.1)
        self.start()
        self.speak(self.LOW_FREQ, .1)
        self.stop()
        self.start()
        self.speak(self.LOW_FREQ, .1)
        self.stop()
        time.sleep(0.05)
        self.start()
        self.speak(self.HIGH_FREQ, .3)
        self.stop()

    def speak(self, freq, sleep, dc=50):
        self.buzz.start(dc)
        self.buzz.ChangeFrequency(freq)
        time.sleep(sleep)

    def stop(self):
        self.buzz.stop()

    def close(self):
        self.start()
        self.speak(self.HIGH_FREQ, .1)
        self.stop()
        time.sleep(0.1)
        self.start()
        self.speak(self.HIGH_FREQ, .1)
        self.stop()
        self.start()
        self.speak(self.HIGH_FREQ, .1)
        self.stop()
        time.sleep(0.05)
        self.start()
        self.speak(self.LOW_FREQ, .3)
        self.stop()

        GPIO.cleanup()


if __name__ == '__main__':
    buzz = Buzzer()
    try:
        while True:
            buzz.start()
            buzz.found()
            time.sleep(0.5)
            buzz.lost()

    except:
        buzz.stop()
        buzz.close()
    
