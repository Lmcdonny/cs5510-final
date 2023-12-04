from robot.Follow_Bot import Follow_Bot
from Controller import Controller
from sensors.Ultrasonic import Ultrasonic
from sensors.Camera import Camera
from sensors.Car_Camera import Car_Camera
from Yolo import Yolo

def main():
    # [W, H]
    cam_dims = [640, 480]
    # Robot dimensions in meters [W, L]
    robot_dims = [22 / 100, 16 / 100]

    # Robot
    robot = Follow_Bot(robot_dims[1])

    # Ultrasonic
    u_sens = Ultrasonic()

    # Camera
    camera = Car_Camera()
    
    # YOLO
    yolo_sens = Yolo(camera)
    # usage: yolo_sens.predict(image)

    # Controller
    controller = Controller(yolo_sens, u_sens, robot)
    controller.run()

if __name__ == '__main__':
    main()