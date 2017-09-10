'''
python index.py --sprites sprites --index index.pickle
'''
from tools.zernikemoments import ZernikeMoments
import numpy as np
import pickle
import glob
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--sprites", required = True)
ap.add_argument("-i", "--index", required = True)
args = vars(ap.parse_args())

desc = ZernikeMoments(21)
index = {}

for spritePath in glob.glob(args["sprites"]+"\\*.png"):
	pokemon = spritePath[spritePath.rfind("\\")+1:].replace(".png", "")
	image = cv2.imread(spritePath)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cv2.imshow("gray", image)
	#print("gray[0]:%s" % image[0])
	image = cv2.copyMakeBorder(image, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value = 255)
	cv2.imshow("border", image)
	#print("border[0]:%s" % image[0])
	thresh = cv2.bitwise_not(image)
	cv2.imshow("thresh", thresh)
	thresh[thresh > 0] = 255
	cv2.imshow("thresh1", thresh) 

	outline = np.zeros(thresh.shape, dtype = "uint8")
	(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
	cv2.drawContours(outline, [cnts], -1, 255, -1)
	cv2.imshow("outline", outline)
	
	moments = desc.describe(outline)
	index[pokemon] = moments
	#print(moments)
	#cv2.waitKey(0)

with open(args["index"], "wb") as f:
	f.write(pickle.dumps(index))