import pandas as pd
import numpy as np
from random import random
from osgeo import gdal
import  numpy as np
import os,glob
import pandas as pd
def statistics(_path, out_xlsx, ):
    kind=5                           #重分类的类别数，通常重分类从1开始
    pixel_len=3323.2033193           #像元长度
    os.chdir(r'D:\高级数据服务_数据\旱情评估\转Albert计算面积')
    tif_files=glob.glob('*.tif')
    Day_list=[]
    Area_list=[]
    Value_list=[]
    Than_list=[]
    for tif_file in tif_files:
        dataset=gdal.Open(tif_file)
        band1=dataset.GetRasterBand(1).ReadAsArray()
        area_list=[]               #存放不同种类像元的面积
        than_list=[]               #存放不同种类像元的面积占比
        day_list=[]
        for i in range(1,kind+1):
            num=len(band1[band1==i])
            area=num*pixel_len*pixel_len/1000000/10000
            than=area/960
            area_list.append(int(area))
            than_list.append(than)
            day=tif_file.split('.')[0]
            day_list.append(day)
            value_list=list(range(1,kind+1))
        area_list[4]=960-sum(area_list)
        than_list[4]=1-sum(than_list)
        Than_list.extend(than_list)
        Day_list.extend(day_list)    
        Area_list.extend(area_list)
        Value_list.extend(value_list)
    df=pd.DataFrame({'day':Day_list,'value':Value_list,'area':Area_list,'than':Than_list})
    df.to_csv(out_xlsx,index=False)
    
if __name__=='__main__':
    statistics(_path=r'D:\高级数据服务_数据\旱情评估\转Albert计算面积', out_xlsx=r"D:\高级数据服务_数据\旱情评估\转Albert计算面积\全国旱情分五类面积及占比.csv")