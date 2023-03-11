import cv2
import pytesseract
import torch
from PIL import Image
from numpy import asarray

def detect_license_plate():
    # Load YOLOv5 model from checkpoint file
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

    license_plate_image_jpg = Image.open("tablica.jpg")
    frame = asarray(license_plate_image_jpg)
    # Detect license plates in the frame using YOLOv5
    results = model(frame)

    # Extract bounding boxes for license plates
    license_plate_boxes = results.pred[0][results.pred[0][:, -1] == 0][:, :4]

    # Draw bounding boxes around license plates
    for box in license_plate_boxes:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Extract license plate image and apply OCR
        license_plate_image = frame[y1:y2, x1:x2]
        license_plate_text = pytesseract.image_to_string(license_plate_image, config='--psm 11')
        print(license_plate_text)

        # Draw license plate text on image
        cv2.putText(frame, license_plate_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


# Call the function to run the license plate detection on start-up
if __name__ == '__main__':
    detect_license_plate()
