'''

'''
from cv2 import waitKey
from threading import Thread

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
        t = Thread(target=self.yolo.camshift, args=[])
        t.start()
        while True:
            # Get sensor info
            img = self.camera.read()
            temp_found_person = self.yolo.target_found
            boundingBoxDims = self.yolo.bounding_box
            dist = self.ultrasonic.distance() # sense is a placeholder

            # Determine state
            

                # Toggling
            if found_person and not temp_found_person:
                # cant find person
                # beep beep sheep sheep
                # stop moving
                self.robot.operate(None, -1)
                # yolo loop til someones found
                found_person = False
                print("Lost Person")
                pass
            elif not found_person and temp_found_person:
                # beeeep found a new target
                found_person = True
                print("Found Person")

            # Invoke robot decision
            self.robot.operate(boundingBoxDims, dist)

            # If esc is pressed break
            if waitKey(1) & 0xFF == ord(' '):
                self.close()
                break

    def close(self):
        self.camera.close()