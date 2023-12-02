import numpy as np

# Conversions
ft_to_m = 0.3048 # Conversion factor applied to feet to obtain meter value
m_to_pixel = 15 # What we want our relative space to be

# Given the coordinates of two points, return the distance between them
def distance(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.linalg.norm(p1-p2)

# Given the circle center position, the point of a position in the same plane as the circle,
# and the radius of the circle, return the x, y, and distance of ppos from the closest point
def closest_point(circpos, ppos, r):
    cX = circpos[0]
    cY = circpos[1]
    vX = ppos[0] - cX
    vY = ppos[1] - cY
    magV = np.sqrt(vX ** 2 + vY ** 2)
    dX = cX + (vX / magV) * r
    dY = cY + (vY / magV) * r
    d = distance((ppos[0], ppos[1]), (dX, dY))

    return dX, dY, d

def tangent_angle(ppos, cpos):
    '''Given a point on the circle and circle center info, return the tangent angle. Currently throws /0 warnings.
    
        Args:
            ppos (tuple, list): position of the point on the circle's border
            cpos (tuple, list): position of the center of the circle
    '''
    x = ppos[0] - cpos[0]
    y = ppos[1] - cpos[1]
    if x == 0:
        if y >= 0:
            return 0 + (np.pi / 2)
        else:
            return np.pi + (np.pi / 2)
    if y == 0:
        if x >= 0:
            return (np.pi / 2) + (np.pi / 2)
        else:
            return ((3 * np.pi) / 2) + (np.pi / 2)
    tangent = (np.tan(y / x) + (np.pi / 2)) % (2 * np.pi)
    return tangent

# Return the difference of ang1 to ang2 yoinked from here: https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def compare_angles(ang1, ang2):
    a = (ang1 + np.pi) - (ang2 + np.pi)
    sign = np.sign(a)
    return sign * (a % (2 * np.pi))
