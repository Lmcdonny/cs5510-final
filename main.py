from robot.Follow_Bot import Follow_Bot
from Controller import Controller
from sensors.Ultrasonic import Ultrasonic
from sensors.Camera import Camera
from sensors.Car_Camera import Car_Camera
from Yolo import Yolo

def main():
    # Robot dimensions in meters [W, L]
    robot_dims = [22 / 100, 16 / 100]

    # Robot
    robot = Follow_Bot(robot_dims[1])

    # Ultrasonic
    u_sens = Ultrasonic()

    # YOLO
    camera = Car_Camera()
    yolo_sens = Yolo(camera)
    # usage: yolo_sens.predict(image)

    # Controller
    controller = Controller(yolo_sens, u_sens, robot)
    controller.run()

if __name__ == '__main__':
    main()