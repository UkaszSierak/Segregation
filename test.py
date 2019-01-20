
import test_c
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time

def Shadow(img,):
    im = np.asanyarray(img, dtype = np.int)
    rows, cols, a = im.shape
    t = time.process_time()
    gray = test_c.ShadowReduce(im,rows,cols)
    elapsed_time = time.process_time() - t

    print('Czas operacji: ' + str(elapsed_time))
    return gray



