import cv2 as cv

hehe = cv.imread('zshadow.png')
hehe2 = ~hehe
cv.imwrite('shadowup.png',hehe2)