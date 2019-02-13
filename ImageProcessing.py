"""
    Image Processing module contains majority of functions which are used to preprocessed,
    processed and analise image.

    Functions:
                viewImages() - only for testing purposes, views image
                prepare() - held all preprocessing actions in image processing such as converting to grey, binarizing and applaying Canny filter,

                shadowCorrection() - reduce shadow influence on image processing, performed on image ROIs which contains detected objects,
                                     shadow reduce mechanism is described in function ShadowReduce() in test_c.pyx module
                getObject() - extract all detected object ROIS from image
                getContours - return contours data from image
"""

from functions import *
import numpy
import test_c

def viewImages(images: list):

    for idx, item in enumerate(images):
        cv.imshow(str(idx), item )
    cv.waitKey()

def prepare(image: numpy.ndarray):

    image_container = image


    if image_container.ndim == 3:
        image_container = cv.cvtColor(image_container, cv.COLOR_RGB2GRAY)
    else:
        pass

    image_container = binarize(image_container)
    image_container = AutoCanny(image_container)

    return image_container

def shadowCorrection(contours ,image: np.ndarray):

    im = np.asanyarray(image, dtype=np.int)
    objects = []
    ref_points = []

    for cell in contours:

        x1, y1, width, height = cv.boundingRect(cell)
        x1 -= 5
        y1 -= 5
        height += 10
        width += 10
        y2 = y1 + height
        x2 = x1 + width
        shape = (height, width)
        gray = np.empty(shape, dtype = np.int)
        test_c.ShadowReduce(im[y1:y2, x1:x2], gray)
        grey = np.uint8(gray)

        objects.append(grey)
        ref_points.append([x1,y1])

    return objects, ref_points

def getObjects(image):

    prepared_image = prepare(image)
    img, contours, hierarchy = cv.findContours(prepared_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    objects, ref_points = shadowCorrection(contours,image)

    return objects, ref_points

def getContours(objects: list):

    list = []

    for idx, object in enumerate(objects):
        obrazek, kontury, hierarchia = cv.findContours(prepare(object), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        list.append(kontury)

    return list

if __name__ == '__main__':

    import cv2 as cv
    import Object
    from database import *
    from Trajectory import *
    import RobotControlProgram

    image = cv.imread('test5.jpg')
    image = scaleUp(image)
    message = 'QoKX;290.62;Y;-0.09;Z;11.26;A;-179.94;B;-0.26;C;179.93;L1;0.00;;6,0;100;0.00;00000000'
    current_location = ExtractCoordinates(message)
    objects, ref_points = getObjects(image)
    objects = [ Object.Object(image,object, ref_point)  for object, ref_point in zip(objects,ref_points)]
    containers = {'2block': (298.6117,0.00,339.8730,0.00,178.7203,0.00),
                  '4block': (327.6703,-252.0321,125.6951,0.00,178.7204,0.0000),
                  '3block': (237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)}

    trajectory = Trajectory()
    for key, value in containers.items():
        trajectory.addPoint(value)

    data = ReadFromDB()
    for item in objects:
        item.assignContainer(data)
        container = item.container
        x_delta, y_delta = item.getCamDistance()
        correction = {'X': current_location['X'] + x_delta,
                      'Y': current_location['Y'] + y_delta,
                      'A': item.rotation}
        new_location = GetNewLocation(correction, current_location)
        prepared_location = PrepareLocation(new_location)

        trajectory.addPoint(prepared_location)
        trajectory.addRelation(prepared_location,containers[container])

    robot = RobotControlProgram.RobotControlProgram(trajectory.point_list, trajectory.point_relations, '/dev/USB')
    robot.generate()
    robot.chopp()
