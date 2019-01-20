import numpy as np
cimport numpy as np

DTYPE = np.int

ctypedef np.int_t DTYPE_t

cpdef ShadowReduce(np.ndarray[DTYPE_t, ndim=3] im, np.ndarray[DTYPE_t, ndim=2] gray_img, int y1, int x1, int y2, int x2):

    cdef int  sum,rows, cols
    cdef DTYPE_t max, pix,
    for cols in range(x1,x2):
        for rows in range(y1,y2):
            sum = 0
            max = im[rows][cols][im[rows][cols].argmax(0)]
            for cell in range(3):
                pix = im.item(rows,cols,cell)
                sum += max - pix
            if sum > 255:
                gray_img.itemset((rows,cols), 255)
            else:

                gray_img.itemset((rows,cols), sum)
