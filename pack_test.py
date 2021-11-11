import SPMUtil as spmu
from SPMUtil.DataSerializerPackage import DataSerializerPackage
from SPMUtil import NdarrayDecoder, NdarrayEncoder
import matplotlib.pyplot as plt
import json
import numpy as np

pack = DataSerializerPackage(path="./tio2_20211025")
pack.JsonEncoder = NdarrayEncoder
pack.JsonDecoder = NdarrayDecoder


# save test
# path = "./tio2_20211025"
# pack.save_from_folder(path)


# load test
pack.load()
print(pack.datas_name_list)
key = 'tio2_20211025_5'

data = pack.get_dataSerializer(key=key)
topo_map = spmu.flatten_map(data.data_dict['FWFW_ZMap'], spmu.FlattenMode.LinearFit)
param = json.loads(data.data_dict['Stage Param'], cls=NdarrayDecoder)
current_error_map = data.data_dict['FWFW_CurrentMap']-param["setpoint"]
# print(json.loads(data.data_dict['data_main_header'])["Time_Start_Scan"])



def time_string_to_sec(time_str: str):
    ftr = [3600, 60, 1]
    return sum([a * b for a, b in zip(ftr, map(int, time_str.split(':')))])

print(json.loads(data.data_dict['data_main_header'])["Time_Start_Scan"])
print(time_string_to_sec(json.loads(data.data_dict['data_main_header'])["Time_Start_Scan"]))

plt.imshow(spmu.formula.topo_map_correction(topo_map, threshold=5), cmap="afmhot")
plt.title(key)
plt.colorbar()
plt.show()
