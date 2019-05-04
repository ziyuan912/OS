import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1], 1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
height, length, x = hsv.shape
for i in range(height):
	for j in range(length):
		(h, s, v) = hsv[i][j]
		if 0 < h and h < 20 and 28 < s and s < 256 and 50 < v and v < 256:
			continue
		else:
			img[i][j] = (0,0,0)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
