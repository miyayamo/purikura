import cv2

frame = cv2.imread("out.png", -1)
cv2.imshow("webcam", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
