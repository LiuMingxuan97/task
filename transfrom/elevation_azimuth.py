import numpy as np
import math
import pymap3d as pm

# # 卫星直角坐标
# satellite_xyz = np.array([1234567.89, 2345678.90, 3456789.01])

# # 测站直角坐标
# station_xyz = np.array([2345678.90, 3456789.01, 4567890.12])

# # WGS84椭球参数
# semi_major_axis = 6378137.0
# flattening = 1 / 298.257223563
# semi_minor_axis = semi_major_axis * (1 - flattening)

# # 计算测站地心距离
# station_range = np.linalg.norm(station_xyz)

# # 计算测站的地心经纬度
# latitude = np.arcsin(station_xyz[2] / station_range)
# longitude = np.arctan2(station_xyz[1], station_xyz[0])

# # 计算卫星相对于测站的位置矢量
# satellite_rel_xyz = satellite_xyz - station_xyz

# # 计算卫星的地心距离
# satellite_range = np.linalg.norm(satellite_rel_xyz)

# # 计算卫星的仰角和方位角
# elevation = np.arcsin(satellite_rel_xyz[2] / satellite_range)
# azimuth = np.arctan2(satellite_rel_xyz[0], satellite_rel_xyz[1])

# # 将方位角从北极方向转换为正东方向
# azimuth = np.pi / 2 - azimuth

# # 将弧度转换为角度
# latitude_deg = np.degrees(latitude)
# longitude_deg = np.degrees(longitude)
# elevation_deg = np.degrees(elevation)
# azimuth_deg = np.degrees(azimuth)

# print("测站经纬度：{}, {}".format(latitude_deg, longitude_deg))
# print("卫星仰角：{}".format(elevation_deg))
# print("卫星方位角：{}".format(azimuth_deg))
'''
    Le 测站纬度
    Ls 卫星纬度
    le 测站经度
    ls 卫星经度
'''

Le = 0
Ls = 0 
le = 0
ls = 0
Ls, ls, alt = pm.ecef2geodetic(1004591.08, -5081433.5804, -4531206.1957)
Le, le, alt = pm.ecef2geodetic(1121826.61526021, -4623505.4143307,  -4233738.31197042)
x, y, z = 1004591.08, -5081433.5804, -4531206.1957#卫星坐标
sx, sy, sz = 1121826.61526021, -4623505.4143307,  -4233738.31197042 #测站坐标
y = math.cosh(math.cos(Le)*math.cos(Ls) * math.cos(ls - le) + math.sin(Le)*math.sin(Ls))

rs = math.sqrt(x**2 + y**2 + z**2)
re = math.sqrt(sx**2 + sy**2 + sz**2)

d = rs*math.sqrt((1 + (re/rs)**2 - 2*(re/rs)*math.cos(y)))
#el 卫星高度角 zentith 卫星天顶角
el = math.cosh((rs * math.sin(y) / d))
zenith = 90 - math.degrees(el) 

azimuth = math.tanh((math.sin(abs(ls-le))*math.cos(Ls))/ (math.cos(Le)*math.sin(Ls)
                                -math.sin(Le)*math.cos(Ls)*math.cos(Le-Ls)))
print('卫星天顶角：\n', zenith)
print('卫星方位角：\n', azimuth)


