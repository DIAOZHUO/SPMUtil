from __future__ import annotations
from SPMUtil import NdarrayEncoder, NdarrayDecoder, DataSerializer
import json
from enum import Enum, auto, IntEnum
from datetime import datetime as dt
from copy import deepcopy
from typing import TypeVar
from functools import cache

Cls = TypeVar('Cls')


class SignalAIType(IntEnum):
    none = 0
    Z = 1
    Current = 2
    Df = 3
    Amp = 4
    Excitation = 5
    CPD = 6


class SignalAOType(IntEnum):
    const = 0
    Z = 1
    Vs = 2
    Tube_X = 3
    Tube_Y = 4
    HS_X = 5
    HS_Y = 6



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
    Output_FW_ExcitationLine = 12
    Output_BW_ExcitationLine = 13
    Output_FW_CPDLine = 14
    Output_BW_CPDLine = 15

    @staticmethod
    @cache
    def from_signal_type(signal_type: SignalAIType, aux1_fw_bw: bool) -> cache_1d_scope:
        _signal_lookup_dict = {
            (SignalAIType.Z, True): cache_1d_scope.Output_FW_ZLine,
            (SignalAIType.Z, False): cache_1d_scope.Output_BW_ZLine,
            (SignalAIType.Current, True): cache_1d_scope.Output_FW_CurrentLine,
            (SignalAIType.Current, False): cache_1d_scope.Output_BW_CurrentLine,
            (SignalAIType.Df, True): cache_1d_scope.Output_FW_DfLine,
            (SignalAIType.Df, False): cache_1d_scope.Output_BW_DfLine,
            (SignalAIType.Amp, True): cache_1d_scope.Output_FW_AmpLine,
            (SignalAIType.Amp, False): cache_1d_scope.Output_BW_AmpLine,
            (SignalAIType.Excitation, True): cache_1d_scope.Output_FW_ExcitationLine,
            (SignalAIType.Excitation, False): cache_1d_scope.Output_FW_ExcitationLine,
            (SignalAIType.CPD, True): cache_1d_scope.Output_FW_CPDLine,
            (SignalAIType.CPD, False): cache_1d_scope.Output_BW_CPDLine,
        }
        return _signal_lookup_dict[(signal_type, aux1_fw_bw)]



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
    FWFW_ExcitationMap = 24
    FWBW_ExcitationMap = 25
    BWFW_ExcitationMap = 26
    BWBW_ExcitationMap = 27
    FWFW_CPDMap = 28
    FWBW_CPDMap = 29
    BWFW_CPDMap = 30
    BWBW_CPDMap = 31


    @staticmethod
    @cache
    def from_signal_type(signal_type: SignalAIType, aux1_fw_bw: bool, aux2_fw_bw: bool) -> cache_2d_scope:
        _signal_lookup_dict = {
            (SignalAIType.Z, True, True): cache_2d_scope.FWFW_ZMap,
            (SignalAIType.Z, False, True): cache_2d_scope.BWFW_ZMap,
            (SignalAIType.Z, True, False): cache_2d_scope.FWBW_ZMap,
            (SignalAIType.Z, False, False): cache_2d_scope.BWBW_ZMap,
            (SignalAIType.Current, True, True): cache_2d_scope.FWFW_CurrentMap,
            (SignalAIType.Current, False, True): cache_2d_scope.BWFW_CurrentMap,
            (SignalAIType.Current, True, False): cache_2d_scope.FWBW_CurrentMap,
            (SignalAIType.Current, False, False): cache_2d_scope.BWBW_CurrentMap,
            (SignalAIType.Df, True, True): cache_2d_scope.FWFW_DfMap,
            (SignalAIType.Df, False, True): cache_2d_scope.BWFW_DfMap,
            (SignalAIType.Df, True, False): cache_2d_scope.FWBW_DfMap,
            (SignalAIType.Df, False, False): cache_2d_scope.BWBW_DfMap,
            (SignalAIType.Amp, True, True): cache_2d_scope.FWFW_AmpMap,
            (SignalAIType.Amp, False, True): cache_2d_scope.BWFW_AmpMap,
            (SignalAIType.Amp, True, False): cache_2d_scope.FWBW_AmpMap,
            (SignalAIType.Amp, False, False): cache_2d_scope.BWBW_AmpMap,
            (SignalAIType.Excitation, True, True): cache_2d_scope.FWFW_ExcitationMap,
            (SignalAIType.Excitation, False, True): cache_2d_scope.BWFW_ExcitationMap,
            (SignalAIType.Excitation, True, False): cache_2d_scope.FWBW_ExcitationMap,
            (SignalAIType.Excitation, False, False): cache_2d_scope.BWBW_ExcitationMap,
            (SignalAIType.CPD, True, True): cache_2d_scope.FWFW_CPDMap,
            (SignalAIType.CPD, False, True): cache_2d_scope.BWFW_CPDMap,
            (SignalAIType.CPD, True, False): cache_2d_scope.FWBW_CPDMap,
            (SignalAIType.CPD, False, False): cache_2d_scope.BWBW_CPDMap,
        }
        return _signal_lookup_dict[(signal_type, aux1_fw_bw, aux2_fw_bw)]





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
    def from_dataSerilizer(dataSerilizer: DataSerializer) -> StageConfigure:
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
    def from_dataSerilizer(dataSerilizer: DataSerializer) -> PythonScanParam:
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
    def from_dataSerilizer(dataSerilizer: DataSerializer) -> ScanDataHeader:
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
        # piezo calibration (nm/V)
        self.Tube_Scanner_X_Piezo_Calibration = 1.0
        self.Tube_Scanner_Y_Piezo_Calibration = 1.0
        self.Tube_Scanner_Z_Piezo_Calibration = 1.0
        self.HS_Scanner_X_Piezo_Calibration = 1.0
        self.HS_Scanner_Y_Piezo_Calibration = 1.0
        self.HS_Scanner_Z_Piezo_Calibration = 1.0
        # Voltage Range (V)
        self.Tube_Scanner_Voltage_Range_Min = -10.0
        self.Tube_Scanner_Voltage_Range_Max = 10.0
        self.HS_Scanner_Voltage_Range_Min = -10.0
        self.HS_Scanner_Voltage_Range_Max = 10.0
        self.software_version = "v0.0.1"
        # input channel
        self.SignalAIType_AI0 = SignalAIType.none
        self.SignalAIType_AI1 = SignalAIType.none
        self.SignalAIType_AI2 = SignalAIType.none
        self.SignalAIType_AI3 = SignalAIType.none
        self.SignalAIType_AI4 = SignalAIType.none
        self.SignalAIType_AI5 = SignalAIType.none
        self.SignalAIType_AI6 = SignalAIType.none
        self.SignalAIType_AI7 = SignalAIType.none

        # output channel
        self.SignalAOType_AO0 = SignalAOType.const
        self.const_AO0 = 0.0
        self.SignalAOType_AO1 = SignalAOType.const
        self.const_AO1 = 0.0
        self.SignalAOType_AO2 = SignalAOType.const
        self.const_AO2 = 0.0
        self.SignalAOType_AO2 = SignalAOType.const
        self.const_AO2 = 0.0
        self.SignalAOType_AO3 = SignalAOType.const
        self.const_AO3 = 0.0
        self.SignalAOType_AO4 = SignalAOType.const
        self.const_AO4 = 0.0
        self.SignalAOType_AO5 = SignalAOType.const
        self.const_AO5 = 0.0
        self.SignalAOType_AO6 = SignalAOType.const
        self.const_AO6 = 0.0
        self.SignalAOType_AO7 = SignalAOType.const
        self.const_AO7 = 0.0

        self.Feedback_Signal = SignalAIType.Current


    @staticmethod
    def GetKeyName() -> str:
        return "HardwareConfigure"

    @staticmethod
    def from_dataSerilizer(dataSerilizer: DataSerializer) -> HardwareConfigure:
        data = HardwareConfigure()
        data.from_json(dataSerilizer.data_dict[data.GetKeyName()])
        return data


if __name__ == '__main__':
    print(cache_1d_scope.from_signal_type(SignalAIType.Z, False))
    print(cache_2d_scope.from_signal_type(SignalAIType.Current, True, True))