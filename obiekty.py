import math
import cv2 as cv
import numpy as np

class Object:

    def __init__(self, name, cntrs):

        self.clasified = []
        self.name = name                                                                       # nazwa obiektu
        self.cntrs = cntrs                                                                     # kontur

        self.center, self.width, self.height, self.angle, self.boxPnts = self.calcParams()
        self.ratio = self.calcRatio()                                                            # współczynnik kształtu


    def getWidth(self):

        return self.width
    def getHeight(self):

        return self.height

    def getCenter(self):
        return self.center

    def getAngle(self):
        return self.angle

    def getBox(self):
        return self.boxPnts
    def getClass(self):
        return self.clasified[0]
    def getRatio(self):
        return self.ratio


    def calcParams(self):   #wyliczanie parametrów obiektu

        rect = cv.minAreaRect(self.cntrs)

        center = rect[0]
        width = int(rect[1][0])
        height = int(rect[1][1])
        angle = rect[2]
        box = cv.boxPoints(rect)
        boxPnts = np.int0(box)



        return center, width, height, angle, boxPnts




    def calcRatio(self):    #wyliczanie współczynnika kształtu obiektu

        if self.width != 0 and self.height != 0:

            if self.width >= self.height:

                ratio = self.width / self.height

            else:

                ratio = self.height / self.width
        else: ratio = 0

        return ratio



    def clasify(self,data):      #klasyfikowanie obiektu

        if self.ratio != 0:

            match = 10

            for row in data:

                a = abs(1 - row[3] / self.ratio)
                if a < match:
                    match = a
                    index = row[0] + row[2]

            self.clasified.append(index)
        else:
            self.clasified.append(False)

    def drawOnImg(self, img):
        cv.drawContours(img, [self.boxPnts], 0, (0, 0, 255), 2)
        cv.putText(img, str(self.clasified), (int(self.center[0]), int(self.center[1])), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 1, cv.LINE_AA)
        cv.putText(img, str(self.ratio), (int(self.center[0]), int(self.center[1]) - 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255), 1, cv.LINE_AA)


