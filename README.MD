SPMUtil (spmu)
===================================
Some Common method for SPM data analysis and realtime data processing.
<br>
Python version 3.* required.

Features
-------


- Image Processing and Flatten Method


- Experiment data IO
  (support Dulcinea file and Nanonis file and a speical intergrated file format(.pak) for common data)


- 3D visualization tool.
specially view tool for Nanonis Grid file


- Fomulas used in SPM
Like Df/F convert (sader-jarvis method and matrix method) and so on...




Installation
-------

this package runs in the environment of python 3.6:

* `pip install SPMUtil`

##### (optional) Cython support

To get better performance in realtime meansurement, 
please consider compiling cython script in "SPMUtil/cython_files".
Just go to this path, then

* `python cython_setup.py build_ext --inplace`

To enable cython script, type this at beginning.

```python
import SPMUtil as spmu
spmu.use_cython = True
```

