'''
Our implementation of a skidsteer robot
'''
from robot.ROBOT import Robot
from robot.utils.geometry import distance, tangent_angle, compare_angles
import robot.utils.objectives as obs
import numpy as np

class Skidsteer_Robot(Robot):
    def __init__(self, startpos, width, hz):
        super().__init__(startpos, width, hz)
        self.v_max = 8 * self.m2p # Max speed in m/s converted to pixels/s
        self.vr = 0
        self.vl = 0

        # self.objective = obs.GET_TO_CIRCLE

    def operate(self, circpos, r):
        if self.objective == obs.IDLE:
            self.set_v(0, 0)
        elif self.objective == obs.GET_TO_CIRCLE:
            dist = distance((self.x, self.y), circpos)
            if dist < r - 5:
                x = self.hz * (r - dist)
                self.set_v(x, x)
            else:
                self.set_v(0, 0)
                print('GET_TO_CIRCLE complete.')
                self.objective = obs.ALIGN_TO_CIRCLE
        elif self.objective == obs.ALIGN_TO_CIRCLE:
            tangent = tangent_angle((self.x, self.y), circpos)
            compare = compare_angles(tangent, self.heading)
            if compare > 0:
                self.turn(compare)
            else:
                self.set_v(0, 0)
                self.objective = obs.FOLLOW_CIRCLE
                print('ALIGN_TO_CIRCLE complete.')
        elif self.objective == obs.FOLLOW_CIRCLE:
            tangent = tangent_angle((self.x, self.y), circpos)
            compare = compare_angles(tangent, self.heading)

            self.follow_circle(r)

        elif self.objective == obs.DEBUG:
            pass

    def follow_circle(self, r):
        vl = -((self.w * (self.v_max * 0.225) * (self.hz ** 2)) / r) + self.v_max
        self.set_v(vl, self.v_max)

    def set_l(self, s):
        if s >= self.v_max:
            self.vl = self.v_max
        elif s <= -self.v_max:
            self.vl = -self.v_max
        else:
            self.vl = s

    def set_r(self, s):
        if s >= self.v_max:
            self.vr = self.v_max
        elif s <= -self.v_max:
            self.vr = -self.v_max
        else:
            self.vr = s

    def set_v(self, sl, sr):
        self.set_l(sl)
        self.set_r(sr)

    def turn(self, angle):
        vr = (self.hz * self.w * angle) / 2
        vl = -vr
        self.set_v(vl, vr)

    def get_v(self, side):
        if side == 0:
            return self.vl
        else:
            return self.vr

    def kinematics(self, dt):
        self.x += ((self.vr + self.vl) / 2) * np.sin(self.heading) * dt
        self.y += ((self.vr + self.vl) / 2) * np.cos(self.heading) * dt

        self.set_heading(self.heading + ((self.vr - self.vl) / self.w) * dt)