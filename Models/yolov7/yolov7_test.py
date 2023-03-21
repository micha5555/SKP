from model_yolov7 import detect_license_plate_yolov7

if __name__ == '__main__':
    results_file = "../tests_results.txt"
    video_path = '../Videos/short.mp4'

    detect_license_plate_yolov7(video_path, results_file)