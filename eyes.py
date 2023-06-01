# Description: This program detects the eyes of a person using the webcam and
#              then detects the iris of the eyes using blob detection.
# https://medium.com/@stepanfilonov/tracking-your-eyes-with-python-3952e66194a6
# https://github.com/stepacool/

import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
img = cv2.imread('test2.jpg')

detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)

#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
#_, img = cv2.threshold(gray, 42, 255, cv2.THRESH_BINARY)

#cv2.imshow('my image',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, lambda x: None)

    while True:
        _, frame = cap.read()
        face_frame = detect_faces(frame, face_cascade)
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            irises = []
            for eye in eyes:
                if eye is not None:
                    threshold = cv2.getTrackbarPos('threshold', 'image')
                    eye = cut_eyebrows(eye)
                    iris = blob_process(eye, threshold, detector)
                    eye = cv2.drawKeypoints(eye, iris, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                    gaze_direction = calculate_gaze_direction(eyes)
                    print("Gaze Direction:", gaze_direction)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detect_faces(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    coords = classifier.detectMultiScale(gray_frame, 1.3, 5) # detect faces
    if len(coords) > 1: # if number of faces greater than 1
        biggest = (0, 0, 0, 0)
        for i in coords: # extract the biggest face
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1: # if one face detected, convert it from tuple to numpy array
        biggest = np.array([coords[0]], np.int32)
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y+h, x:x+w]
    return frame

def detect_eyes(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to grayscale
    eyes = classifier.detectMultiScale(gray_frame, 1.3, 5) # detect eyes
    width = np.size(img, 1) # get face frame width
    height = np.size(img, 0) # get face frame height
    left_eye = None
    right_eye = None
    for (x,y,w,h) in eyes:
        if y+h > height/2: # pass if the eye is at the bottom half of the face
            pass
        
        eye_center = x + w / 2 # get the eye center
        if eye_center < width * 0.5:
            left_eye = img[y:y+h, x:x+w]
        else:
            right_eye = img[y:y+h, x:x+w]

    return left_eye, right_eye

def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width] # cut eyebrows out (15 px)
    return img

def blob_process(img, threshold, detector):
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2) # erode away boundaries
    img = cv2.dilate(img, None, iterations=4) # dilate to merge adjacent blobs
    img = cv2.medianBlur(img, 5) # blur to smooth out blob irregularities
    keypoints = detector.detect(img) # detect blobs
    return keypoints

def calculate_gaze_direction(eyes):
    if eyes[0] is not None and eyes[1] is not None:
        left_eye_center_x = eyes[0][0] + eyes[0][2] / 2
        right_eye_center_x = eyes[1][0] + eyes[1][2] / 2
        average_eye_center_x = (left_eye_center_x + right_eye_center_x) / 2
        face_width = eyes[0][2] + eyes[1][2]
        horizontal_displacement = (average_eye_center_x - face_width / 2) / (face_width / 2)
    elif eyes[0] is not None:
        eye_center_x = eyes[0][0] + eyes[0][2] / 2
        face_width = eyes[0][2]
        horizontal_displacement = (eye_center_x - face_width / 2) / (face_width / 2)
    else:
        return 0.0

    gaze_direction = horizontal_displacement
    return gaze_direction


if __name__ == '__main__':
    main()