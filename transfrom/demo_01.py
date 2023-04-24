import numpy as np
import pymap3d
import arrow
from datetime import datetime
from scipy.spatial.transform import Rotation
from math import sin,cos
import spiceypy as spice
import math


'''
rpy描述以轨道为参考系 卫星的转动姿态
q0 q1 q2 q3 描述以惯性系为参考系 卫星的转动姿态
'''
#卫星基本参数
roll, pitch, yaw = -0.34, -0.188, -0.0381
q0, q1,  q2, q3 = 0.4818, -0.03303, 0.874899, 0.0365
#地惯系下卫星姿态 q0, q1,  q2, q3
qua=[0.4818, -0.03303, 0.874899, 0.0365]
q0, q1,  q2, q3 = qua[0], qua[1], qua[2], qua[3]
quat = np.array([q0, q1, q2, q3])
# 创建旋转矩阵对象
r = Rotation.from_quat(quat)
rotation_matrix_q = r.as_matrix()
print('rotation_matrix_q:\n', rotation_matrix_q)

#卫星rpy转轨道系，轨道系转eci
#卫星rpy转轨道系


# roll, pitch, yaw = -0.34*math.pi/180, -0.188*math.pi/180, -0.0381*math.pi/180
rpy = [yaw, pitch, roll]
#使用第三方库
# R_boyd2orb = Rotation.from_euler('ZYX',rpy)
# R_boyd2orb_matrix = R_boyd2orb.as_matrix()
# print('disan:\n',R_boyd2orb_matrix)
#自己编写旋转矩阵
R_x = np.array([[1, 0, 0],
                [0, cos(roll), sin(roll)],
                [0, -sin(roll), cos(roll)]])
R_y = np.array([[cos(pitch), 0, -sin(pitch)],
                [0, 1, 0],
                [sin(pitch), 0, cos(pitch)]])
R_z = np.array([[cos(yaw), sin(yaw), 0],
                [-sin(yaw), cos(yaw), 0],
                [0, 0,1 ]])
R_boyd2orb_matrix_1 = np.dot(R_x,np.dot(R_y,R_z)).T
print('R_boyd2orb_matrix\n', R_boyd2orb_matrix_1)

#轨道系转eci
x=obs_x=1009100
y=obs_y=-5047454
z=obs_z=-4568021
vx, vy, vz = -682.96, -5209.74, 5604
obs_vx, obs_vy, obs_vz = -682.96, -5209.74, 5604
time_second = 1230768000 + 388728701
sate_time = arrow.get(time_second)
sate_time = sate_time.datetime
# obs_x, obs_y, obs_z = pymap3d.ecef2eci(x, y, z, sate_time)
# obs_vx, obs_vy, obs_vz = pymap3d.ecef2eci(vx, vy, vz, sate_time)
date_str = sate_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
r_ECI = np.array([[obs_x, obs_y, obs_z]])
v_ECI = np.array([[obs_vx, obs_vy, obs_vz]])

spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/naif0012.tls')
spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/earth_latest_high_prec.bpc')
et = spice.str2et(date_str)
mat = spice.pxform('ITRF93', 'J2000', et)
mat66_r2i = spice.sxform('ITRF93', 'J2000', et)
epos, estate = [0] * 3, [0] * 6
for i in range(3):
    epos[i] = r_ECI[0][i]
    estate[i] = r_ECI[0][i]
    estate[i+3] = v_ECI[0][i]
jpos = spice.mxv(mat, epos)
jstate = spice.mxvg(mat66_r2i, estate)
eci_pos, eci_vel = [0] *3, [0] *3
for i in range(3):
    eci_pos[i] = jpos[i]
    eci_vel[i] = jstate[i+3]
# print('eci_pos:\n', eci_pos)
# print('eci_vel:\n', eci_vel)
# r_ECI, v_ECI = np.array(eci_pos), np.array(eci_vel)
r_ECI = [eci_pos[0], eci_pos[1], eci_pos[2]]
v_ECI = [eci_vel[0], eci_vel[1], eci_vel[2]]
R_orb2eci = np.ndarray(shape=(3,3), dtype=float, order='F')
b3 = np.zeros(3)
b2 = np.zeros(3)
b1 = np.zeros(3)
temp = np.zeros(3)

for i in range(3):
    b3[i] = -1 * r_ECI[i] / np.linalg.norm(r_ECI)
temp = np.cross(b3, v_ECI)
norm = np.linalg.norm(temp)

for i in range(3):
    b2[i] = temp[i] / norm
    
b1 = np.cross(b2 , b3)
R_orb2eci = np.vstack((b1, b2, b3)).T
print('R_orb2eci:\n',R_orb2eci)

R_body2eci = R_orb2eci.dot(R_boyd2orb_matrix_1)
print('R_body2eci:\n', R_body2eci)


obs_x, obs_y, obs_z = r_ECI[0], r_ECI[1], r_ECI[2]
#相机参数
Samples, Lines = 7920, 7920
# optical center (pixels) in x,y direction
Cx, Cy = 3960, 3960
# focal length (m)
F=575.0e-3 
# size of pixels in world units (m)
Px=4.6e-6 
Py=4.6e-6 
major_radius=6378140
minor_radius=6356750
image_vector = np.array([Samples, Lines, 1], dtype=float)
#camera_array像元坐标转到相机坐标
camera_array = np.array([[Py, 0, 0],[0, Px,0],[-Cy*Py,-Cx*Px,F]], dtype=float)
print('camera_array',camera_array)
camera_look_vector = np.matmul(np.transpose(image_vector),camera_array)
#img2cam
camera_look_vector=camera_look_vector/np.linalg.norm(camera_look_vector,2)

look_vector=np.matmul(np.transpose(camera_look_vector),R_body2eci)
print('look_vector', look_vector)

radius_squared_ratio =major_radius**2/minor_radius**2
a=look_vector[0]**2 + look_vector[1]**2 + radius_squared_ratio*look_vector[2]**2
b=2*(look_vector[0]*obs_x+look_vector[1]*obs_y+radius_squared_ratio*look_vector[2]*obs_z)
c=obs_x**2+obs_y**2+radius_squared_ratio*obs_z**2-major_radius**2
discriminant=b**2-4.0*a*c

if discriminant<0 :
    discriminant=0
    
distance=(-b-np.sqrt(discriminant))/(2*a)

obs_vector=np.array([obs_x, obs_y, obs_z])
ground_point = obs_vector+distance*look_vector
print('ground_point', ground_point)
lon, lat, alt = pymap3d.eci2geodetic(ground_point[0], ground_point[1], ground_point[2], sate_time)
print(lon,lat,alt)