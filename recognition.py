from ultralytics import YOLO
import cv2
import math 
import os
# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
#model = YOLO("yolo-Weights/yolov8n.pt")
print(os.getcwd())
model = YOLO(os.getcwd()+"\Trained_Model_Steroided.pt")


# object classes
classNames = ['Short Sleeve', 'long sleeve top', 'short sleeve outwear', 'long sleeve outwear', 'vest', 'sling', 'shorts','trousers','skirt','short sleeve dress','long sleeve dress','vest dress','sling dress']

topsNames = ['Short Sleeve', 'long sleeve top', 'short sleeve outwear', 'long sleeve outwear', 'vest']
bottomNames = ['shorts','trousers','skirt']

tops = []
bottoms = []

def storeCloth(img,box,x1, y1, x2, y2):   
    results = model(img, stream=True)
    cls = int(box.cls[0])
    
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    # Get the color of the pixel at the center of the bounding box
    color = img[center_y, center_x]  # Returns the BGR value (Blue, Green, Red)

    # Convert the color to RGB if needed
    color_rgb = color[::-1]

    if (classNames[cls] in topsNames):
        tops.append([f"{color_rgb} {classNames[cls]}"])
    elif(classNames[cls] in bottomNames):
        bottoms.append([f"{color_rgb} {classNames[cls]}"])



while True:
    success, img = cap.read()
    results = model(img, stream=True)



    # coordinates
    if len(tops) > 0:
        print(tops)
        break
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            #storeCloth(img,box,x1, y1, x2, y2)

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Get the color of the pixel at the center of the bounding box
            color = img[center_y, center_x]  # Returns the BGR value (Blue, Green, Red)

            # Convert the color to RGB if needed
            color_rgb = color[::-1]

            print("Colour--> ", color_rgb)

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)



    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()