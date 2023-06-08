import numpy as np
import sqlite3
import json
import os
import shutil
import matplotlib.pyplot as plt


def show_imagetime(attrs_path: str, line_header_id: str = "3eb0903eb090"):
    """
    插值操作
    :param attrs_path: 辅助数据sqlite路径
    :param line_header_id: 行头标识
    :return:
    """
    with sqlite3.connect(attrs_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT row, attrs FROM image_attrs")
        rows = cursor.fetchall()

        # 从数据库中取出x、y、z位置, vx、vy、vz速度, q0 q1 q2 q3四元数
        time, utc, utc_int = [], [], []  # 数据格式：(行号, 成像时间, 辅助数据)
        UTC_list, UTCint_list = [], []
        for item in rows:
            row = item[0]
            attrs = json.loads(item[1])
            if attrs["LineHeader"] == line_header_id:
                time.append(attrs["ImagingTime"])
                UTCint_value = attrs["UTCInt"]
                UTC_value = attrs["UTC"]
                
                if UTC_value not in UTC_list:  # 取出要插值的数,组成列表
                    UTC_list.append(UTC_value)
                    
                if UTCint_value not in UTCint_list:
                    UTCint_list.append(attrs["UTCInt"])
                    
                utc.append(attrs["UTC"])
                utc_int.append(attrs["UTCInt"])
                
        #tiaobiao 记录发生变化的第i行
        #change_value 记录跳变时变了多少秒，向下跳变取正，向上跳变取负     
        tiaobian, change_value = [], []
        for i in range(1,len(time)):
            if time[i] <= time[i-1]:
                tiaobian.append(i)
                m = round(time[i-1] - time[i],1)
                change_value.append(m)
            elif time[i] - time[i-1] > 0.5:
                tiaobian.append(i)
                m = -round(time[i] - time[i-1],1)
                change_value.append(m)
        new_change = []
        sum_value = 0
        for index in change_value:
            sum_value = sum_value + index
            new_change.append(sum_value)
        #new_chane 为需要补的秒数
        #tiaobian  为发生变化时列表的索引
        
        #将time列表的每个跳变区域与new_change相加
        for i in range(len(tiaobian)-1):
            time1 = time[tiaobian[i] : tiaobian[i+1]]
            new_time = [x + new_change[i] for x in time1]
            time[tiaobian[i] : tiaobian[i+1]] = new_time
            
            
              
                
              

            
        # print(tiaobian)
        x = range(len(time))
        # x1 =range(28)
        
        plt.plot(x, time, label='time')
        plt.plot(x, utc, label='UTC')
        plt.plot(x, utc_int, label='UTCInt')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('List Plot')
        plt.show()
            

            
if __name__=="__main__":
  sqlit_path = r"D:\correction\1B_425_test\TQ1_CH2_100.0Mbps_1200.00MHz_20230103191023_tmp-PAN.sqlite"
  show_imagetime(sqlit_path)