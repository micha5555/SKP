import cv2
import pytesseract
import torch
import ultralytics
import time

def detect_license_plate_yolov8(video_path, results_file):
    # Load YOLOv5 model from checkpoint file
    #model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
    model = ultralytics.YOLO('best_yolov8.pt')

    # Set up video capture from default camera
    cap = cv2.VideoCapture(video_path)
    model.overrides['conf'] = 0.25  # NMS confidence threshold
    model.overrides['iou'] = 0.45  # NMS IoU threshold

    # Initialize FPS variables
    fps_start_time = 0
    fps_counter = 0
    fps_avg = []

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
        # End of video file
            break

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

         # Calculate FPS
        fps_counter += 1
        if (time.time() - fps_start_time) > 1:
            fps = fps_counter / (time.time() - fps_start_time)
            fps_avg.append(fps)
            print(f"FPS: {round(fps,2)}")
            fps_start_time = time.time()
            fps_counter = 0

        # Exit on 'q' keypress
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and close window
    cap.release()
    cv2.destroyAllWindows()

    # Calculate the average of the numbers
    average = sum(fps_avg) / len(fps_avg)
    file  = open(results_file, "a")
    file.write("Yolov8 average FPS: " + str(average) + '\n')
    file.close()

# Call the function to run the license plate detection on start-up
if __name__ == '__main__':
    results = "tests_results.txt"
    video = '/home/nebraszka/Downloads/VID_20230313_143216.mp4'
    detect_license_plate_yolov8(results_file=results, video_path=video)