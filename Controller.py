'''
Main class that receives input, makes decision, and issues 
commands to the various moving parts of the system
'''
from threading import Thread
from robot.utils import objectives as obs
from time import time

class Controller:
    def __init__(self, yolo, ultrasonic, robot):
        self.yolo = yolo
        self.ultrasonic = ultrasonic
        self.robot = robot

    def run(self):
        try:
            # Main loop
            found_person = False
            self.yolo.predict()
            t = Thread(target=self.yolo.camshift, args=[])
            yolo_thread = Thread(target=self.yolo.predict, args=[])
            t.start()
            runtime = 0
            start = time()
            while True:
                # Get sensor info
                temp_found_person = self.yolo.target_found
                boundingBoxDims = self.yolo.bounding_box
                dist = self.ultrasonic.distance()

                # Determine state
                    # Toggling
                if found_person and not temp_found_person:
                    # cant find person
                    self.robot.set_ob(obs.LOST)
                    found_person = False
                    print("Controller.py: Lost Person")
                    # yolo loop til someones found
                    self.yolo.predict()
                elif not found_person and temp_found_person:
                    # beeeep found a new target
                    self.robot.set_ob(obs.FOUND)
                    found_person = True
                    print("Controller.py: Found Person")

                # Invoke robot decision
                self.robot.operate(boundingBoxDims, dist, True)
                runtime = time() - start
                if runtime > 6:
                    if not yolo_thread.is_alive():
                        yolo_thread.start()
                        start = time()
        except KeyboardInterrupt:
            # if anything fails
            self.print('Shutting down: Keyboard Interrupt')
            self.close()
            exit()
        except Exception as e:
            print(e)
            self.robot.stop()
            self.close()
            exit()

    def close(self):
        self.yolo.close()
        self.robot.stop()
        self.robot.close()

    def print(lself, message):
        print(f"Controller.py: {message}")