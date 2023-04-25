import pandas as pd
import os,glob

def merge(_path, _out_path):
    os.chdir(_path)
    xlsx_files=glob.glob('*.xlsx')
    Day_list, Min_list, Max_list, Mean_list, Id_list, Shengqu_list = [],[],[],[],[],[]
    for xlsx_file in xlsx_files:
        filename=xlsx_file.split('.')[0]
        filename=filename[22:]
        day_list=[filename]*33 
        xlsx_name=f'{_path}'+xlsx_file
        df=pd.read_excel(xlsx_name)
        id=df['OBJECTID'].tolist()
        max=df['_max'].tolist()
        min=df['_min'].tolist()
        mean=df['_mean'].value().tolist()
        shengqu=df['省区'].tolist()

        Day_list.extend(day_list)            #日期列
        Id_list.extend(id)
        Min_list.extend(min)
        Max_list.extend(max)
        Mean_list.extend(mean)
        Shengqu_list.extend(shengqu)
    df_pro=pd.DataFrame({'Day':Day_list,'OBJECTID':Id_list,'province':Shengqu_list,'min':Min_list,'max':Max_list,'mean':Mean_list})
    outputfile_path = _out_path
    df_pro.to_excel(outputfile_path,index= False)
if __name__=='__main__':
    _path = r'D:\高级数据服务_数据\旱情监测-new\旱情监测省级统计'
    _out_path = r'D:\高级数据服务_数据\旱情监测-new\旱情监测省级统计.xlsx'
    merge(_path, _out_path)
    