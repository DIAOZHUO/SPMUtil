import subprocess
import sys


def get_latest_version(package):
    result = subprocess.run(
        [sys.executable, "-m", "pip", "index", "versions", package],
        capture_output=True,
        text=True
    )
    lines = result.stdout.splitlines()
    for line in lines:
        if "Available versions:" in line:
            versions = line.split(":")[1].strip().replace(" ", "").split(",")
            return versions[0]
    return None


def _check(name):
    try:
        latest_version = get_latest_version("SPMUtil")

        current_version = str(
            subprocess.run([sys.executable, '-m', 'pip', 'show', '{}'.format(name)], capture_output=True, text=True))
        current_version = current_version[current_version.find('Version:') + 8:]
        current_version = current_version[:current_version.find('\\n')].replace(' ', '')
        if latest_version == current_version:
            return True
        else:
            print(
                '\033[93m' + f"SPMUtil({current_version}) is not in the latest version({latest_version}). Please consider updating it by 'pip install spmutil -U'" + '\033[0m')
            return False
    except:
        import traceback
        traceback.print_exc()


_check("SPMUtil")

import SPMUtil.structures._structures as structures

import SPMUtil.nanonispy as nanonispy
import SPMUtil.converter as converter

from SPMUtil.DataSerializer import DataSerializer, NdarrayDecoder, NdarrayEncoder
from SPMUtil.structures.rect_2d import Rect2D
from SPMUtil.structures.scan_data_format import cache_1d_scope, cache_2d_scope, SignalAIType, SignalAOType, \
    ScanDataHeader, \
    StageConfigure, PythonScanParam, HardwareConfigure, JsonStringClass

from SPMUtil.DataInspector import DataInspector
from SPMUtil.DataSerializerPackage import DataSerializerPackage

import SPMUtil.formula as formula
import SPMUtil.analyzer as analyzer

from SPMUtil.flatten import *
from SPMUtil.filters import filter_1d, filter_2d

from SPMUtil.gui import Rect2DSelector, NanonisGridVisualizer, TiltCalculator, LineSelector, JsonEditor, PointSelector

use_cython = False


