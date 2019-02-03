import math
import re
import cv2 as cv
import numpy as np


def GetROIpoints(points):

    z = [[x for x, y in points], [y for x, y in points]]

    x_min = np.amin(z[0])-25
    x_max = np.amax(z[0])+25
    y_min = np.amin(z[1])-25
    y_max = np.amax(z[1])+25

    corners = [[x_min, x_max],[y_min, y_max]]

    return corners

def scaleUp(image):
    max_dimension = max(image.shape)
    scale = 700 / max_dimension
    image = cv.resize(image, None, fx=scale, fy=scale)

    return image


def binarize(image):

    blur = cv.GaussianBlur(image, (7, 7), 0)
    ret, th = cv.threshold(blur, 0, 255, cv.THRESH_OTSU)
    return th


def Harlick(contour, center):
    sum_1 = 0
    sum_2 = 0
    cont_lenght = len(contour[0])

    for c in range(0, len(contour[0]) - 1):
        a = math.sqrt(pow(contour[0][c][0][0] - center[0], 2) + pow(contour[0][c][0][1] - center[1], 2))
        sum_1 += a
        sum_2 += pow(a, 2)

    Rh = math.sqrt((pow(sum_1, 2)) / (cont_lenght * sum_2 - 1))

    return Rh


def ShadowReduce(img):

    height, width, chan = img.shape
    gray_img = np.zeros((height, width), np.uint8)

    im = np.asanyarray(img)

    dupa = im.shape

    rows = dupa[0]
    cols = dupa[1]

    gray_img.argmax()
    im[100, 100].argmax(0)

    print(im[100,100].argmax(0))

    for x in range(cols):
        for y in range(rows):
            sum = 0
            max = im[y][x][im[y][x].argmax(0)]
            for cell in range(3):
                pix = im.item(y,x,cell)
                sum += max - pix
            if sum > 255:
                gray_img.itemset((y,x),255)
            else:
                gray_img.itemset((y,x),sum)


    return gray_img


def AutoCanny(img, dest = None):
    hi_thrs1, thrsh_src = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    low_thrs1 = 0.5 * hi_thrs1

    edge = cv.Canny(img, low_thrs1, hi_thrs1)


    return edge


def Rectangle(img, cnt):

    obct = len(cnt)
    ratio = []
    center = []
    points = []
    theta = []
    width = []
    height = []
    print("Ile obiektów : ")
    print(obct)
    if(obct > 1):

        for x in range(0,obct):
            rect = cv.minAreaRect(cnt[x])
            box = cv.boxPoints(rect)
            box = np.int0(box)
            cv.drawContours(img, [box], 0, (0, 0, 255), 2)

            ratio.append(np.amax(rect[1]) / np.amin(rect[1]))
            center.append(rect[0])

            points.append(box)

            width.append(int(rect[1][0]))
            height.append(int(rect[1][1]))
            theta.append(rect[2])
    else:

        rect = cv.minAreaRect(cnt[0])
        box = cv.boxPoints(rect)
        box = np.int0(box)
        cv.drawContours(img, [box], 0, (0, 0, 255), 2)

        ratio.append(np.amax(rect[1]) / np.amin(rect[1]))
        center.append(rect[0])

        points.append(box)

        width.append(int(rect[1][0]))
        height.append(int(rect[1][1]))
        theta.append(rect[2])

    return ratio, center, points,width, height, theta


def subimage(image, center, theta, width, height):

   '''
   Rotates OpenCV image around center with angle theta (in deg)
   then crops the image according to width and height.
   '''

   # Uncomment for theta in radians
   #theta *= 180/np.pi

   shape = image.shape[:2]

   matrix = cv.getRotationMatrix2D(center, theta, 1 )
   image = cv.warpAffine( image, matrix, shape )

   x = int( center[0] - width/2  )
   y = int( center[1] - height/2 )

   image = image[ y:y+height, x:x+width ]

   return image

def AccesROI(img, corners, centers):

    roi = img[corners[1][0]:corners[1][1], corners[0][0]:corners[0][1]]

    new_centers = (centers[0] - corners[0][0], centers[1] - corners[1][0])

    return roi, new_centers

def getPos(string, value):

    x = re.findall(value+';-\d+\.\d+|'+value+';\d+\.\d+',string)
    x = float(re.sub(value + ';', '', x[0]))
    return x