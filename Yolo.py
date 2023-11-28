from ultralytics import YOLO
import cv2 as cv
from picamera2 import Picamera2
import numpy as np
from time import sleep, time
import _thread


class Yolo:
    target_found = False
    bounding_box = None
    cam = Picamera2()
    IMAGE_SIZE = [640, 480] # width, height

    def __init__(self):
        # YOLO stuff
        self.model = YOLO('yolov8n.pt')
        self.cam.start()

    # In our program, the use of this is just to tell if we found a person and to get that persons bounding box
    def predict(self, img):
        ''' Takes one iterative step in the YOLO algorithm
        
            -> pos(tuple): position of target, found_target(boolean): whether the target has been observed
        '''
        temp_found_person = False
        b = None

        # Prediction
        results = self.model.predict(img)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                c = box.cls
                if self.model.names[int(c)] == "person":
                    if not temp_found_person:
                        temp_found_person = True
                    b = box.xyxy[0]
                    break
        if not temp_found_person:
            self.bounding_box = None
        self.target_found = temp_found_person
        return b


    def camshift(self):
        frame = np.ascontiguousarray(self.cam.capture_array()[:, :, 0:3])
        b = self.predict(frame) # predict can take an ndarray
        if b == None:
            print("YOLO could not find a person")
            return 0
        # set up bounding box
        x1, y1 = int(b[0]), int(b[1])
        x2, y2 = int(b[2]), int(b[3])
        w = abs(x1 - x2)
        h = abs(y1 - y2)
        track_window = (x1, y1, w, h)
        roi = frame[y1:y1+h, x1:x1+w]
        hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)
        # Setup the termination criteria, either 10 iteration or move by at least 1 pt
        term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

        runtime = 0 # in seconds
        start = time()
        while runtime < 50:
            frame = np.ascontiguousarray(self.cam.capture_array()[:, :, 0:3])
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)
            # apply camshift to get the new location
            ret, track_window = cv.CamShift(dst, track_window, term_crit)
            pts = cv.boxPoints(ret) 
            pts = np.int0(pts) # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            self.bounding_box = pts
            img2 = cv.polylines(frame,[pts],True, 255,2)
            cv.imshow('img2',img2)
            sleep(.1)
            end = time()
            runtime = end - start
        self.bounding_box = None


if __name__ == "__main__":
    yolo = Yolo()
    _thread.start_new_thread(yolo.camshift())
    while(True):
        print(yolo.bounding_box)

    