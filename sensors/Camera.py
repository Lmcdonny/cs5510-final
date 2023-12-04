import cv2

class Camera:
    def __init__(self, mode=0):
        self.cap = cv2.VideoCapture(mode)
        self.cap.set(3, 640)
        self.cap.set(4, 480)

        width  = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

        print(width, ", ", height)

    def get_im(self):
        _, img = self.cap.read()
        return img

    def close(self):
        self.cap.release()