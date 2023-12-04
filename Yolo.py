from ultralytics import YOLO
import cv2 as cv
import numpy as np
from time import sleep, time
from threading import Thread


class Yolo:
    running = False
    target_found = False
    yolo_box = None
    bounding_box = None

    def __init__(self, cam):
        '''
        Cam must implement the following methods:

        start(), capture_array(), 
        '''
        self.cam = cam
        self.model = YOLO('yolov8n.pt')
        self.cam.start()

    # In our program, the use of this is just to tell if we found a person and to get that persons bounding box
    def predict(self):
        ''' Takes one iterative step in the YOLO algorithm
        
            -> pos(tuple): position of target, found_target(boolean): whether the target has been observed
        '''
        temp_found_person = False
        b = None
        img = self.cam.capture_array()

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
        self.target_found = temp_found_person
        self.yolo_box = b


    def camshift(self):
        self.running = True
        while self.running:
            frame = np.ascontiguousarray(self.cam.capture_array())
            while self.yolo_box is None:
                print("Yolo.py: YOLO could not find a person")
                print("Yolo.py: Running YOLO")
                self.predict()
                print("Yolo.py: YOLO'd")
                sleep(1)
            # set up bounding box
            b = self.yolo_box
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

            while self.running:
                if b is not self.yolo_box: # restart the function
                    break
                frame = np.ascontiguousarray(self.cam.capture_array())
                hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                dst = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)
                # apply camshift to get the new location
                ret, track_window = cv.CamShift(dst, track_window, term_crit)
                pts = cv.boxPoints(ret)
                pts = np.intp(pts) # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                self.bounding_box = pts
                # sleep(.1)

    def print(self, message):
        print("Yolo.py: " + message)

    def close(self):
        self.cam.close()

if __name__ == "__main__":
    yolo = Yolo()
    yolo.predict(np.ascontiguousarray(yolo.cam.capture_array()))
    print("Running YOLO")
    t = Thread(target=yolo.camshift, args=[])
    t.start()
    runtime = 0 # in seconds
    start = time()
    while(True):
        # if not yolo.bounding_box is None:
        print(yolo.bounding_box)
        current = time()
        runtime = current - start
        if runtime > 10:
            print("Running YOLO")
            yolo.predict(np.ascontiguousarray(yolo.cam.capture_array()))
            print("YOLO'd")
            start = time() # reset timer
