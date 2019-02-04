from RobotControlClass import *
from melfa_IV import *
import numpy as np
import functions
import cv2 as cv
import ImageProcessing



def GenerateProgram( robot: RobotControl, objects_locations: list, containers_location: dict, ):

    program_list = []
    containers_list = []
    destination = dict
    id = None

    for idx, item in enumerate(objects_locations):

        id = idx +1
        offset = 10 * (idx * 2 + 1)
        next_offset = offset + 10


        if item.get('container') not in containers_list:
            containers_list.append(item.get('container'))

        program_list.append(robot.edit_line(offset, defin_position(id)))
        program_list.append(robot.edit_line(next_offset, declare_position(id, item.get('location'))))

    for item in containers_list:
        id += 1

        offset = 10 + next_offset
        next_offset = 10 + offset

        program_list.append(robot.edit_line(offset, defin_position(id)))
        program_list.append(robot.edit_line(next_offset, declare_position(id, containers_location.get(item))))



    return program_list






if __name__ == '__main__':


    #objects = [{'location': (327.6703,-252.0321,125.6951,0.00,178.7204,0.0000), 'container': 'small', 'variable': None},
     #                    {'location': (627.6703,-252.0321,125.6951,0.00,178.7204,0.0000), 'container': 'medium', 'variable': None}]

    #containers_location = {'small': (727.6703,-252.0321,125.6951,0.00,178.7204,0.0000),
    #                       'medium': (827.6703,-252.0321,125.6951,0.00,178.7204,0.0000),
    #                       'large': (927.6703,-252.0321,125.6951,0.00,178.7204,0.0000)}

    #robot = RobotControl('USB')

    #program_list = GenerateProgram(robot, objects_locations, containers_location)

    #for line in program_list:
    #    print(line)

    """image = cv.imread('test5.jpg', 0)
    image = functions.scaleUp(image)
    ImageProcessing.View_images([image])

    x1 = 40
    y1 = 50
    width = 100
    height =250
    x2 = x1 + width
    y2 = y1 + height
    shape = (height, width)

    image1 = image[y1:y2, x1:x2]
    grey = np.empty((shape), dtype=np.int)
    ImageProcessing.View_images([image1])
    for row_idx ,row in enumerate(image1):
        for column_idx, item in enumerate(row):
            string = 'in row: {}, column {},  printed item is = {}'.format(row_idx, column_idx, item)
            print(string)
            grey.itemset((row_idx,column_idx), item)
    grey = np.uint8(grey)

    ImageProcessing.View_images([grey])
    """
    #test = [[1,2,3],[4,5,6,], [7,8,9]]
    #test = np.asanyarray(test, dtype= np.int)
    #for item in test:
    #    print(item)
    #    print(item.max())
    #ImageProcessing.__Prepare()

a = 1.4857142857142858
b = 1.5714285714285714
c = 1.775

q = 2.0

list = [a,b,c]

match = 1
result = None
for value in list:
    x,y = divmod(q, value)
    print('value {} tested \n x = {} y = {}'.format(value, x,y))
    if x == 1 or x == 0:
        if y < match:
            match = y
            result = value
print('object with value: {} is matched'.format(result))