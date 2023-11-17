'''
Ackerman steering representation of a robot. Included purely for reference.
'''
from ROBOT import Robot
import math
from utils.geometry import distance
import utils.objectives as obs
import numpy as np

class Ackerman_Robot(Robot):
    def __init__(self, startpos, width, length, hz):
        super().__init__(startpos, width, hz)

        self.l = length * self.m2p # Length stored in pixels
        self.a = math.radians(0) # Turning angle stored as radians
        self.max_v = 8 * self.m2p # Velocity in m/s converted to pixels/s
        self.v = self.max_v

        self.max_a = math.radians(45.0) # Standard cramp angle of napa fire truck https://www.cityofnapa.org/DocumentCenter/View/1492/Fire-Apparatus-Turn-Information-PDF
        
        self.objective = obs.GET_TO_CIRCLE # Initial objective

    def operate(self, circpos, r):
        '''Instructions for the robot.

            Args:
                circpos (tuple, list): Center position of the circle
                r (int, float): Radius of the circle
        '''
        if self.objective == obs.IDLE:
            self.v = 0
            self.set_turn(0)
        elif self.objective == obs.GET_TO_CIRCLE:
            # self.set_turn(self.max_a * 0.5)
            # self.objective = obs.ALIGN_TO_CIRCLE
            dist = distance((self.x, self.y), circpos)
            if dist < r:    
                self.set_turn(self.max_a * 1)
                print(self.a)
            else:
                self.objective = obs.ALIGN_TO_CIRCLE
            
        elif self.objective == obs.ALIGN_TO_CIRCLE:
            dist = distance((self.x, self.y), circpos)
            if self.heading >= (np.pi + np.pi * 0.09):
                self.set_turn(0)
                if dist <= r:
                    self.objective = obs.FOLLOW_CIRCLE
                    self.v = 0
            else:
                self.set_turn(self.max_a)
        
        elif self.objective == obs.FOLLOW_CIRCLE:
            self.v = self.max_v
            self.set_turn(self.max_a * 0.68)

        elif self.objective == obs.DEBUG:
            dist = distance((self.x, self.y), circpos)
            if dist >= r:
                self.v = 0

    def follow_circle(self, circpos, r):
        dist = distance((self.x, self.y), circpos)
        
        self.set_turn((dist-r) / self.max_a)      
    
    def set_turn(self, a):
        if a > self.max_a:
            self.a = self.max_a
            return
        if a < -self.max_a:
            self.a = -self.max_a
            return
        self.a = a


    def get_v(self, side):
        return self.v

    def kinematics(self, dt):
        self.x += self.v * math.sin(self.heading) * dt
        self.y += self.v * math.cos(self.heading) * dt

        self.set_heading(self.heading + ((self.v / self.l) * math.tan(self.a)) * dt)
