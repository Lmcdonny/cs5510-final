'''Internal representation of the robot to be used by the controller'''

from Skidsteer_Robot import Skidsteer_Robot
import utils.objectives as obs
from Car import Car

car = Car()

class Follow_Bot(Skidsteer_Robot):
    def __init__(self, startpos, width, hz, mode='sim'):
        super().__init__(startpos, width, hz)

        self.mode = mode
        self.objective = obs.IDLE

    def operate(self, bbDims, distance):
        #y = 480
        #x = 640
        #bbDims = [[x, y],
        #          [x, y],
        #          [x, y],
        #          [x, y]]
        if (bbDims == None):
            car.stop()
        
        else:
            bbCenterY = ((abs(bbDims[0][1] - bbDims[3][1]) + bbDims[0][1]) + (abs(bbDims[1][1] - bbDims[2][1]) + bbDims[1][1])) / 2
            bbCenterX = ((abs(bbDims[0][0] - bbDims[3][0]) + bbDims[0][0]) + (abs(bbDims[1][0] - bbDims[2][0]) + bbDims[1][0])) / 2
            bbCenter = [bbCenterX, bbCenterY]
            print("bbCenter: ", bbCenter)
            vidSize = [640, 480]
            print("vidSize: ", vidSize)
            center = [vidSize[0] / 2, vidSize[1] / 2]
            print("center: ", center)

            minDist = 200

            if bbCenter[0] < center[0]:
                #turn left
                car.control_car(250, 0)
                print("Turniing left")
            elif bbCenter[0] > center[0]:
                #turn right
                car.control_car(0, 250)
                print("Turning right")
            elif bbCenter[0] == center[0] and distance > minDist:
                #continue straight
                car.control_car(250, 250)
                print("Going straight")

            else:
                car.stop()
                print("Stop")

    def set_l(self, power):
        if self.mode == 'sim':
            super().set_l(power)

    def set_r(self, power):
        if self.mode == 'sim':
            super().set_r(power)

if __name__ == '__main__':
    bot = Follow_Bot((0,0), 3, 3, mode='real')
    bot.set_v(0, 0)
