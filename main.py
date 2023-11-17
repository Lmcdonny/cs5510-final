from robot.Follow_Bot import Follow_Bot
from Controller import Controller
from sensors.Ultrasonic import Ultrasonic
from sensors.Camera import Camera
from Yolo import Yolo

def main():

    # Robot
    robot = Follow_Bot(ROBOT_DIMS[0], 2)

    # Ultrasonic
    u_sens = Ultrasonic()

    # Camera
    camera = Camera()
    
    # YOLO
    yolo_sens = Yolo()

    # Controller
    controller = Controller(camera, yolo_sens, u_sens, robot)
    controller.run()

if __name__ == '__main__':
    main()