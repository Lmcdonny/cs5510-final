from ultralytics import YOLO
import cv2
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated
from time import sleep
from picamera2 import Picamera2
import numpy as np

model = YOLO('yolov8n.pt')
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
cam = Picamera2()
cam.start()

while True:
    # _, img = cap.read()
    img = np.ascontiguousarray(cam.capture_array()[:, :, 0:3])    
    print(img.shape)
    # BGR to RGB conversion is performed under the hood
    # see: https://github.com/ultralytics/ultralytics/issues/2575
    results = model.predict(img)
    print(results)
    sleep(1)

cap.release()
cv2.destroyAllWindows()
