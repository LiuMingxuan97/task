from osgeo import gdal
import  numpy as np
import os,glob

def statistics(_path):
    os.chdir(_path)
    tif_files=glob.glob('*.tif')
    result = []
    for tif_file in tif_files:
        dataset=gdal.Open(tif_file)
        band1=dataset.GetRasterBand(1).ReadAsArray()
        arr_max = np.nanmax(band1)
        arr_min =np.nanmin(band1)
        arr_mean = np.nanmean(band1)
        _dict = {'最大值':arr_max, '最小值':arr_min, '平均值':arr_mean}
        result.append(_dict)
    return result
