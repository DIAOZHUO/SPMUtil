cimport numpy as np

cdef extern from "template_matching.h":
    void calc_NCC_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat)
    void calc_NCC_dim2(float *m_flat, int m_size[2], float *f_flat, int f_size[2], float *R_flat)
    void calc_SSD_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat)
    void calc_SAD_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat)


def c_calc_NCC_dim3(np.ndarray[float, ndim=1] m_flat, np.ndarray[int, ndim=1] m_size, np.ndarray[float, ndim=1] f_flat, np.ndarray[int, ndim=1] f_size, np.ndarray[float, ndim=1] R_flat):
    calc_NCC_dim3(&m_flat[0], &m_size[0], &f_flat[0], &f_size[0], &R_flat[0])

def c_calc_NCC_dim2(np.ndarray[float, ndim=1] m_flat, np.ndarray[int, ndim=1] m_size, np.ndarray[float, ndim=1] f_flat, np.ndarray[int, ndim=1] f_size, np.ndarray[float, ndim=1] R_flat):
    calc_NCC_dim2(&m_flat[0], &m_size[0], &f_flat[0], &f_size[0], &R_flat[0])

def c_calc_SSD_dim3(np.ndarray[float, ndim=1] m_flat, np.ndarray[int, ndim=1] m_size, np.ndarray[float, ndim=1] f_flat, np.ndarray[int, ndim=1] f_size, np.ndarray[float, ndim=1] R_flat):
    calc_SSD_dim3(&m_flat[0], &m_size[0], &f_flat[0], &f_size[0], &R_flat[0])

def c_calc_SAD_dim3(np.ndarray[float, ndim=1] m_flat, np.ndarray[int, ndim=1] m_size, np.ndarray[float, ndim=1] f_flat, np.ndarray[int, ndim=1] f_size, np.ndarray[float, ndim=1] R_flat):
    calc_SAD_dim3(&m_flat[0], &m_size[0], &f_flat[0], &f_size[0], &R_flat[0])
