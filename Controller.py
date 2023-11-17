'''

'''
from cv2 import waitKey

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

        while True:
            # Get sensor info
            img = self.camera.read()
            pos, temp_found_person = self.yolo.predict(img)
            target_dist = self.ultrasonic.sense(pos) # sense is a placeholder

            # Determine state
            

                # Toggling
            if found_person and not temp_found_person:
                # cant find person
                # beep beep sheep sheep
                # stop moving
                # yolo loop til someones found
                found_person = False
                print("Lost Person")
                pass
            elif not found_person and temp_found_person:
                # beeeep found a new target
                found_person = True
                print("Found Person")

            # Invoke robot decision
            self.robot.operate()

            # If esc is pressed break
            if waitKey(1) & 0xFF == ord(' '):
                self.close()
                break

    def close(self):
        self.camera.close()