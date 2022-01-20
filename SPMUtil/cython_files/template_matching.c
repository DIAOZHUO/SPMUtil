#include "template_matching.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>


void calc_NCC_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat)
{
    // calc |F|
    float f_norm = 0.0;
    for (int i = 0; i < f_size[0] * f_size[1] * f_size[2]; i++)
    {
        f_norm += pow(f_flat[i], 2);
    }
    f_norm = sqrt(f_norm);

    // calc NCC
    for (int j = 0; j < m_size[1] - f_size[1]; j++)
    {
        for (int k = 0; k < m_size[2] - f_size[2]; k++)
        {
            float m_norm = 0.0;
            for (int i = 0; i < m_size[0]; i++)
            {
                for (int u = 0; u < f_size[1]; u++)
                {
                    for (int v = 0; v < f_size[2]; v++)
                    {
                        R_flat[j * (m_size[2] - f_size[2]) + k] += m_flat[i * m_size[1] * m_size[2] + (j + u) * m_size[2] + k + v] * f_flat[i * f_size[1] * f_size[2] + u * f_size[2] + v];
                        m_norm += pow(m_flat[i * m_size[1] * m_size[2] + (j + u) * m_size[2] + k + v], 2);
                    }
                }
            }
            R_flat[j * (m_size[2] - f_size[2]) + k] /= (f_norm * sqrt(m_norm));
        }
    }
}


void calc_SAD_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat)
{
    for (int j = 0; j < m_size[1] - f_size[1]; j++)
    {
        for (int k = 0; k < m_size[2] - f_size[2]; k++)
        {
            for (int i = 0; i < m_size[0]; i++)
            {
                for (int u = 0; u < f_size[1]; u++)
                {
                    for (int v = 0; v < f_size[2]; v++)
                    {
                        R_flat[j * (m_size[2] - f_size[2]) + k] += fabsf(m_flat[i * m_size[1] * m_size[2] + (j + u) * m_size[2] + k + v] - f_flat[i * f_size[1] * f_size[2] + u * f_size[2] + v]);
                    }
                }
            }
        }
    }
}


void calc_SSD_dim3(float *m_flat, int m_size[3], float *f_flat, int f_size[3], float *R_flat)
{
    for (int j = 0; j < m_size[1] - f_size[1]; j++)
    {
        for (int k = 0; k < m_size[2] - f_size[2]; k++)
        {
            for (int i = 0; i < m_size[0]; i++)
            {
                for (int u = 0; u < f_size[1]; u++)
                {
                    for (int v = 0; v < f_size[2]; v++)
                    {
                        R_flat[j * (m_size[2] - f_size[2]) + k] += pow(m_flat[i * m_size[1] * m_size[2] + (j + u) * m_size[2] + k + v] - f_flat[i * f_size[1] * f_size[2] + u * f_size[2] + v], 2);
                    }
                }
            }
        }
    }
}





void calc_NCC_dim2(float *m_flat, int m_size[2], float *f_flat, int f_size[2], float *R_flat)
{
    // calc |F|
    float f_norm = 0.0;
    for (int i = 0; i < f_size[0] * f_size[1]; i++)
    {
        f_norm += pow(f_flat[i], 2);
    }
    f_norm = sqrt(f_norm);

    // calc NCC
    for (int j = 0; j < m_size[0] - f_size[0]; j++)
    {
        for (int k = 0; k < m_size[1] - f_size[1]; k++)
        {
            float m_norm = 0.0;
            for (int i = 0; i < m_size[0]; i++)
            {
                for (int u = 0; u < f_size[1]; u++)
                {
                    R_flat[j * (m_size[1] - f_size[1]) + k] += m_flat[(i + j) * m_size[1] + u + k] * f_flat[i * f_size[1] + u];
                    m_norm += pow(m_flat[(i + j) * m_size[1] + u + k], 2);
                }
            }
            R_flat[j * (m_size[1] - f_size[1]) + k] /= (f_norm * sqrt(m_norm));
        }
    }
}

