from picamera2 import Picamera2
import time
import cv2

class Car_Camera:
    cam = Picamera2()

    def start(self):
        self.cam.start()

    def capture_array(self):
        return self.cam.capture_array()[:, :, 0:3]
    
    def close(self):
        pass

if __name__ == '__main__':
    picam2 = Picamera2()
    picam2.start()
    
    array = picam2.capture_array()

    cv2.imshow('Image', array)
    cv2.waitKey(0)

    
