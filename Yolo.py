from ultralytics import YOLO

class Yolo:
    def __init__(self):
        # YOLO stuff
        self.model = YOLO('yolov8n.pt')

    def predict(self, img):
        ''' Takes one iterative step in the YOLO algorithm
        
            -> pos(tuple): position of target, found_target(boolean): whether the target has been observed
        '''
        temp_found_person = False

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

        # if we have a bounding box
        #   see where bounding box is compared to screen center
        #   if bb is left
        #       turn left
        #   elif bb is right
        #       turn right
        # ultrasonic test for distance
        # if > 6 ft
        #   move forward