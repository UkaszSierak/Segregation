import ImageProcessing
import cv2 as cv
import numpy as np


class Object:
    def __init__(self, image):
        self.object_image = image
        self.contours = self.GetContours()
        self.parameters = self.CalcParameters()
        self.container = None

    def CalcRatio(self):

        if self.parameters['width'] != 0 and self.parameters['height'] != 0:

            if self.parameters['width'] >= self.parameters['height']:

                ratio = self.parameters['width'] / self.parameters['height']

            else:

                ratio = self.parameters['height'] / self.parameters['width']

        else: ratio = 0

        return ratio

    def GetContours(self):

        expanded_image = cv.copyMakeBorder(self.object_image, top=5, bottom=5, left=5, right=5, borderType=cv.BORDER_CONSTANT, value=0)
        output_image, contours, hierarchy = cv.findContours(ImageProcessing.Prepare(expanded_image), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        return contours[0]

    def CalcParameters(self):

        parameters = {}
        rect = cv.minAreaRect(self.contours)

        parameters['center'] = rect[0]
        parameters['width'] = int(rect[1][0])
        parameters['height'] = int(rect[1][1])
        parameters['angle'] = rect[2]
        box = cv.boxPoints(rect)
        parameters['boxPnts'] = np.int0(box)

        return  parameters


    def AssignContainer(self, data):

        ratio = self.CalcRatio()

        if ratio != 0:
            container = None
            match = 1

            for row in data:

                y = abs(row[3] - ratio)
                if y < match:
                    match = y
                    container = row[0]
            self.container = container


