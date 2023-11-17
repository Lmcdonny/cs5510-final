import picamera
import cv2
import numpy as np

VIDEO_NAME = 'my_video.h264'

##### Camera Setup #####
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 60

output = np.empty((240, 320, 3), dtype=np.uint8)
camera.capture(output, 'rgb')

cv2.imshow('Image', output)
cv2.waitKey(0)