# FollowBot


### Goal
Our goal is to have our robot detect and follow a human subject using image recoginsion techniques and the robots' ultrasonic sensors.

### Our Approach
Our plan is to use OpenCV's CAMShift functionality combined with Ultralytics 
YOLO in order to identify our subject.

1) Set up pretrained YOLO model
2) Use YOLOv8 to identify a valid human subject and obtain our initial bounding box
3) Use CAMShift to track the bounding box
4) Periodically update bounding box with Yolo

The reason for this approach is that YOLO can take a up to 3 seconds to run on the Raspberry Pi 3 whereas CAMShift can be run with much lower latency. A drawback of CAMShift is that it cannot tell when it has lost its target (the bounding box just find a new target to follow), so we have to periodically run Yolo again to detect if there is still a valid human target in frame.


## Setup
This program is tested on a Yahboom Raspbot with a Raspberry Pi 3 using Debian GNU/Linux 11 (bullseye).
To run this program you will need to install on your Yahboom Raspbot:
* [Ultralytics] (https://docs.ultralytics.com/)
* [smbus]
* [picamera2] (https://github.com/raspberrypi/picamera2)
* [OpenCV] (https://pypi.org/project/opencv-python/)
* [Torch]

## Usage
1) Place your Raspbot 6 feet away from you
2) Run the `main.py` script
3) Wait for the camera to boot up and for Yolo to run its initial prediction. This can take up to 15 seconds.
4) Once the robot finds a valid subject it will beep once and start following.
5) If the robot loses its subject it will beep and stop moving. The robot will attempt to run Yolo predictions until it finds a target again.
