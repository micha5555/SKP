import cv2
import pytesseract
import torch
import time

def detect_license_plate():
    # Load YOLOv5 model from checkpoint file
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='best_yolov5.pt', force_reload=True)

    # Set up video capture from default camera
    cap = cv2.VideoCapture(0)

    # Initialize FPS variables
    fps_start_time = 0
    fps_counter = 0

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

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

        # Display the resulting frame
        cv2.imshow('License Plate Detector', frame)

        # Calculate FPS
        fps_counter += 1
        if (time.time() - fps_start_time) > 1:
            fps = fps_counter / (time.time() - fps_start_time)
            print(f"FPS: {round(fps,2)}")
            fps_start_time = time.time()
            fps_counter = 0

        # Exit on 'q' keypress
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to run the license plate detection on start-up
if __name__ == '__main__':
    detect_license_plate()
