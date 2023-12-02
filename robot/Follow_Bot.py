'''Internal representation of the robot to be used by the controller'''

from robot.Skidsteer_Robot import Skidsteer_Robot
import robot.utils.objectives as obs
from robot.Car import Car
from robot.Buzzer import Buzzer

class Follow_Bot(Skidsteer_Robot):
    def __init__(self, hz=2):
        super().__init__((1,1), 1, hz)
        self.objective = obs.LOST
        self.buzz = Buzzer()

        self.car = Car()
        self.lv = 0
        self.rv = 0
        self.v_max = 255

    def operate(self, bbDims, distance, verbose=False):
        if self.objective == obs.FOUND:
            #y = 480
            #x = 640
            #bbDims = [[x, y],
            #          [x, y],
            #          [x, y],
            #          [x, y]]
            if (bbDims == None):
                self.stop()
            
            else:
                bbCenterY = ((abs(bbDims[0][1] - bbDims[3][1]) + bbDims[0][1]) + (abs(bbDims[1][1] - bbDims[2][1]) + bbDims[1][1])) / 2
                bbCenterX = ((abs(bbDims[0][0] - bbDims[3][0]) + bbDims[0][0]) + (abs(bbDims[1][0] - bbDims[2][0]) + bbDims[1][0])) / 2
                bbCenter = [bbCenterX, bbCenterY]
                
                vidSize = [640, 480]
                
                center = [vidSize[0] / 2, vidSize[1] / 2]
                
                if verbose:
                    print("bbCenter: ", bbCenter)
                    print("vidSize: ", vidSize)
                    print("center: ", center)

                minDist = 100

                if bbCenter[0] < center[0]:
                    #turn left
                    self.set_v(self.v_max, 0)
                    if verbose:
                        print("Turniing left")
                elif bbCenter[0] > center[0]:
                    #turn right
                    self.set_v(0, self.v_max)
                    if verbose:
                        print("Turning right")
                elif bbCenter[0] == center[0]:
                    # and distance > minDist
                    #continue straight
                    self.set_v(self.v_max, self.v_max)
                    if verbose:
                        print("Going straight")

                else:
                    self.car.stop()
                    if verbose:
                        print("Stop")
        elif self.objective == obs.LOST:
            pass

    def set_ob(self, objective):
        '''Handles changing objective. When objective changes, an action happens'''
        if self.objective != objective:
            if objective == obs.LOST:
                self.set_v(0, 0)
                self.buzz.lost()
            elif objective == obs.FOUND:
                self.buzz.found()

    def set_v(self, l, r):
        self.set_l(l)
        self.set_r(r)
        self.car.control_car(self.vl, self.vr)

    def stop(self):
        self.car.stop()

    def close(self):
        self.buzz.close()

if __name__ == '__main__':
    bot = Follow_Bot((0,0), 3, 3, mode='real')
    bot.set_v(0, 0)
