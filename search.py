'''
python search.py --query crop.png --index index.pickle
'''
from tools.zernikemoments import ZernikeMoments
from tools.searcher import Searcher
from tools import imutils
import numpy as np
import argparse
import pickle
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required = True)
ap.add_argument("-i", "--index", required = True)
args = vars(ap.parse_args())

index = pickle.loads(open(args["index"], "rb").read())
query = cv2.imread(args["query"])
query = cv2.cvtColor(query, cv2.COLOR_BGR2GRAY)
query = imutils.resize(query, width = 64)
cv2.imshow("query", query)

#在thresholdType为thresholdType时blockSize(11)越大c(5)越小maxValue越多
thresh = cv2.adaptiveThreshold(query, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 5)
#thresh1 = cv2.adaptiveThreshold(query, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 7, 11)
#cv2.imshow("thresh", thresh)
#cv2.imshow("thresh1", thresh1)
outline = np.zeros(que时ry.shape, dtype = "uint8")
(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
cv2.drawContours(outline, [cnts], -1, 255, -1)
cv2.imshow("outline", outline)

desc = ZernikeMoments(21)
queryFeature = desc.describe(outline)
searcher = Searcher(index)
results = searcher.search(queryFeature)

spriteName = results[0][1]	
spriteImage = cv2.imread("sprites\\"+spriteName+".png")
print("The Pokemon is:%s" % spriteName)
cv2.imshow("sprite", spriteImage)
cv2.waitKey(0)