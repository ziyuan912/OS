import cv2
import numpy as np 
from PIL import Image
import time
import skimage

def create_binary_im(im):
	x,y,z=im.shape
	binary_im=np.zeros([x,y])
	for i in range(x):
		for j in range(y):
			if im[i][j][0]!=0 or im[i][j][1]!=0 or im[i][j][2]!=0:
				binary_im[i][j]=255
	return binary_im


im=cv2.imread('output3.jpeg')
_,_,z=im.shape
if z!=0:
	binary_im=create_binary_im(im)

im_original=cv2.imread('../sample/test.jpeg')
im=im.astype(np.uint8)

w=25
h=35

temp='../sample/template.png'

general_face_template=Image.open(temp)
general_face_template=general_face_template.resize( (w, h), Image.BILINEAR )
general_face_template.save(temp)
general_face_template=cv2.imread(temp)

def template_matching(im ,template):
	global threshold
	res = cv2.matchTemplate(im,template,cv2.TM_CCOEFF_NORMED)
	return res

def draw_black_rec(im,x,y):
	global w,h
	pt=np.array([x,y])
	cv2.rectangle(im, (pt[0]-10,pt[1]-20), (pt[0] + w+10, pt[1] + h+20), (0,0,0), -1)
	return im


def out_of_index(x,y,x_max,y_max):
	if x<0 or x>=x_max or y<0 or y>=y_max:
		return True
	return False

def mark_face(im,x,y):
	global w,h,binary_im
	x_max,y_max,ppp=im.shape
	count=0
	x_max,y_max,z_max=im.shape
	for i in range(w):
		for j in range(h):
			if out_of_index(x+i,y+j,x_max,y_max):
				continue
			if binary_im[i+x][j+y]==0:
				count+=1
	x-=int(w/2)
	y-=int(h/2)
	pt=np.array([x,y])
	cv2.rectangle(im, (pt[1],pt[0]), (pt[1] + w, pt[0] + h), (7,249,151), 2)
	return im

def draw_black_result(im,x,y):
	global w,h
	x_max,y_max=im.shape
	x-=w
	y-=h
	for i in range(2*h):
		for j in range(2*w):
			if out_of_index(i+x,j+y,x_max,y_max):
				continue
			im[i+x][j+y]=0
	return im 



result=template_matching(im,general_face_template)
a,b=result.shape
im_original = cv2.resize(im_original, (b, a), interpolation=cv2.INTER_CUBIC)
binary_im = cv2.resize(binary_im, (b, a), interpolation=cv2.INTER_CUBIC)
x,y=np.unravel_index(np.argmax(result, axis=None), result.shape)
value=result[x][y]
while value>0.42:
	im_original=mark_face(im_original,x,y)
	result=draw_black_result(result,x,y)
	x,y=np.unravel_index(np.argmax(result, axis=None), result.shape)
	value=result[x][y]

cv2.imwrite('output_last.jpg',im_original)
		