from model_yolov5 import detect_license_plate_yolov5
from model_yolov8 import detect_license_plate_yolov8

if __name__ == '__main__':
    results_file = "tests_results.txt"
    video_path = '../Videos/short.mp4'

    detect_license_plate_yolov5(video_path, results_file, 10)
    detect_license_plate_yolov8(video_path, results_file, 10)
