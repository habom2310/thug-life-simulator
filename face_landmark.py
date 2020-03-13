import numpy as np
import cv2
import dlib
import os
import utils

class Face_landmark:
    def __init__(self):
        model_path = os.getcwd() + "/shape_predictor_5_face_landmarks.dat"
        self.predictor = dlib.shape_predictor(model_path)

    def facial_landmark(self, face):
        h, w, c = face.shape
        shape = self.predictor(face, dlib.rectangle(0, 0, w, h))

        shape = utils.read_dlib_shape(shape)
        return np.array(shape)

    
from face_detection import Face_detection
if __name__ == "__main__":
    fd = Face_detection()
    fl = Face_landmark()

    img = cv2.imread("face.jpg")
    # img = cv2.imread("flower.jpg")

    rects = fd.detect(img)

    if len(rects) == 0:
        print("no face detected")
    
    else:
        rect = rects[0]
        rect = utils.read_dlib_rect(rect)

        face = img[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
        shape = fl.facial_landmark(face)

        for (x, y) in shape:
            cv2.circle(face, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("face", face)
        cv2.waitKey()
