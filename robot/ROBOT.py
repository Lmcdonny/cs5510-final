'''
Class for handling robot control and kinematics
'''
from abc import abstractmethod
from abc import ABC
from robot.utils.geometry import m_to_pixel
import robot.utils.objectives as obs
from numpy import pi

class Robot(ABC):
    def __init__(self, startpos, width, hz):
        self.hz = hz
        self.m2p = m_to_pixel # From meters to pixels
        self.w = width * self.m2p

        self.x = startpos[0]
        self.y = startpos[1]
        self.heading = 0.0

        self.objective = obs.IDLE

    @abstractmethod
    def operate(self, circpos, r):
        pass

    @abstractmethod
    def get_v(self, side):
        pass

    def set_heading(self, heading):
        self.heading = heading % (2 * pi)

    @abstractmethod
    def kinematics(self, dt):
        pass
    