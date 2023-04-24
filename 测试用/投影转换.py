import math

# 卫星地固系下的坐标
satellite_x = 1005644.8570433102 # 卫星x坐标
satellite_y = -5092639.160816824 # 卫星y坐标
satellite_z = -3694078.293271559 # 卫星z坐标


# 地球椭球体模型参数
earth_equatorial_radius = 6378137.0 # 地球赤道半径，单位：米
earth_flattening = 1 / 298.257223563 # 地球扁率

# 传感器参数
sensor_fov = math.radians(0.1) # 传感器视场角，单位：弧度
sensor_width = 7920 # 传感器像素宽度
sensor_height = 7920 # 传感器像素高度

# 目标像素坐标
target_pixel_x = 1 # 目标像素x坐标
target_pixel_y = 1 # 目标像素y坐标

# 计算卫星到地球中心的距离
satellite_distance = math.sqrt(satellite_x**2 + satellite_y**2 + satellite_z**2)

# 计算卫星在地球椭球体上的经纬度
latitude = math.asin(satellite_z / satellite_distance) # 纬度，单位：弧度
longitude = math.atan2(satellite_y, satellite_x) # 经度，单位：弧度

# 将经纬度转换为角度
latitude_deg = math.degrees(latitude) # 纬度，单位：度
longitude_deg = math.degrees(longitude) # 经度，单位：度

# 计算地面点的坐标
ground_point_latitude = latitude_deg + math.degrees(sensor_fov/2.0) - (target_pixel_y / sensor_height) * math.degrees(sensor_fov) # 地面点纬度，单位：度
ground_point_longitude = longitude_deg + (target_pixel_x / sensor_width) * math.degrees(sensor_fov) # 地面点经度，单位：度

# 计算地面点的高度
ground_point_height = earth_equatorial_radius * math.cos(math.radians(ground_point_latitude)) # 地面点高度，单位：米

# # 输出地面点坐标
# print("地面点坐标：")
# print("纬度：", ground_point_latitude)
# print("经度：", ground_point_longitude)
# print("高度：", ground_point_height)

import pymap3d as pm

x,y,z = pm.geodetic2ecef(-41.45474475,-78.78,1)
print(x,y,z)
lat,lon,alt = pm.ecef2geodetic(x,y,z)
print(lat,lon,alt)


import math

latitude = math.asin(-3694078.293271559/satellite_distance)
latitude_deg = math.degrees(latitude) 
print(latitude_deg)
