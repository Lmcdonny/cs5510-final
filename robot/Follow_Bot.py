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

        self.car = Car()
        # Init camera servo settings
        self.car.set_servo(1, 90)
        sleep(0.1)
        self.car.set_servo(2, 100)
        sleep(0.1)

        self.lv = 0
        self.rv = 0
        self.v_max = 255

    def operate(self, bbDims, distance, verbose=False):
        print('Follow_Bot.py: self.objective')
        if distance < 50:
            self.stop()
        elif self.objective == obs.FOUND:
            #y = 480
            #x = 640
            #bbDims = [[x, y],
            #          [x, y],
            #          [x, y],
            #          [x, y]]
            if (bbDims is None):
                print("Follow_Bot.py: No Bounding box")
                self.stop()
            
            else:
                # bbCenterY = ((abs(bbDims[0][1] - bbDims[3][1]) + bbDims[0][1]) + (abs(bbDims[1][1] - bbDims[2][1]) + bbDims[1][1])) / 2
                # bbCenterX = ((abs(bbDims[0][0] - bbDims[3][0]) + bbDims[0][0]) + (abs(bbDims[1][0] - bbDims[2][0]) + bbDims[1][0])) / 2
                
                bbCenterY = (bbDims[0][1] - (abs(bbDims[0][1] - bbDims[1][1]) / 2))
                bbCenterX = (bbDims[0][0] + (abs(bbDims[0][0] - bbDims[1][0]) / 2))
                bbCenter = [bbCenterX, bbCenterY]
                print("Follow_Bot.py: Bounding Box center -> ", bbCenter)
                
                vidSize = [640, 480]
                
                center = [vidSize[0] / 2, vidSize[1] / 2]
                
                if verbose:
                    print("Follow_Bot.py: bbCenter: ", bbCenter)
                    print("Follow_Bot.py: vidSize: ", vidSize)
                    print("Follow_Bot.py: center: ", center)

                minDist = 100

                if center[0] + 50 > bbCenter[0] and bbCenter[0] > center[0] - 50:
                    # and distance > minDist
                    #continue straight
                    self.set_v(self.v_max * 0.25, self.v_max * 0.25)
                    if verbose:
                        print("Follow_Bot.py: Going straight")
                elif bbCenter[0] < center[0]:
                    #turn left
                    self.turn_left()
                    if verbose:
                        print("Follow_Bot.py: Turniing left")
                elif bbCenter[0] > center[0]:
                    #turn right
                    self.turn_right()

                    if verbose:
                        print("Follow_Bot.py: Turning right")

                else:
                    self.car.stop()
                    if verbose:
                        print("Follow_Bot.py: Stop")
        elif self.objective == obs.LOST:
            pass

    def turn_left(self):
        self.set_v(-self.v_max * 0.25, self.v_max * 0.25)
        

    def turn_right(self):
        self.set_v(self.v_max * 0.25, -self.v_max * 0.25)


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

if __name__ == '__main__':
    bot = Follow_Bot(25)
    bot.set_v(0, 0)
