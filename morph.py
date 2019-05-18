
import skimage
import cv2
import numpy as np

import sys

def show_image(img):
	cv2.imshow('img',img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def hole_filling(im_in,k):
	h,l=im_in.shape
	tmp=np.zeros((h,l))
	tmp_inv=np.zeros((h,l))
	for i in range(h):
		for j in range(l):
			if im_in[i][j]!=0:
				tmp[i][j]=1
			else:
				tmp_inv[i][j]=1
	tmp2=tmp
	iterations=10
	kernel = np.ones((k,k),np.uint8)
	for i in range(iterations):
		dilation = cv2.dilate(tmp,kernel,iterations = 1)
		for j in range(h):
			for k in range(l):
				if dilation[j][k]==1 and tmp_inv[j][k]==1:
					tmp[j][k]=1
	for i in range(h):
		for j in range(l):
			if tmp[i][j]==1:
				tmp2[i][j]=1
	return tmp2


def after_eliminate_by_opening(opening,img):
	height, length= img.shape
	for i in range(height):
		for j in range(length):
			if opening[i][j]==0:
				img[i][j]=0
	return img


def perform_opening(img,k):
	kernel = np.ones((k,k),np.uint8)
	opening = cv2.morphologyEx(img, cv2.MORPH_OPEN,kernel)
	return opening




img = cv2.imread(sys.argv[1], 1)
img2=img
img=cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
img = skimage.color.rgb2gray(img)
img2=skimage.color.rgb2gray(img2)
#cv2.imwrite('gray.jpeg',im2)
height, length= img.shape
#show_image(img)
#perform thesholding
for i in range(height):
	for j in range(length):
		if img[i][j]<0.2:
			img[i][j]=0
#opening and hole filling first time by a smaller kernel
opening=perform_opening(img,3)
opening=hole_filling(opening,3)
img=after_eliminate_by_opening(opening,img)
#opening by a bigger kernel
opening=perform_opening(img,5)
opening=hole_filling(opening,5)

img=after_eliminate_by_opening(opening,img2)
#scale to 0~255
img*=255
cv2.imwrite('output2.jpg',img)