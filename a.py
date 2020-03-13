import cv2
import numpy as np

img = cv2.imread("smoke.png", cv2.IMREAD_UNCHANGED)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

coords = cv2.findNonZero(gray) # Find all non-zero points (text)
x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box

rect = img[y:y+h, x:x+w]
cv2.imwrite("smoke2.png",rect)