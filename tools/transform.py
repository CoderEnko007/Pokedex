import numpy as np
import cv2

def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")

	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	print("pts = "+str(pts))
	print("sum = "+str(s))
	print("diff = "+str(diff))
	print("rect = "+str(rect))
	return rect

def four_point_transform(image, pts):
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	widthA = np.sqrt((tl[0]-tr[0])**2 + (tl[1]-tr[1])**2)
	widthB = np.sqrt((bl[0]-br[0])**2 + (bl[1]-br[1])**2)
	maxWidth = max(int(widthA), int(widthB))
	#print(type(maxWidth))

	heightA = np.sqrt((tl[0]-bl[0])**2 + (tl[1]-bl[1])**2)
	heightB = np.sqrt((tr[0]-br[0])**2 + (tr[1]-br[1])**2)
	maxHeight = max(int(heightA), int(heightB))
	#print(type(maxHeight))

	dst = np.array([
		[0, 0],
		[maxWidth-1, 0],
		[maxWidth-1, maxHeight-1],
		[0, maxHeight-1]], dtype = "float32")
	print("dst = "+str(dst))
	M = cv2.getPerspectiveTransform(rect, dst)
	warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

	return warp