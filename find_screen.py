from tools import imutils
from tools.transform import four_point_transform
from skimage import exposure
import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--query", required = True)
args = vars(ap.parse_args())

image = cv2.imread(args["query"])
#cv2.imshow("image", image)
print(image.shape)
ratio = image.shape[0] / 300.0
orig = image.copy()
image = imutils.resize(image, height = 300)
#image = imutils.rotate_flip(image, 1)
#cv2.imshow("image", image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
edged = cv2.Canny(gray, 30, 200)
'''
edged = imutils.rotate_flip(image, 1)
edged1 = imutils.rotate_flip(image, -1)
edged2 = imutils.rotate_flip(image, 0)
cv2.imshow("edged", edged)
cv2.imshow("edged1", edged1)
cv2.imshow("edged2", edged2)
'''
(_, cnts, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

for c in cnts:
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)

	if len(approx) == 4:
		screenCnt = approx
		break

orig1 = image.copy()
cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
#cv2.imshow("screen", image)

#image.shape[:2]只取imag的高和宽，不取通道值，因为mask为单通道
mask = np.zeros(image.shape[:2], dtype = "uint8")
#轮廓内填充白色作为掩码
cv2.drawContours(mask, [screenCnt], -1, 255, -1)
#应用掩码显示轮廓内部分
cv2.imshow("Masked", cv2.bitwise_and(orig1, orig1, mask = mask))
print(screenCnt)

pts = screenCnt.reshape(4, 2)
warp = four_point_transform(orig, pts*ratio)
warp = imutils.resize(warp, height = 300)
warp = cv2.cvtColor(warp, cv2.COLOR_BGR2GRAY)
warp = exposure.rescale_intensity(warp, out_range = (0, 255))

(h, w) = warp.shape
(dX, dY) = (int(w * 0.4), int(h * 0.4))
crop = warp[10:dY, w - dX:w - 10]
cv2.imwrite("crop.png", crop)
cv2.imshow("warp", imutils.resize(warp, height = 300))
cv2.imshow("crop", imutils.resize(crop, height = 300))
cv2.waitKey(0)