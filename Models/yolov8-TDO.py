import asone
from asone import ASOne

# Instantiate Asone object
detect = ASOne(tracker=asone.BYTETRACK, detector=asone.YOLOV8S_PYTORCH, weights='./best_yolov8.pt', recognizer=asone.EASYOCR, use_cuda=False) #set use_cuda=False to use cpu

filter_classes = None # set to None to track all classes

# ##############################################
#           To track using video file
# ##############################################
# Get tracking function
track = detect.track_video('video.mp4', output_dir='data/results', save_result=False, display=True, filter_classes=filter_classes)

# Loop over track to retrieve outputs of each frame 
for bbox_details, frame_details in track:
    bbox_xyxy, ids, scores, class_ids = bbox_details
    frame, frame_num, fps = frame_details
    # Do anything with bboxes here
    for boxik in bbox_xyxy:
        x1,y1,x2,y2 = boxik
        license_plate_image = frame[int(y1):int(y2), int(x1):int(x2)]
        results = detect.detect_text(license_plate_image) 
        # img = utils.draw_text(img, results)

# ##############################################
#           To track using webcam
# ##############################################
# Get tracking function
track = detect.track_webcam(cam_id=0, output_dir='data/results', save_result=True, display=True, filter_classes=filter_classes)

# Loop over track to retrieve outputs of each frame 
for bbox_details, frame_details in track:
    bbox_xyxy, ids, scores, class_ids = bbox_details
    frame, frame_num, fps = frame_details
    # Do anything with bboxes here
