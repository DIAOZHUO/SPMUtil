import numpy as np
from scipy import interpolate



def line_proline(map, xy_point_from, xy_point_to):
    length = int(np.hypot(xy_point_to[0] - xy_point_from[0], xy_point_to[1] - xy_point_from[1]))
    x, y = np.linspace(xy_point_from[0], xy_point_to[0], length), np.linspace(xy_point_from[1], xy_point_to[1], length)
    return map[x.astype(np.int), y.astype(np.int)]


def topo_map_correction(topo_map: np.ndarray, threshold=3):
    mean, std = np.mean(topo_map), np.std(topo_map)
    size = topo_map.shape
    threshold = threshold * std
    topo_map[abs(topo_map - mean) > threshold] = np.nan
    x, y = np.arange(0, size[1]), np.arange(0, size[0])
    array = np.ma.masked_invalid(topo_map)
    xx, yy = np.meshgrid(x, y)
    x1, y1 = xx[~array.mask], yy[~array.mask]
    return interpolate.griddata((x1, y1), array[~array.mask].ravel(), (xx, yy), method="cubic")


def calc_ncc(template, image, use_cython=False):
    if use_cython:
        import SPMUtil.cython_files.cython_calc_NCC as cython_calc_NCC
        F = template.numpy()[0].astype(np.float32)
        M = image.numpy()[0].astype(np.float32)
        ncc = np.zeros(
            (M.shape[1] - F.shape[1]) * (M.shape[2] - F.shape[2])).astype(np.float32)
        cython_calc_NCC.c_calc_NCC(M.flatten().astype(np.float32), np.array(M.shape).astype(
            np.int32), F.flatten().astype(np.float32), np.array(F.shape).astype(np.int32), ncc)
        ncc = ncc.reshape([M.shape[1] - F.shape[1], M.shape[2] - F.shape[2]])

    else:
        c, h_f, w_f = template.shape[-3:]
        tmp = np.zeros((c, image.shape[-2] - h_f, image.shape[-1] - w_f, h_f, w_f))
        for i in range(image.shape[-2] - h_f):
            for j in range(image.shape[-1] - w_f):
                M_tilde = image[:, :, i:i + h_f, j:j + w_f][:, None, None, :, :]
                tmp[:, i, j, :, :] = M_tilde / np.linalg.norm(M_tilde)
        ncc = np.sum(tmp * template.reshape(template.shape[-3], 1, 1, template.shape[-2], template.shape[-1]),
                     axis=(0, 3, 4))
    return ncc

