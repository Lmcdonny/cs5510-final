'''Internal representation of the robot to be used by the controller'''

from Skidsteer_Robot import Skidsteer_Robot
import utils.objectives as obs

class Follow_Bot(Skidsteer_Robot):
    def __init__(self, startpos, width, hz, mode='sim'):
        super().__init__(startpos, width, hz)

        self.mode = mode
        self.objective = obs.IDLE

    def operate(self):
        pass

    def set_l(self, power):
        if self.mode == 'sim':
            super().set_l(power)

    def set_r(self, power):
        if self.mode == 'sim':
            super().set_r(power)

if __name__ == '__main__':
    bot = Follow_Bot((0,0), 3, 3, mode='real')
    bot.set_v(0, 0)