import serial
import cv2 as cv
import cython

def ConnParam(parameter):
    dict = {
        'Even': serial.PARITY_EVEN,
        'None': serial.PARITY_NONE,
        'Odd': serial.PARITY_ODD,
        'Mark': serial.PARITY_MARK,
        'Space': serial.PARITY_SPACE,
        '5': serial.FIVEBITS,
        '6': serial.SIXBITS,
        '7': serial.SEVENBITS,
        '8': serial.EIGHTBITS,
        '1': serial.STOPBITS_ONE,
        '1.5': serial.STOPBITS_ONE_POINT_FIVE,
        '2': serial.STOPBITS_TWO,

    }
    return dict[parameter]

def ActionOne(param):
    dict = {
        'pushButton': '1;1;JOG01;00;00;01;00'+'\r\n',
        'pushButton_2': '1;1;JOG01;00;01;00;00'+'\r\n',
        'pushButton_3': '1;1;JOG01;00;00;02;00'+'\r\n',
        'pushButton_4': '1;1;JOG01;00;02;00;00'+'\r\n',
        'pushButton_5': '1;1;JOG01;00;00;04;00'+'\r\n',
        'pushButton_6': '1;1;JOG01;00;04;00;00'+'\r\n',
        'pushButton_7': '1;1;JOG00;00;00;40;00'+'\r\n',
        'pushButton_8': '1;1;JOG00;00;40;00;00'+'\r\n',
        'pushButton_9': '1;1;JOG00;00;00;02;00'+'\r\n',
        'pushButton_10': '1;1;JOG00;00;02;00;00'+'\r\n',
        'pushButton_11': '1;1;JOG00;00;00;04;00'+'\r\n',
        'pushButton_14': '1;1;JOG00;00;04;00;00'+'\r\n',
        'pushButton_15': '1;1;JOG00;00;00;10;00'+'\r\n',
        'pushButton_16': '1;1;JOG00;00;10;00;00'+'\r\n',
        'pushButton_17': '1;1;JOG00;00;00;20;00'+'\r\n',
        'pushButton_18': '1;1;JOG00;00;20;00;00'+'\r\n',
    }
    return dict[param]

def CamCount():

    count = 0
    cam_index = []
    while True:

        cam = cv.VideoCapture(count)

        if cam.isOpened():
            cam.release()
            cam_index.append(count)
            count += 1
        else:
            break

    return cam_index







