from robot.Follow_Bot import Follow_Bot
from Controller import Controller
from sensors.Ultrasonic import Ultrasonic
from sensors.Camera import Camera
from Yolo import Yolo

def main():
    # [W, H]
    cam_dims = [640, 480]

    # Robot
    robot = Follow_Bot((2,2), 4, 2)

    # Ultrasonic
    u_sens = Ultrasonic()

    # Camera
    camera = Camera()
    
    # YOLO
    yolo_sens = Yolo(camera)
    # usage: yolo_sens.predict(image)

    # Controller
    controller = Controller(camera, yolo_sens, u_sens, robot)
    controller.run()

if __name__ == '__main__':
    main()