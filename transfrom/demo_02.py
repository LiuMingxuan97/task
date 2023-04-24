import numpy as np
import pymap3d
import arrow
from datetime import datetime
from scipy.spatial.transform import Rotation
from math import sin,cos
import spiceypy as spice
import math
# from transfrom import param
'''
参数
'''
roll, pitch, yaw = -0.34, -0.188, -0.0381
q0, q1,  q2, q3 = 0.4818, -0.03303, 0.874899, 0.0365
obs_x, obs_y, obs_z =1009100, -5047454, -4568021
obs_pos = [1009100, -5047454, -4568021]
obs_vx, obs_vy, obs_vz = -682.96, -5209.74, 5604
obs_vel = [-682.96, -5209.74, 5604]
time_second = 1230768000 + 388728701
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


def img2cam(Samples, Lines, Px, Py, Cx, Cy, F):
    image_vector = np.array([Samples, Lines, 1], dtype=float)
    #camera_array像元坐标转到相机坐标
    camera_array = np.array([[Py, 0, 0],[0, Px,0],[-Cy*Py,-Cx*Px,F]], dtype=float)
    camera_look_vector = np.matmul(np.transpose(image_vector),camera_array)
    camera_look_vector=camera_look_vector/np.linalg.norm(camera_look_vector,2)
    return camera_look_vector



def cam2body():
    R_cam2body = np.array([[1, 0, 0],
                           [0, 1, 0],
                           [0, 0, 1]])
    return R_cam2body

def body2orb(roll, pitch, yaw):
    R_x = np.array([[1, 0, 0],
                [0, cos(roll), sin(roll)],
                [0, -sin(roll), cos(roll)]])
    R_y = np.array([[cos(pitch), 0, -sin(pitch)],
                [0, 1, 0],
                [sin(pitch), 0, cos(pitch)]])
    R_z = np.array([[cos(yaw), sin(yaw), 0],
                [-sin(yaw), cos(yaw), 0],
                [0, 0,1 ]])
    R_body2orb= np.dot(R_x,np.dot(R_y,R_z)).T
    return R_body2orb

def ecr2eci(obs_pos, obs_vel, satatime):
    sate_time = arrow.get(satatime)
    sate_time = sate_time.datetime
    date_str = sate_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/naif0012.tls')
    spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/earth_latest_high_prec.bpc')
    et = spice.str2et(date_str)
    mat = spice.pxform('ITRF93', 'J2000', et)
    mat66_r2i = spice.sxform('ITRF93', 'J2000', et)
    epos, estate = [0] * 3, [0] * 6
    for i in range(3):
        epos[i] = obs_pos[i]
        estate[i] = obs_pos[i]
        estate[i+3] = obs_vel[i]
        jpos = spice.mxv(mat, epos)
        jstate = spice.mxvg(mat66_r2i, estate)
        eci_pos, eci_vel = [0] *3, [0] *3
    for i in range(3):
        eci_pos[i] = jpos[i]
        eci_vel[i] = jstate[i+3]
    return eci_pos, eci_vel

def orb2eci(r_ECI, v_ECI):
    '''
    :r_ECI   地固系通过spice转换为地惯系位置
    :v_ECI   地固系通过spice转换为地惯系速度
    '''
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
    return R_orb2eci

def eci2ecr(eci_x, eci_y, eci_z, satatime):
    obs_x, obs_y, obs_z = pymap3d.eci2ecef(eci_x, eci_y, eci_z, satatime)
    ecr_pos = [obs_x, obs_y, obs_z]
    return ecr_pos

def cal_pos(major_radius, minor_radius, look_vector, eci_pos):
    obs_x, obs_y, obs_z = eci_pos[0], eci_pos[1], eci_pos[2]
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
    
    return ground_point




if __name__=='__main__':
 
    #img2cam
    camera_look_vector = img2cam(Samples, Lines, Px, Py, Cx, Cy, F)
    print('camera_look_vector', camera_look_vector)
    R_cam2body = cam2body()
    R_body2orb = body2orb(roll, pitch, yaw)
    print('R_body2orb:\n', R_body2orb)
    eci_pos, eci_vel = ecr2eci(obs_pos, obs_vel, time_second)
    R_orb2eci = orb2eci(eci_pos, eci_vel)
    print('R_orb2eci:\n', R_orb2eci)
    R_body2eci  = R_orb2eci.dot(R_body2orb)
    print('R_body2eci:\n', R_body2eci)
    look_vector=np.matmul(np.transpose(camera_look_vector),R_body2eci)
    print('look_vector', look_vector)
    ground_point = cal_pos(major_radius, minor_radius, look_vector, eci_pos)
    print('ground_point:\n', ground_point)
    sate_time = arrow.get(time_second)
    sate_time = sate_time.datetime
    lat, lon, alt = pymap3d.eci2geodetic(ground_point[0], ground_point[1], ground_point[2], sate_time)
    print(lat, lon, alt)