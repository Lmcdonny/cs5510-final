'''

'''
import pygame
import os
from utils.geometry import m_to_pixel

class Simulation:
    def __init__(self, name, gfx, robot, circle):
        self.name = name
        self.gfx = gfx
        self.robot = robot
        self.circle = circle

        self.rob_log = []
        self.time = 0
        self.data_path = 'data/'

    def run(self):
        dt = 0
        curr_hz = 0
        last_time = pygame.time.get_ticks()
        running = True
        # Simulation loop
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.save()

            # Time
            dt = (pygame.time.get_ticks() - last_time) / 1000
            self.time += dt
            curr_hz += dt
            last_time = pygame.time.get_ticks()

            # Physics
            self.robot.kinematics(dt)

            # Draw
            self.gfx.draw_map()
            self.gfx.draw_robot(self.robot.x, self.robot.y, self.robot.heading)

            # Robot control
            if curr_hz >= 1 / self.robot.hz:
                # print(f'Curr_hz: {curr_hz}')
                curr_hz = 0
                self.robot.operate(self.circle.get_pos(), self.circle.r * m_to_pixel)

            # Data Recording
            self.log()

            pygame.display.update()

    def get_stats(self):
        # x, y, angle, vl, vr, timestamp
        return f'{self.robot.x},{self.robot.y},{self.robot.heading},{self.robot.get_v(0)},{self.robot.get_v(1)},{self.time}'
        
    def log(self):
        self.rob_log.append(self.get_stats())

    def save(self):
        try:
            # Check if the directory already exists
            if not os.path.exists(self.data_path):
                # If not, create the directory
                os.makedirs(self.data_path)
                print(f"Directory '{self.data_path}' created successfully.")
            else:
                # print(f"Directory '{self.data_path}' already exists.")
                pass
        except Exception as e:
            print(f"Error: {e}")
        try:
            file_path = self.data_path + self.name + '.blt'
            with open(file_path, 'w') as file:
                file.write('x,y,heading,vl,vr,timestamp\n')
                for string in self.rob_log:
                    file.write(string + '\n')
            print(f"Successfully wrote {len(self.rob_log)} lines to {file_path}")
        except Exception as e:
            print(f"Error: {e}")
