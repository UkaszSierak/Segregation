import ImageProcessing
import cv2 as cv
import numpy as np
import functions


class Object:
    def __init__(self, source_image,roi_image, ref_point):
        self.source_image = source_image
        self.object_image = roi_image
        self.ref_point = ref_point
        self.contours = self.GetContours()
        self.parameters = self.CalcParameters()
        self.container = None
        self.center = self.CalcReferingToOryginal()
        self.rotation = self.parameters['angle']

    def CalcRatio(self):

        if self.parameters['width'] != 0 and self.parameters['height'] != 0:

            if self.parameters['width'] >= self.parameters['height']:

                ratio = self.parameters['width'] / self.parameters['height']

            else:

                ratio = self.parameters['height'] / self.parameters['width']

        else: ratio = 0

        return ratio

    def GetContours(self):

        output_image, contours, hierarchy = cv.findContours(ImageProcessing.Prepare(self.object_image), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

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

    def CalcReferingToOryginal(self):

        return [ a + b for a, b in zip(self.ref_point, self.parameters['center'])]

    def GetFromCameraDistance(self):

        def PixToMM(dist_in_pix: float):
            return dist_in_pix * 0.4

        x_delta = PixToMM(float(self.source_image.shape[1] - self.center[0]))
        y_delta = PixToMM(float(self.source_image.shape[0] - self.center[1]))

        return [x_delta, y_delta]

    def __hash__(self):
        return hash(self.center)













