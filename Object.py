"""
    Module contains definition of recognized object in certain attributes: 
       
        source_image   - source image  
        object_image   - ROI form source image witch contains object view
        ref_point      - corner pixel coordinates of ROI in source image
        contours       - recognized object contours data
        parameters     - dictionary of all object parameters such as height, width, rotation angle, center points and box points
        container      - container name witch object needs to be insert
        center         - center points of recognized object in pixels 
        rotation       - rotation angle of object
       
    Class definition contains following methods: 
        
        calcRatio()         - calculating object descriptor based on object height and width
        getContours()       - return object contours from image
        calcParameters()    - calculate object parameters based on contours 
        assignContainer()   - recognise object by assigning dedicated container name
        referringOriginal() - calculate image center point in pixel on source image
        getCamDistance()    - calc distance in mm from center of camera to object center in 2D

"""
import ImageProcessing
import cv2 as cv
import numpy as np

class Object:
    def __init__(self, source_image,roi_image, ref_point):
        self.source_image = source_image
        self.object_image = roi_image
        self.ref_point = ref_point
        self.contours = self.getContours()
        self.parameters = self.calcParameters()
        self.container = None
        self.center = self.referringOriginal()
        self.rotation = self.parameters['angle']

    def calcRatio(self) -> float:

        if self.parameters['width'] != 0 and self.parameters['height'] != 0:

            if self.parameters['width'] >= self.parameters['height']:

                ratio = self.parameters['width'] / self.parameters['height']

            else:

                ratio = self.parameters['height'] / self.parameters['width']

        else: ratio = 0

        return ratio

    def getContours(self):

        output_image, contours, hierarchy = cv.findContours(ImageProcessing.prepare(self.object_image), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        return contours[0]

    def calcParameters(self):

        parameters = {}
        rect = cv.minAreaRect(self.contours)

        parameters['center'] = rect[0]
        parameters['width'] = int(rect[1][0])
        parameters['height'] = int(rect[1][1])
        parameters['angle'] = rect[2]
        box = cv.boxPoints(rect)
        parameters['boxPnts'] = np.int0(box)

        return  parameters

    def assignContainer(self, data):

        ratio = self.calcRatio()

        if ratio != 0:
            container = None
            match = 1

            for row in data:

                y = abs(row[3] - ratio)
                if y < match:
                    match = y
                    container = row[0]
            self.container = container

    def referringOriginal(self):

        return [ a + b for a, b in zip(self.ref_point, self.parameters['center'])]

    def getCamDistance(self):

        mm_value = lambda dist_in_pix: dist_in_pix * 0.4

        x_delta = mm_value(float(self.source_image.shape[1] - self.center[0]))
        y_delta = mm_value(float(self.source_image.shape[0] - self.center[1]))

        return [x_delta, y_delta]

    def __hash__(self):
        return hash(self.center)












