'''
Solution to part (a) of question 2 on the midterm
'''

from utils.Circle import Circle
from Simulation import Simulation
from robot.Ackerman_Robot import Ackerman_Robot
from Graphics import Graphics
from utils.sim_settings import SIM_CENTER, RESOLUTION, ROBOT_DIMS

def main():
    RADIUS = 18 # in meters

    # Circle
    circle = Circle(RADIUS, SIM_CENTER)

    # Robot
    robot = Ackerman_Robot(SIM_CENTER, ROBOT_DIMS[0], ROBOT_DIMS[1], 2)

    # Graphics
    gfx = Graphics(RESOLUTION, circle, 'assets/firetruck.png', ROBOT_DIMS)

    # Simulation
    sim = Simulation('a', gfx, robot, circle)
    sim.run()
    

if __name__ == '__main__':
    main()