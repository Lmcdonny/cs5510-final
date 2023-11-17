'''
Simulation settings
'''
from utils.geometry import ft_to_m

RESOLUTION = (720, 1280) # in pixels
SIM_CENTER = (RESOLUTION[1] // 2, RESOLUTION[0] // 2)
# Width then length
ROBOT_DIMS = (10 * ft_to_m, 35 * ft_to_m) # in meters