#ifndef CYTHON_CODE
#define CYTHON_CODE
void calc_NCC_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat);
void calc_NCC_dim2(float *m_flat, int m_size[2], float *f_flat, int f_size[2], float *R_flat);
void calc_SSD_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat);
void calc_SAD_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat);
#endif