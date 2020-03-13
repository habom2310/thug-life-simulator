import numpy as np
import cv2
import os
import utils

class Thug:
    def __init__(self):
        glass_img_path = os.getcwd() + "/glass2.png"
        smoke_img_path = os.getcwd() + "/smoke2.png"
        self.glass_img = cv2.imread(glass_img_path, cv2.IMREAD_UNCHANGED)
        self.smoke_img = cv2.imread(smoke_img_path, cv2.IMREAD_UNCHANGED)
    
    def rotate_and_scale(self):
        pass

    
from face_detection import Face_detection
from face_landmark import Face_landmark
if __name__ == "__main__":
    th = Thug()
    img = cv2.imread("face.jpg")
    fd = Face_detection()
    fl = Face_landmark()

    rects = fd.detect(img)

    if len(rects) == 0:
        print("no face detected")
    
    else:
        rect = rects[0]
        rect = utils.read_dlib_rect(rect)

        face = img[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
        shape = fl.facial_landmark(face)

        glass_width = int(1.3 * (shape[0][0] - shape[2][0]))
        print(glass_width)
        glass_height = th.glass_img.shape[0] * int(glass_width/th.glass_img.shape[1])
        print(glass_height)

        th.glass_img = cv2.resize(th.glass_img,(glass_width,glass_height))

        img = utils.overlay_transparent(img, th.glass_img, rect[0] + shape[2][0] - int(glass_width * 0.125), rect[1] + shape[2][1]-int(glass_height/2))

        x_mouth = rect[0] + shape[4][0] - th.smoke_img.shape[1]
        y_mouth = rect[1] + int(shape[4][1] + (shape[4][1] - (shape[0][1] + shape[2][1])/2) / 2)

        print(x_mouth, y_mouth)

        # th.smoke_img = cv2.resize(th.smoke_img,(int(glass_width/2),int(glass_width/2)))

        img = utils.overlay_transparent(img, th.smoke_img, x_mouth, y_mouth)

        for (x, y) in shape:
            print(x,y)
            cv2.circle(face, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("face", face)
        cv2.imshow("img", img)

        cv2.waitKey()

        