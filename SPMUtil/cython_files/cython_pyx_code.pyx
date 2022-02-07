import numpy as np
cimport numpy as np
np.import_array()
cimport cython
from cython.parallel cimport prange
ctypedef np.float64_t DTYPE_t


@cython.boundscheck(False)
@cython.wraparound(False)
def convolve2d(np.ndarray[double, ndim=2] f, np.ndarray[double, ndim=2] g, int rim):
    cdef:
        ssize_t vmax, wmax, smax, tmax, smid, tmid, xmax, ymax
        ssize_t s_from, s_to, t_from, t_to
        ssize_t x, y, s, t, v, w
        float value
        np.ndarray[double, ndim=2] h
    # f is an image and is indexed by (v, w)
    # g is a filter kernel and is indexed by (s, t),
    #   it needs odd dimensions
    # h is the output image and is indexed by (x, y),
    #   it is not cropped
    if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
        raise ValueError("Only odd dimensions on filter supported")
    # smid and tmid are number of pixels between the center pixel
    # and the edge, ie for a 5x5 filter they will be 2.
    #
    # The output size is calculated by adding smid, tmid to each
    # side of the dimensions of the input image.
    vmax = f.shape[0]
    wmax = f.shape[1]
    smax = g.shape[0]
    tmax = g.shape[1]
    smid = smax // 2
    tmid = tmax // 2
    xmax = vmax + 2 * smid
    ymax = wmax + 2 * tmid
    # Allocate result image.
    h = np.zeros([xmax-rim*2, ymax-rim*2], dtype=f.dtype)
    # Do convolution
    for x in range(rim, xmax-rim):
        for y in range(rim, ymax-rim):
            # Calculate pixel value for h at (x,y). Sum one component
            # for each pixel (s, t) of the filter g.
            s_from = max(smid - x, -smid)
            s_to = min((xmax - x) - smid, smid + 1)
            t_from = max(tmid - y, -tmid)
            t_to = min((ymax - y) - tmid, tmid + 1)
            value = 0
            for s in range(s_from, s_to):
                for t in range(t_from, t_to):
                    v = x - smid + s
                    w = y - tmid + t
                    value += g[smid - s, tmid - t] * f[v, w]
            h[x-rim, y-rim] = value
    return h


@cython.boundscheck(False)
@cython.wraparound(False)
def convolve2d_tuned(np.ndarray[double, ndim=2, mode='c'] f, np.ndarray[double, ndim=2, mode='c'] g, int rim):
    cdef:
        ssize_t vmax, wmax, smax, tmax, smid, tmid, xmax, ymax
        ssize_t s_from, s_to, t_from, t_to
        ssize_t x, y, s, t, v, w
        float value
        np.ndarray[double, ndim=2] h
    # f is an image and is indexed by (v, w)
    # g is a filter kernel and is indexed by (s, t),
    #   it needs odd dimensions
    # h is the output image and is indexed by (x, y),
    #   it is not cropped
    if g.shape[0] % 2 != 1 or g.shape[1] % 2 != 1:
        raise ValueError("Only odd dimensions on filter supported")
    # smid and tmid are number of pixels between the center pixel
    # and the edge, ie for a 5x5 filter they will be 2.
    #
    # The output size is calculated by adding smid, tmid to each
    # side of the dimensions of the input image.
    vmax = f.shape[0]
    wmax = f.shape[1]
    smax = g.shape[0]
    tmax = g.shape[1]
    smid = smax // 2
    tmid = tmax // 2
    xmax = vmax + 2*smid
    ymax = wmax + 2*tmid
    # Allocate result image.
    h = np.zeros([xmax-rim*2, ymax-rim*2], dtype=f.dtype)
    # Do convolution
    with nogil:
        for x in prange(rim, xmax-rim, schedule='static'):
            for y in range(rim, ymax-rim):
                # Calculate pixel value for h at (x,y). Sum one component
                # for each pixel (s, t) of the filter g.
                s_from = max(smid - x, -smid)
                s_to = min((xmax - x) - smid, smid + 1)
                t_from = max(tmid - y, -tmid)
                t_to = min((ymax - y) - tmid, tmid + 1)
                value = 0
                for s in range(s_from, s_to):
                    for t in range(t_from, t_to):
                        v = x - smid + s
                        w = y - tmid + t
                        value = value + g[smid - s, tmid - t] * f[v, w]
                h[x-rim, y-rim] = value
    return h



cpdef inline np.ndarray[DTYPE_t, ndim=2] flatten_map_average_c(np.ndarray[DTYPE_t, ndim=2] map2d):
    cdef int size1 = map2d.shape[0]
    cdef int size2 = map2d.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=1] col_ave
    cdef np.ndarray[DTYPE_t, ndim=1] row_ave
    map2d -= np.nanmean(map2d, dtype=map2d.dtype)
    col_ave = np.nanmean(map2d, axis=0, dtype=map2d.dtype)
    row_ave = np.nanmean(map2d, axis=1, dtype=map2d.dtype)
    map2d -= np.tile(col_ave, (size1, 1)) + np.tile(np.array([row_ave]).transpose(), (1, size2), dtype=map2d.dtype)
    return map2d


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inline np.ndarray[DTYPE_t, ndim=2] \
        rotate_array(np.ndarray[DTYPE_t, ndim=1] array_x, np.ndarray[DTYPE_t, ndim=1] array_y, np.ndarray[DTYPE_t, ndim=1] rot_mat):
    cdef int size = len(array_x)
    cdef np.ndarray[DTYPE_t, ndim=1] ax = np.empty(size)
    cdef np.ndarray[DTYPE_t, ndim=1] ay = np.empty(size)
    for i in range(0, size):
        ax[i] = rot_mat[0] * array_x[i] + rot_mat[1] * array_y[i] + rot_mat[2]
        ay[i] = rot_mat[3] * array_x[i] + rot_mat[4] * array_y[i] + rot_mat[5]
    return np.vstack([ax, ay])







@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inline (double, double) get_flatten_param_linear(np.ndarray[DTYPE_t, ndim=2] map2d):
    cdef int size1 = map2d.shape[0]
    cdef int size2 = map2d.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=1] array_x = np.linspace(0, size1, size2)
    cdef np.ndarray[DTYPE_t, ndim=1] array_y = np.linspace(0, size1, size2)
    cdef double result_x
    cdef double result_y
    cdef double coef_x = 0.0
    cdef double coef_y = 0.0
    for i in range(0, size2):
        coef = np.polyfit(array_x, map2d[:, i], 1)
        coef_x += coef[0]
    for i in range(0, size1):
        coef = np.polyfit(array_y, map2d[i], 1)
        coef_y += coef[0]
    result_x = np.array(coef_x/size2)
    result_y = np.array(coef_y/size1)
    return result_x, result_y




@cython.boundscheck(False)
@cython.wraparound(False)
cpdef inline np.ndarray[DTYPE_t, ndim=2] get_flatten_param_poly(np.ndarray[DTYPE_t, ndim=2] map2d, int poly_fit_order):
    cdef int size1 = map2d.shape[0]
    cdef int size2 = map2d.shape[1]
    cdef np.ndarray[DTYPE_t, ndim=1] array_x = np.linspace(0, size1, size2)
    cdef np.ndarray[DTYPE_t, ndim=1] array_y = np.linspace(0, size1, size2)

    cdef np.ndarray[DTYPE_t, ndim=1] coef_x = np.polyfit(array_x, map2d[:, 0], poly_fit_order)
    cdef np.ndarray[DTYPE_t, ndim=1] coef_y = np.polyfit(array_y, map2d[0], poly_fit_order)

    cdef np.ndarray[DTYPE_t, ndim=2] result = np.empty(shape=(2, poly_fit_order+1))

    for i in range(1, size2):
        coef_x += np.polyfit(array_x, map2d[:, i], poly_fit_order)
    for i in range(1, size1):
        coef_y += np.polyfit(array_y, map2d[i], poly_fit_order)
    result[0] = np.array(coef_x/size2)
    result[1] = np.array(coef_y/size1)
    return result

