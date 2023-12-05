'''Internal representation of the robot to be used by the controller'''

from robot.Skidsteer_Robot import Skidsteer_Robot
import robot.utils.objectives as obs
from robot.Car import Car
from robot.Buzzer import Buzzer
from time import sleep

class Follow_Bot(Skidsteer_Robot):
    def __init__(self, w):
        super().__init__((1,1), w, 2)
        self.objective = obs.LOST
        self.buzz = Buzzer()

        self.lv = 0
        self.rv = 0
        self.turn_strength = 0.20
        self.turn_thresh = 25
        self.v_max = 255
        self.min_dist = 100

        self.car = Car()
        self.startup()

    def operate(self, bbDims, distance, verbose=False):
        self.print(f'obj: {self.objective}')
        self.print(f'dist: {distance}')
        if self.objective == obs.FOUND:
            if (bbDims is None):
                self.print("No Bounding box")
                self.stop()
            
            else:
                bbCenterX = (bbDims[0][0] + bbDims[1][0] + bbDims[2][0] + bbDims[3][0]) / 4
                self.print(f"Bounding Box center -> {bbCenterX}")
                
                vidSize = [640, 480]
                
                center = [vidSize[0] / 2, vidSize[1] / 2]
                
                if verbose:
                    self.print(f"bbCenter: {bbCenterX}")
                    self.print(f"vidSize: {vidSize}")
                    self.print(f"center: {center}")

                if distance < self.min_dist and distance > 0:
                    self.stop()
                elif center[0] + self.turn_thresh > bbCenterX and bbCenterX > center[0] - self.turn_thresh:
                    #continue straight
                    self.set_v(self.v_max * 0.25, self.v_max * 0.25)
                    if verbose:
                        self.print("Going straight")
                elif bbCenterX < center[0]:
                    #turn left
                    self.turn_left()
                    if verbose:
                        self.print("Turning left")
                elif bbCenterX > center[0]:
                    #turn right
                    self.turn_right()
                    if verbose:
                        self.print("Turning right")

                else:
                    self.car.stop()
                    if verbose:
                        self.print("Stop")
        elif self.objective == obs.LOST:
            self.stop()

    def turn_left(self):
        self.set_v(-self.v_max * self.turn_strength, self.v_max * self.turn_strength)
        

    def turn_right(self):
        self.set_v(self.v_max * self.turn_strength, -self.v_max * self.turn_strength)


    def set_ob(self, objective):
        '''Handles changing objective. When objective changes, an action happens'''
        if self.objective != objective:
            if objective == obs.LOST:
                self.set_v(0, 0)
                self.buzz.lost()
            elif objective == obs.FOUND:
                self.buzz.found()

        self.objective = objective

    def set_v(self, l, r):
        self.set_l(int(l))
        self.set_r(int(r))
        self.car.control_car(self.vl, self.vr)

    def stop(self):
        self.car.stop()

    def close(self):
        self.buzz.close()

    def print(self, message):
        print(f"Follow_Bot.py: {message}")

    def startup(self):
        # Init camera servo settings
        self.car.set_servo(1, 90)
        sleep(0.1)
        self.car.set_servo(2, 100)
        sleep(0.1)

        # Startup beeps
        self.buzz.startup()

if __name__ == '__main__':
    bot = Follow_Bot(25)
    bot.set_v(0, 0)
