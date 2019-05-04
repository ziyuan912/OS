import cv2
import numpy as np
import sys

img = cv2.imread(sys.argv[1], 1)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
height, length, x = hsv.shape
for i in range(height):
	for j in range(length):
		(h, s, v) = hsv[i][j]
		"""if s >= 10 and v >= 40 and s <= (-1*h-0.1*v+110) and h <= (-0.4*v + 75):
			if h >= 0 and s <= 0.08*(100 - v)*h + 0.5*v:
				continue
			elif s <= 0.5*h + 35:
				continue
			else:
				#print(i,j)
				img[i][j] = (0,0,0)"""
		if 0 < h and h < 20 and 28 < s and s < 256 and 50 < v and v < 256:
			continue
		else:
			img[i][j] = (0,0,0)

#mask = cv2.inRange(hsv, lower_blue, upper_blue)
#res = cv2.bitwise_and(img,img, mask = hsv)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
