import cv2
import numpy as np
import sys

def delete(img, labels, delleabel):
	height, length= img.shape
	for i in range(height):
		for j in range(length):
			if labels[i][j] != 0:
				if delleabel[labels[i][j] - 1] == 1:
					img[i][j] = 0
			else:
				img[i][j] = 0
def euler_component(img, label, E, h, l, bound):
	cnt = 1
	label[h][l] = E
	if l != 0:
		if label[h][l - 1] != E and img[h][l - 1] < 50 and l-1 >= bound[2]:
			if l-1 == bound[2]:
				return 0
			cnt += euler_component(img, label, E, h, l-1, bound)
	if l != img.shape[1] - 1:
		if label[h][l + 1] != E and img[h][l + 1] < 50 and l+1 <= bound[3]:
			if l+1 == bound[3]:
				return 0
			cnt += euler_component(img, label, E, h, l+1, bound)
	if h != 0:
		if label[h - 1][l] != E and img[h - 1][l] < 50 and h-1 >= bound[0]:
			if h-1 == bound[0]:
				return 0
			cnt += euler_component(img, label, E, h - 1, l, bound)
	if h != img.shape[0] - 1:
		if label[h + 1][l] != E and img[h + 1][l] < 50 and h+1 <= bound[1]:
			if h+1 == bound[1]:
				return 0
			cnt += euler_component(img, label, E, h + 1, l, bound)
	return cnt

def euler_number(img, holelabel, ranges, ret):
	C = 1
	E = 0
	for h in range(ranges[ret][0],ranges[ret][1]):
		for l in range(ranges[ret][2],ranges[ret][3]):
			if img[h][l] < 50 and holelabel[h][l] == 0:
				E += 1
				bound = ranges[ret]
				cnt = euler_component(img, holelabel, E, h, l, bound)
				if cnt > 100:
					E -= 1
	return C - E
		

if __name__ == '__main__':
	sys.setrecursionlimit(100000)
	img = cv2.imread(sys.argv[1])
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	binary = cv2.threshold(gray,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	height, length= gray.shape
	ret, labels = cv2.connectedComponents(binary)
	ranges = [[np.inf, 0, np.inf, 0] for i in range(ret-1)]
	delleabel = [0 for i in range(ret-1)]
	for i in range(height):
		for j in range(length):
			if labels[i][j] != 0:
				if i < ranges[labels[i][j] - 1][0]:
					ranges[labels[i][j] - 1][0] = i
				if i > ranges[labels[i][j] - 1][1]:
					ranges[labels[i][j] - 1][1] = i
				if j < ranges[labels[i][j] - 1][2]:
					ranges[labels[i][j] - 1][2] = j
				if j > ranges[labels[i][j] - 1][3]:
					ranges[labels[i][j] - 1][3] = j
	for i in range(ret-1):
		if ranges[i][1] - ranges[i][0] < 20 or ranges[i][3] - ranges[i][2] < 20:
			delleabel[i] = 1
		elif (ranges[i][1] - ranges[i][0])/(ranges[i][3] - ranges[i][2]) < 0.5:
			delleabel[i] = 1
		elif (ranges[i][3] - ranges[i][2])/(ranges[i][1] - ranges[i][0]) < 0.5:
			delleabel[i] = 1
		elif ranges[i][0] == 0 or ranges[i][1] == height-1 or ranges[i][2] == 0 or ranges[i][3] == length-1:
			delleabel[i] = 1
	delete(gray, labels, delleabel)
	cv2.imwrite('output3.jpg', gray)
	holelabel = np.zeros((labels.shape))
	for i in range(ret - 1):
		for h in range(height):
			for l in range(length):
				holelabel[h][l] = 0
		euler = euler_number(gray, holelabel, ranges, i)
		part = gray[ranges[i][0]:ranges[i][1],ranges[i][2]:ranges[i][3]]
		"""if delleabel[i] != 1:
			cv2.imshow('ya',part)
			cv2.waitKey(1000)
			print(i, euler)"""
		if euler >= -9:
			delleabel[i] = 1
	delete(gray, labels, delleabel)
	cv2.imwrite('output4.jpg', gray)
