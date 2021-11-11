from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy as np

# 1. install compiler
# https://www.mingw-w64.org/downloads/
# 2. pip install Cython

sourcefiles = ['cython_pyx_code.pyx', 'cython_calc_NCC.c']

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("cython_calc_NCC", sourcefiles,
                           include_dirs=[np.get_include()])],
)
# python setup.py build_ext - -inplace - f

