import time

import SPMUtil as spmu
from SPMUtil.DataSerializerPackage import DataSerializerPackage
from SPMUtil import NdarrayDecoder, NdarrayEncoder
import matplotlib.pyplot as plt
import json
import numpy as np

pack = DataSerializerPackage(path="./tio2_20211025")


# save test
# path = "./tio2_20211025"
# pack.save_from_folder(path)


# load test
pack.load()
print(pack.datas_name_list)
key = 'tio2_20211025_1-new'

data = pack.get_dataSerializer(key=key)

# extract data serializer pack to data serializer
# pack.extract_to_folder("./")



config = spmu.StageConfigure.from_dataSerilizer(data)
header = spmu.ScanDataHeader.from_dataSerilizer(data)
param = spmu.PythonScanParam.from_dataSerilizer(data)

topo_map = data.data_dict[spmu.cache_2d_scope.FWFW_ZMap.name]

plt.show()






"""
spmu.use_cython = False
t = time.time()
for i in range(3):
    # flatten_c.get_flatten_param_poly(topo_map, poly_fit_order=3)
    # sample.get_flatten_param_linear(topo_map)
    map1 = spmu.filter_2d.GaussianHannMap(topo_map, 15, 1, 1)
t1 = time.time()
print("dt:", t1-t)
print(map1.shape)
plt.imshow(map1)
plt.show()

spmu.use_cython = True
t = time.time()
for i in range(3):
    map1 = spmu.filter_2d.GaussianHannMap(topo_map, 15, 1, 1)
    # spmu.get_flatten_param(topo_map, spmu.FlattenMode.PolyFit, poly_fit_order=3)
    # spmu.get_flatten_param(topo_map, spmu.FlattenMode.LinearFit, poly_fit_order=3)

    # print(111)
t1 = time.time()
print("dt:", t1-t)
print(map1.shape)
plt.imshow(map1)
plt.show()
"""


# map = spmu.filter_2d.GaussianHannMap(topo_map, kernel_size=5, sigma_x=3, sigma_y=3)
# print(map.shape)
# map = spmu.formula.topo_map_correction(topo_map, threshold=5)
# # plt.imshow(map, cmap="afmhot")
# # plt.title(key)
# # plt.colorbar()
# # plt.show()
# rect = spmu.Rect2DSelector().select_rect(map)
# print(rect)
# plt.imshow(rect.extract_2d_map_from_rect(map))
# plt.show()
