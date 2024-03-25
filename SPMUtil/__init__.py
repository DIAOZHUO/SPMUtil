import subprocess
import sys
def _check(name):
    try:
        latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', '{}==random'.format(name)], capture_output=True, text=True))
        latest_version = latest_version[latest_version.find('(from versions:')+15:]
        latest_version = latest_version[:latest_version.find(')')]
        latest_version = latest_version.replace(' ','').split(',')[-1]

        current_version = str(subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(name)], capture_output=True, text=True))
        current_version = current_version[current_version.find('Version:')+8:]
        current_version = current_version[:current_version.find('\\n')].replace(' ','')
        if latest_version == current_version:
            return True
        else:
            print('\033[93m' + "SPMUtil is not in the latest version. Please consider updating it by 'pip install spmutil -U'" + '\033[0m')
            return False
    except:
        pass
_check("SPMUtil")

import SPMUtil.structures._structures as structures


import SPMUtil.nanonispy as nanonispy
import SPMUtil.converter as converter

from SPMUtil.DataSerializer import DataSerializer, NdarrayDecoder, NdarrayEncoder
from SPMUtil.structures.rect_2d import Rect2D
from SPMUtil.structures.scan_data_format import cache_1d_scope, cache_2d_scope, SignalAIType, SignalAOType, ScanDataHeader, \
    StageConfigure, PythonScanParam, HardwareConfigure, JsonStringClass


from SPMUtil.DataInspector import DataInspector
from SPMUtil.DataSerializerPackage import DataSerializerPackage



import SPMUtil.formula as formula
import SPMUtil.analyzer as analyzer

from SPMUtil.flatten import *
from SPMUtil.filters import filter_1d, filter_2d

from SPMUtil.gui import Rect2DSelector, NanonisGridVisualizer, TiltCalculator, LineSelector, JsonEditor, PointSelector


use_cython = False


