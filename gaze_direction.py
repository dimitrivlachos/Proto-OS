import cv2
import numpy as np
from picamera2 import Picamera2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
#img = cv2.imread('test2.jpg')

detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

#threshold = 50

def main():
    cap = picam2.capture_array()
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, lambda x: None)

    while True:
        frame = cap.read()
        face_frame = detect_faces(frame, face_cascade)
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    #threshold = cv2.getTrackbarPos('threshold', 'image')
                    eye = cut_eyebrows(eye)
                    iris_center = detect_iris_center(eye, threshold, detector)
                    if iris_center is not None:
                        gaze_direction = calculate_gaze_direction(eye, iris_center)
                        print(gaze_direction)
                        #save_to_csv(gaze_direction)
                        eye_with_markers = draw_markers(eye, iris_center, gaze_direction)
                        cv2.imshow('eye_with_markers', eye_with_markers)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_faces(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = classifier.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = np.array([coords[0]], np.int32)
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y+h, x:x+w]
    return frame

def detect_eyes(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = classifier.detectMultiScale(gray_frame, 1.3, 5)
    width = np.size(img, 1)
    height = np.size(img, 0)
    left_eye = None
    right_eye = None
    for (x,y,w,h) in eyes:
        if y+h > height/2:
            pass
        eye_center = x + w / 2
        if eye_center < width * 0.5:
            left_eye = img[y:y+h, x:x+w]
        else:
            right_eye = img[y:y+h, x:x+w]
    return left_eye, right_eye

def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]
    return img

def detect_iris_center(eye, threshold, detector):
    _, eye_binary = cv2.threshold(eye, threshold, 255, cv2.THRESH_BINARY)
    eye_binary = cv2.erode(eye_binary, None, iterations=2)
    eye_binary = cv2.dilate(eye_binary, None, iterations=4)
    eye_binary = cv2.medianBlur(eye_binary, 5)
    keypoints = detector.detect(eye_binary)
    if keypoints:
        iris_center = keypoints[0].pt
        return iris_center
    else:
        return None

def calculate_gaze_direction(eye, iris_center):
    eye_width = eye.shape[1]
    eye_height = eye.shape[0]
    eye_center_x = eye_width / 2
    eye_center_y = eye_height / 2
    horizontal_displacement = (iris_center[0] - eye_center_x) / eye_center_x
    vertical_displacement = (iris_center[1] - eye_center_y) / eye_center_y
    gaze_direction = (horizontal_displacement, vertical_displacement)
    return gaze_direction

def draw_markers(eye, iris_center, gaze_direction):
    eye_with_markers = eye.copy()
    eye_width = eye.shape[1]
    eye_height = eye.shape[0]
    iris_center_x = int(iris_center[0])
    iris_center_y = int(iris_center[1])
    marker_color = (0, 255, 0)  # Green color for markers

    # Draw iris center
    cv2.circle(eye_with_markers, (iris_center_x, iris_center_y), 2, marker_color, 2)

    # Calculate gaze direction end point
    gaze_end_x = int(eye_width / 2 + gaze_direction[0] * eye_width / 4)
    gaze_end_y = int(eye_height / 2 + gaze_direction[1] * eye_height / 4)

    # Draw gaze direction line
    cv2.line(eye_with_markers, (int(eye_width / 2), int(eye_height / 2)), (gaze_end_x, gaze_end_y), marker_color, 2)

    return eye_with_markers

def save_to_csv(gaze_direction):
    with open('gaze_direction.csv', 'a') as f:
        f.write('{},{}\n'.format(gaze_direction[0], gaze_direction[1]))

if __name__ == '__main__':
    main()
