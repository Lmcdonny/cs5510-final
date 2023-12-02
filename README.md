

### Our Approach
Our plan is to use OpenCV's CAMShift functionality combined with Ultralytics 
YOLO in order to identify our subject.

1) Set up pretrained YOLO model
2) Use YOLOv8 to identify a valid human subject and obtain our initial bounding box
3) Use CAMShift to track the bounding box


## Setup
To run this program you will need to install on your Yahboom Raspbot:
* Ultralytics [https://docs.ultralytics.com/]
* smbus
* picamera2
* OpenCV [https://pypi.org/project/opencv-python/]
