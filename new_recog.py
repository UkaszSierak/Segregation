
from functions import *
from database import *
from matplotlib import pyplot as plt
import obiekty
import numpy as np
import test_c
import cv2 as cv


def Recognition(image,name):
    cv.imwrite(name + '.png', image)

    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    gray2 = gray

    bin = binarize(gray,'binary')


    edges = AutoCanny(bin)


    gray = np.asanyarray(gray, dtype=np.int)


    gray[gray < 255] = 0


    img, contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    im = np.asanyarray(image, dtype=np.int)


    for cell in contours:
        x1, y1, width, height = cv.boundingRect(cell)
        x2 = x1 + width
        y2 = y1 + height
        test_c.ShadowReduce(im, gray, y1, x1, y2, x2)


    gray = np.uint8(gray)

    bin2 = binarize(gray2,'otsu')


    bin = binarize(gray,'otsu')
    cv.imwrite('bez_shadow.png', bin2)
    cv.imwrite('zshadow'+name+'.png', bin)

    edges = AutoCanny(bin)

    img, contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # ogarnięcie hierarhii konturów
    obj = []
    obj_finall = []
    indeksik = hierarchy[0][0][0]

    accum = obiekty.Object('Obiekt1', contours[0])

    obj.append(accum)
    i = 1
    if indeksik != -1:
        while (1):
            i += 1
            if hierarchy[0][indeksik][3] == -1 and hierarchy[0][indeksik][0] != -1:
                accum = obiekty.Object('Obiekt' + str(i), contours[indeksik])
                obj.append(accum)
                indeksik = hierarchy[0][indeksik][0]
            else:
                if hierarchy[0][indeksik][3] == -1 and hierarchy[0][indeksik][0] == -1:
                    accum = obiekty.Object('Obiekt' + str(i), contours[indeksik])
                    obj.append(accum)
                    break

    data = ReadFromDB()

    for objct in obj:
        objct.clasify(data)
        if objct.getClass() != False:
            obj_finall.append(objct)


    return obj_finall


def RecognitionOld(image):
    height, width, chan = image.shape
    im = np.asanyarray(image, dtype=np.int)
    gray = ShadowReduce(image)


    bin = binarize(gray, 'otsu')

    edges = AutoCanny(bin)

    img, contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    # ogarnięcie hierarhii konturów
    obj = []
    obj_finall = []
    indeksik = hierarchy[0][0][0]

    accum = obiekty.Object('Obiekt1', contours[0])

    obj.append(accum)
    i = 1
    if indeksik != -1:
        while (1):
            i += 1
            if hierarchy[0][indeksik][3] == -1 and hierarchy[0][indeksik][0] != -1:
                accum = obiekty.Object('Obiekt' + str(i), contours[indeksik])
                obj.append(accum)
                indeksik = hierarchy[0][indeksik][0]
            else:
                if hierarchy[0][indeksik][3] == -1 and hierarchy[0][indeksik][0] == -1:
                    accum = obiekty.Object('Obiekt' + str(i), contours[indeksik])
                    obj.append(accum)
                    break

    data = ReadFromDB()

    for objct in obj:
        objct.clasify(data)
        if objct.getClass() != False:
            obj_finall.append(objct)

    return obj_finall