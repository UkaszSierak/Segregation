import cv2 as cv
from functions import *
from database import *
from matplotlib import pyplot as plt



def Recognition(image):

    gray = ShadowReduce(image)
    bin = binarize(gray)
    edges = AutoCanny(bin)

    img, contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    #ogarnięcie hierarhii konturów
    cnt=[]
    indeksik = hierarchy[0][0][0]
    cnt.append(contours[0])
    if indeksik != -1:
        while(1):
            if hierarchy[0][indeksik][3] == -1 and hierarchy[0][indeksik][0] != -1:
                cnt.append(contours[indeksik])
                indeksik = hierarchy[0][indeksik][0]
            else:
                if hierarchy[0][indeksik][3] == -1 and hierarchy[0][indeksik][0] == -1:
                    cnt.append(contours[indeksik])
                    break

    ratio, center, points, width, height, theta = Rectangle(image, cnt)

    data = ReadFromDB()

    indx_lst = []
    for row1 in ratio:
        match = 10
        for row2 in data:
            a = abs(1 - row2[3] / row1)

            if a < match:
                match = a
                indx = row2

        indx_lst.append(indx)

    i = 0
    for row in indx_lst:
        cv.putText(image, row[0] + row[2], (int(center[i][0]), int(center[i][1])), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.5,
                   (255, 255, 255), 1, cv.LINE_AA)
        cv.putText(image, str(ratio[i]), (int(center[i][0]), int(center[i][1]) - 30), cv.FONT_HERSHEY_COMPLEX_SMALL,
                   0.5, (255, 255, 255), 1, cv.LINE_AA)
        i += 1





