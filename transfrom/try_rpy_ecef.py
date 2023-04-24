import numpy as np
import pymap3d
import arrow
from datetime import datetime
from scipy.spatial.transform import Rotation
from math import sin,cos

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
#卫星rpy转轨道系，轨道系转eci
#卫星rpy转轨道系
roll, pitch, yaw = -0.34, -0.188, -0.0381
rpy = [roll, pitch, yaw]
#使用第三方库
# R_boyd2orb = Rotation.from_euler('XYZ',rpy)
# R_boyd2orb_matrix = R_boyd2orb.as_matrix()
#自己编写旋转矩阵
R_x = np.array([[1, 0, 0],
                [0, cos(roll), -sin(roll)],
                [0, sin(roll), cos(roll)]])
R_y = np.array([[cos(pitch), 0, -sin(pitch)],
                [0, 1, 0],
                [sin(pitch), 0, cos(pitch)]])
R_z = np.array([[cos(yaw), sin(yaw), 0],
                [-sin(yaw), cos(yaw), 0],
                [0, 0,1 ]])
R_boyd2orb_matrix = R_x.dot(R_y.dot(R_z))
print('R_boyd2orb_matrix\n', R_boyd2orb_matrix)
#轨道系转eci
x = obs_x = 100910
y = obs_y = -5047454
z = obs_z = -4568021
vx, vy, vz = -682.96, -5209.74, 5604
time_second = 1230768000 + 388728701
sate_time = arrow.get(time_second)
sate_time = sate_time.datetime

image_vector = np.array([Samples, Lines, 1], dtype=float)
camera_array = np.array([[Py, 0, 0],[0, Px,0],[-Cy*Py,-Cx*Px,F]], dtype=float)
camera_look_vector = np.matmul(np.transpose(image_vector),camera_array)
camera_look_vector=camera_look_vector/np.linalg.norm(camera_look_vector,2)

look_vector=np.matmul(np.transpose(camera_look_vector),R_boyd2orb_matrix)

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
lon, lat, alt = pymap3d.ecef2geodetic(ground_point[0], ground_point[1], ground_point[2])
print(lon, lat, alt)
# obs_x, obs_y, obs_z = pymap3d.ecef2eci(x, y, z, sate_time)
# obs_vx, obs_vy, obs_vz = pymap3d.ecef2eci(vx, vy, vz, sate_time)
# r_ECI = np.array([[obs_x, obs_y, obs_z]])
# v_ECI = np.array([[obs_vx, obs_vy, obs_vz]])
r_ECI = np.array([[x, y, z]])
v_ECI = np.array([[vx, vy, vz]])
R_orb2eci = np.ndarray(shape=(3,3), dtype=float, order='F')
b3 = np.empty((3,1))
b2 = np.empty((3,1))
b1 = np.empty((3,1))
temp = np.empty((3,1))
for i in range(3):
    b3[i] = -1 * r_ECI[0][i] / np.linalg.norm(r_ECI)
temp = np.matmul(b3, v_ECI)
norm = np.linalg.norm(temp)
for i in range(3):
    b2[i] = temp[i][0] / norm
b1 = b2 * b3
R_orb2eci = np.column_stack((b1, b2, b3))
print('R_boyd2orb_matrix:\n',R_boyd2orb_matrix)

R_body2eci = R_boyd2orb_matrix.dot(R_orb2eci)
print('R_body2eci:\n', R_body2eci)

