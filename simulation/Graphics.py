'''

'''
import pygame
import math
from utils.geometry import m_to_pixel

class Graphics:
    def __init__(self, dimensions, circle, robot_img_path, robot_dims):
        pygame.init()

        # COLORS
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.red = (255, 0, 0)

        self.circle = circle
        robot = pygame.image.load(robot_img_path)

        robot_dims = (robot_dims[0] * m_to_pixel, robot_dims[1] * m_to_pixel) # Convert meters to pixels
        robot = pygame.transform.scale(robot, robot_dims)
        self.robot = pygame.transform.rotate(robot, 180)
        # Truck currently going the wrong way

        # ------ MAP ------
        # Dimensions
        self.height, self.width = dimensions

        # Window Settings
        pygame.display.set_caption("Robot Simulation") # Prolly change this later
        self.map = pygame.display.set_mode((self.width, self.height))

    # Recieves pixel coordinates and angle in degrees of the robot and draws the robot.
    def draw_robot(self, x, y, heading):
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(heading), 1)
        rect = rotated.get_rect(center=(x, y))
        # draw
        self.map.blit(rotated, rect)
        pygame.draw.circle(self.map, self.red, (x, y), 5, 0)

    # Draws the map. Should be called before drawing anything else
    def draw_map(self):
        self.map.fill(self.white)
        self.draw_circle()

    def draw_circle(self):
        pygame.draw.circle(self.map, self.black, (self.circle.cX, self.circle.cY), self.circle.r * m_to_pixel, 5)

    # At each point, draw a circle
    # Maybe path fade? (only draw last couple of points)
    def draw_path(self):
        path = []
        return path