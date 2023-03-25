import torch
import numpy as np
import cv2
import time
import pytesseract
from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectDetection:
    """
    Class implements Yolo5 model to make inferences on a youtube video using OpenCV.
    """
    
    def __init__(self):
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # self.device = 'cpu'
        print("\n\nDevice Used:",self.device)

    def load_model(self):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='best_yolov5.pt', force_reload=True)
        return model

    def score_frame(self, frame):
        self.model.to(self.device)
        downscale_factor = 1
        self.width = int(frame.shape[1] / downscale_factor)
        self.height = int(frame.shape[0] / downscale_factor)
        frame = cv2.resize(frame, (self.width, self.height))
        
        results = self.model(frame)
     
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

        return labels, cord

    def class_to_label(self, x):
        return self.classes[int(x)]

    def validate_plate(self, plate_width, plate_height):

        if plate_width / plate_height < 2:
            return False
            
        return True

    def detect_boxes(self, results, frame, confidence):
        labels, cord = results
        detections = []
        n = len(labels)
        # print(f"Labels={labels}, n={len(labels)}")
        x_shape, y_shape = self.width, self.height

        for i in range(n):
            row = cord[i]

            if row[4] >= confidence:
                x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
                if self.validate_plate(x2-x1, y2-y1):
                    if self.class_to_label(labels[i]) == 'License_Plate':
                        confidence = float(row[4].item())
                        confidence = round(confidence, 3)*100

                        cv2.putText(img, f'Live conf:', (20,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                        cv2.putText(img, f'{confidence}%', (20,180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                        # print(f"Confidence={confidence}%")

                        detections.append(([x1, y1, int(x2-x1), int(y2-y1)], row[4].item(), "License_Plate"))

        return frame, detections



# cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture("nagranie_test2.mp4")
# cap = cv2.VideoCapture("nagranie_test1.mp4")

detector = ObjectDetection()

# object_tracker = DeepSort(max_age=5,
#                           n_init=3,
#                           nms_max_overlap=1.0,
#                           max_cosine_distance=0.3,
#                           nn_budget=None,
#                           override_track_class=None)
object_tracker = DeepSort(max_age=5,
                          n_init=3)

license_plates = dict()
counter = 0

# dla n=1 jest slowmotion, ale łapiemy wszystkie tablice
# dla n>=2 jest szybciej, ale pomija tablice
detect_every_n_frame = 1

while cap.isOpened():
    success, img = cap.read()

    counter += 1
    if (counter % detect_every_n_frame != 0):
        continue

    start_time = time.perf_counter()

    results = detector.score_frame(img)
    img, detections = detector.detect_boxes(results, img, confidence=0.8)
    
    tracks = object_tracker.update_tracks(detections, frame=img)
    
    
    for track in tracks:
        if not track.is_confirmed():
            continue
        track_id = track.track_id
        ltrb = track.to_ltrb()
        bbox = ltrb

        if not str(track_id) in license_plates:
            license_plate_image = img[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

            license_plate_text = pytesseract.image_to_string(license_plate_image, config='--psm 11')
            license_plates[str(track_id)] = license_plate_text.replace("\n", "")
            
            # print(license_plates)
        
        if (license_plate_image is not None):
            x_offset=250
            y_offset=10
            img[y_offset:y_offset+license_plate_image.shape[0], x_offset:x_offset+license_plate_image.shape[1]] = license_plate_image

        cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0,0,255), 2)
        cv2.putText(img, f"ID: {str(track_id)} - {license_plates[str(track_id)]}", (int(bbox[0]), int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    end_time = time.perf_counter()
    totalTime = end_time - start_time
    fps = 1 / totalTime
    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
    cv2.imshow("img", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()