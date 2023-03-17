import matplotlib.pyplot as plt
import torch
import cv2
from torchvision import transforms
import numpy as np
from utils.datasets import letterbox
from utils.general import non_max_suppression_kpt
from utils.plots import output_to_keypoint, plot_skeleton_kpts
import pytesseract


def detect_license_plate():
    # ladowanie modelu xd
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    weigths = torch.load('best_yolov7.pt', map_location=device)
    model = weigths['model']
    _ = model.float().eval()

    if torch.cuda.is_available():
        model.half().to(device)

    # poka sowe xd
    cap = cv2.VideoCapture('video.mp4')

    while True:
        ret, frame = cap.read()
        frame = letterbox(frame, 960, stride=64, auto=True)[0]
        frame = transforms.ToTensor()(frame)
        frame = torch.tensor(np.array([frame.numpy()]))

        if torch.cuda.is_available():
            frame = frame.half().to(device)   
        results, _ = model(frame)  
        license_plate_boxes = results[0][results[0][:, -1] == 0][:, :4]

        for box in license_plate_boxes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Extract license plate image and apply OCR
            license_plate_image = frame[y1:y2, x1:x2]
            license_plate_text = pytesseract.image_to_string(license_plate_image, config='--psm 11')
            print(license_plate_text)

            # Draw license plate text on image
            cv2.putText(frame, license_plate_text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        cv2.imshow('License Plate Detector', frame.numpy())


    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_license_plate()
