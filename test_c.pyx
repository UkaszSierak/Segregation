import numpy as np
cimport numpy as np

DTYPE = np.int

ctypedef np.int_t DTYPE_t

cpdef ShadowReduce(np.ndarray[DTYPE_t, ndim=3] im, np.ndarray[DTYPE_t, ndim=2] gray_img):

    cdef int row_idx, column_idx
    cdef DTYPE_t max

    for row_idx ,row in enumerate(im):

        for column_idx, item  in enumerate(row):

            sum = 0
            max = item.max()

            for value in item:

                sum += max - value

            if sum > 255:

                gray_img.itemset((row_idx, column_idx), 255)

            else:

                gray_img.itemset((row_idx, column_idx), sum)

