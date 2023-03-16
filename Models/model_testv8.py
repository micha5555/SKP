import cv2
import pytesseract
import torch
import ultralytics


def detect_license_plate():
    # Load YOLOv5 model from checkpoint file
    #model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    model = ultralytics.YOLO('best_yolov8.pt')

    # Set up video capture from default camera
    cap = cv2.VideoCapture(0)
    model.overrides['conf'] = 0.25  # NMS confidence threshold
    model.overrides['iou'] = 0.45  # NMS IoU threshold

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Detect license plates in the fra to me using YOLOv5
        results = model.predict(frame)
        


        # Draw bounding boxes around license plates
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1 = int(x1)
            x2 = int(x2)
            y1 = int(y1)
            y2 = int(y2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Extract license plate image and apply OCR
            license_plate_image = frame[y1:y2, x1:x2]
            license_plate_text = pytesseract.image_to_string(license_plate_image, config='--psm 11')

            # Draw license plate text on image
            cv2.putText(frame, license_plate_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        # Display the resulting frame
        cv2.imshow('License Plate Detector', frame)

        # Exit on 'q' keypress
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to run the license plate detection on start-up
if __name__ == '__main__':
    detect_license_plate()