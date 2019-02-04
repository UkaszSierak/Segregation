from functions import *
import numpy
import test_c
import cv2 as cv
import ObjectClass
from database import *

def View_images(images: list):

    for idx, item in enumerate(images):
        cv.imshow(str(idx), item )
    cv.waitKey()

def Prepare(image: numpy.ndarray):

    image_container = image


    if image_container.ndim == 3:
        image_container = cv.cvtColor(image_container, cv.COLOR_RGB2GRAY)
    else:
        pass

    image_container = binarize(image_container)
    image_container = AutoCanny(image_container)


    return image_container

def ShadowCorrection(contours ,image: np.ndarray):

    im = np.asanyarray(image, dtype=np.int)
    list = []
    for cell in contours:

        x1, y1, width, height = cv.boundingRect(cell)
        y2 = y1 + height
        x2 = x1 + width
        shape = (height, width)
        gray = np.empty(shape, dtype = np.int)
        test_c.ShadowReduce(im[y1:y2, x1:x2], gray)
        grey = np.uint8(gray)

        list.append(grey)


    return list

def GetObjects(image):

    prepared_image = Prepare(image)
    img, contours, hierarchy = cv.findContours(prepared_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    objects = ShadowCorrection(contours,image)


    return objects

def GetContours(objects: list):

    list = []

    for idx, object in enumerate(objects):
        image = cv.copyMakeBorder(object, top=5, bottom=5, left=5, right=5, borderType= cv.BORDER_CONSTANT, value=0)
        obrazek, kontury, hierarchia = cv.findContours(Prepare(image), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        list.append(kontury)

    return list

if __name__ == '__main__':
    image = cv.imread('test7.jpg')
    image = scaleUp(image)

    objects = GetObjects(image)
    data = ReadFromDB()
    i = 0
    for item in objects:

        object = ObjectClass.Object(item)
        ratio = object.CalcRatio()
        object.AssignContainer(data)
        print('Detected object id {}'.format(i))
        print('Ratio of detected object is: {}'.format(ratio))
        print('Detected object is {}'.format(object.container))
        print('')
        i += 1

    View_images(objects)




