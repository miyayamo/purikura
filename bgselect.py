import cv2, sys, datetime, msvcrt, time, pygame, threading, numpy as np

gbimg = cv2.imread("gb.png")
cv2.imshow("webcam", gbimg)
cv2.waitKey(60)

cv2.destroyAllWindows()
