from SPMUtil import NdarrayEncoder, NdarrayDecoder, DataSerializer
import json
from enum import Enum, auto
from datetime import datetime as dt
from copy import deepcopy
from typing import TypeVar
Cls = TypeVar('Cls')


class cache_1d_scope(Enum):
    Output_FW_ZLine = 1
    Output_BW_ZLine = 2
    Output_FW_CurrentLine = 3
    Output_BW_CurrentLine = 4
    Custom_1DSlot1 = 5
    Custom_1DSlot2 = 6
    LineProfile = 7
    Output_FW_DfLine = 8
    Output_BW_DfLine = 9
    Output_FW_AmpLine = 10
    Output_BW_AmpLine = 11


class cache_2d_scope(Enum):
    FWFW_ZMap = 1
    FWBW_ZMap = 2
    BWFW_ZMap = 3
    BWBW_ZMap = 4
    FWFW_CurrentMap = 5
    FWBW_CurrentMap = 6
    BWFW_CurrentMap = 7
    BWBW_CurrentMap = 8
    FF_XArray = 9
    FF_YArray = 10
    FF_ZArray = 11
    FF_CurrentArray = 12
    FF_ReadFlagArray = 13
    Custom_2DSlot1 = 14
    Custom_2DSlot2 = 15
    FWFW_DfMap = 16
    FWBW_DfMap = 17
    BWFW_DfMap = 18
    BWBW_DfMap = 19
    FWFW_AmpMap = 20
    FWBW_AmpMap = 21
    BWFW_AmpMap = 22
    BWBW_AmpMap = 23




class signal_type(Enum):
    Z = auto()
    Current = auto()
    Df = auto()
    Amp = auto()
    Phase = auto()
    Excitation = auto()


class JsonStringClass(object):
    def __str__(self):
        return self.to_json()


    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(self.__dict__, cls=NdarrayEncoder)

    def from_json(self, json_str):
        dict = json.loads(json_str, cls=NdarrayDecoder)
        for key in dict.keys():
            if key in self.__dict__:
                self.__setattr__(key, dict[key])

    @staticmethod
    def GetKeyName() -> str:
        raise NotImplementedError

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        raise NotImplementedError

    @staticmethod
    def copy_class(cls: Cls) -> Cls:
        copy_cls = type(f'{cls.__name__}Copy', cls.__bases__, dict(cls.__dict__))
        for name, attr in cls.__dict__.items():
            try:
                hash(attr)
            except TypeError:
                # Assume lack of __hash__ implies mutability. This is NOT
                # a bullet proof assumption but good in many cases.
                setattr(copy_cls, name, deepcopy(attr))
        return copy_cls


class StageConfigure(JsonStringClass):

    def __init__(self):
        super().__init__()
        self.Sample_Bias = 2
        self.Tube_Scanner_Offset_X = 0
        self.Tube_Scanner_Offset_Y = 0
        self.High_Speed_Scanner_Offset_X = 0
        self.High_Speed_Scanner_Offset_Y = 0
        self.Scan_Speed = 1000
        # 0: tube scanner, 1: hs scanner, 2: disabled
        self.XY_Scan_Option = 0
        self.Z_Scan_Option = 0
        self.setpoint = 0.01
        # labviewにはこれらの変数はないけど, ここはファイル保存のために使う
        self.drift_x = 0.0
        self.drift_y = 0.0
        self.drift_z = 0.0
        self.z_sum_offset = 0.0
        self.sys_x_tilt = 0.0
        self.sys_y_tilt = 0.0

    @staticmethod
    def GetKeyName() -> str:
        return "StageConfigure"

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        data = StageConfigure()
        if type(dataSerilizer.data_dict[data.GetKeyName()]) == str:
            data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        else:
            data = dataSerilizer.data_dict[data.GetKeyName()]
        return data


class PythonScanParam(JsonStringClass):
    def __init__(self):
        super().__init__()
        self.Aux1Pingpong = True
        self.Aux2Pingpong = False
        self.ZRotation = 0.0
        self.Aux1MinVoltage = 0.0
        self.Aux1MaxVoltage = 0.0
        self.Aux2MinVoltage = 0.0
        self.Aux2MaxVoltage = 0.0
        self.Aux1ScanSize = 5
        self.Aux2ScanSize = 5
        self.Xtilt = 0.0
        self.Ytilt = 0.0
        self.Applytilt = False
        """
        class AuxType(Enum):
            X = 1
            Y = 2
            Z = 3
            Current = 4
        """
        self.Aux1Type = "X"
        self.Aux2Type = "Y"
        self.XOffset = 0.0
        self.YOffset = 0.0
        self.ZOffset = 0.0
        self.LinesNumPerFlag = 1
        self.ZFeedbackOn = True
        self.AQBoost = False


    @property
    def Aux1DeltaVoltage(self):
        return (self.Aux1MaxVoltage - self.Aux1MinVoltage) / self.Aux1ScanSize

    @property
    def Aux2DeltaVoltage(self):
        return (self.Aux2MaxVoltage - self.Aux2MinVoltage) / self.Aux2ScanSize

    @staticmethod
    def GetKeyName() -> str:
        return "PythonScanParam"

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        data = PythonScanParam()
        data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        return data





class ScanDataHeader(JsonStringClass):
    def __init__(self):
        super().__init__()
        self.Date = ""
        self.Time_Start_Scan = ""
        self.Time_End_Scan = ""
        self.Scan_Method = ""
        self.Array_Builder = ""

    @property
    def Start_Scan_Sec(self) -> int:
        return self._time_string_to_sec(self.Time_Start_Scan)

    @property
    def End_Scan_Sec(self) -> int:
        return self._time_string_to_sec(self.Time_End_Scan)

    @property
    def Start_Scan_Timestamp(self) -> float:
        tdatetime = dt.strptime(self.Date + " " + self.Time_Start_Scan, '%Y-%m-%d %H:%M:%S')
        return tdatetime.timestamp()

    @property
    def End_Scan_Timestamp(self) -> float:
        tdatetime = dt.strptime(self.Date + " " + self.Time_End_Scan, '%Y-%m-%d %H:%M:%S')
        return tdatetime.timestamp()

    @staticmethod
    def GetKeyName() -> str:
        return "data_main_header"

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        data = ScanDataHeader()
        data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        return data

    def _time_string_to_sec(self, time_str: str):
        ftr = [3600, 60, 1]
        return sum([a * b for a, b in zip(ftr, map(int, time_str.split(':')))])



class HardwareConfigure(JsonStringClass):
    def __init__(self):
        super().__init__()
        self.hardware_name = ""
        # nm/V
        self.Tube_Scanner_X_Piezo_Calibration = 1.0
        self.Tube_Scanner_Y_Piezo_Calibration = 1.0
        self.Tube_Scanner_Z_Piezo_Calibration = 1.0
        self.HS_Scanner_X_Piezo_Calibration = 1.0
        self.HS_Scanner_Y_Piezo_Calibration = 1.0
        self.HS_Scanner_Z_Piezo_Calibration = 1.0
        self.Tube_Scanner_Voltage_Range_Min = -10.0
        self.Tube_Scanner_Voltage_Range_Max = 10.0
        self.HS_Scanner_Voltage_Range_Min = -10.0
        self.HS_Scanner_Voltage_Range_Max = 10.0
        self.software_version = "v0.0.1"

    @staticmethod
    def GetKeyName() -> str:
        return "HardwareConfigure"

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer):
        data = HardwareConfigure()
        data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        return data


