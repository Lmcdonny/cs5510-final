import time
import RPi.GPIO as GPIO

class Buzzer:
    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(32, GPIO.OUT)
        self.buzz = GPIO.PWM(32, 440)

        # self.max_freq = 

    def start(self):
        self.buzz.start(50)
        try:
            while 1:
                self.buzz.stop()
                time.sleep(.5)
                self.buzz.start(50)
                time.sleep(.1)

                # for dc in range(0, 101, 5):
                #     print('start_1')
                #     self.buzz.ChangeDutyCycle(dc)
                #     time.sleep(0.1)
                # for dc in range(100, -1, -5):
                #     self.buzz.ChangeDutyCycle(dc)
                #     print('start_2')
                #     time.sleep(0.1)

        except KeyboardInterrupt:
            pass

        self.stop()

    def stop(self):
        self.buzz.stop()

    def close(self):
        GPIO.cleanup()


if __name__ == '__main__':
    buzz = Buzzer()
    buzz.start()
    buzz.close()