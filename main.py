from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

found_person = False

width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float `width`
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`

print(width, ", ", height)

while True:
    _, img = cap.read()
    temp_found_person = False

    results = model.predict(img)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            c = box.cls
            if model.names[int(c)] == "person":
                if not temp_found_person:
                    temp_found_person = True
                b = box.xyxy[0]
    if found_person and not temp_found_person:
        # cant find person
        # beep beep
        # stop moving
        # yolo loop til someones found
        found_person = False
        print("Lost Person")
    elif not found_person and temp_found_person:
        # beeeep found a new target
        found_person = True
        print("Found Person")

    # if we have a bounding box
    #   see where bounding box is compared to screen center
    #   if bb is left
    #       turn left
    #   elif bb is right
    #       turn right
    # ultrasonic test for distance
    # if > 6 ft
    #   move forward
           
    if cv2.waitKey(1) & 0xFF == ord(' '):
        break

cap.release()
cv2.destroyAllWindows()
