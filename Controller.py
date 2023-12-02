'''

'''
from cv2 import waitKey
from threading import Thread
from robot.utils import objectives as obs
from time import sleep, time

class Controller:
    def __init__(self, camera, yolo, ultrasonic, robot):
        self.camera = camera
        self.yolo = yolo
        self.ultrasonic = ultrasonic
        self.robot = robot
        self.state = 0

    def run(self):
        # Main loop
        found_person = False
        self.yolo.predict()
        t = Thread(target=self.yolo.camshift, args=[])
        t.start()
        runtime = 0
        start = time()
        while True:
            # Get sensor info
            temp_found_person = self.yolo.target_found
            boundingBoxDims = self.yolo.bounding_box
            dist = self.ultrasonic.distance() # sense is a placeholder

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
            if runtime > 5:
                self.yolo.predict()

            # If esc is pressed break
            if waitKey(1) & 0xFF == ord(' '):
                self.close()
                break

    def close(self):
        self.camera.close()
        self.robot.close()