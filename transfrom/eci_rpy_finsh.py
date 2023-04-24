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
roll, pitch, yaw = -0.3421, -0.1881, -0.0385066
q0, q1,  q2, q3 = 0.4818, -0.03303, 0.874899, 0.0365
# obs_x, obs_y, obs_z =1009100, -5047454, -4568021
obs_x, obs_y, obs_z =1004591.08, -5081433.5804, -4531206.1957
obs_pos = [obs_x, obs_y, obs_z]
obs_vx, obs_vy, obs_vz = -695.9209219793258, -5168.771531155607, 5640.48474229
obs_vel = [obs_vx, obs_vy, obs_vz]
time_second = 1230768000 + 388728708.548033
#相机参数
Samples, Lines = 7920, 1
# optical center (pixels) in x,y direction
Cx, Cy = 3960, 3960
# focal length (m)
F=575.0e-3 
# size of pixels in world units (m)
Px=4.6e-6 
Py=4.6e-6 
major_radius=6378140
minor_radius=6356750
pix_cam_id = (0,5000)
principal_point_x = 0.5
principal_point_y = 3960

def pos_cam(pix_cam_id, Px):
    pos_cam_mm = np.array([pix_cam_id[0] *Px , pix_cam_id[1]*Px, 1])
    return pos_cam_mm


def img2cam(Px, Py, F, principal_point_x, principal_point_y):
    fc = F
    x0 = principal_point_x * Px
    y0 = principal_point_y * Py
    R_img2cam = np.array([[1, 0, -x0],
                          [0, 1, -y0],
                          [0, 0, -fc]])
    return R_img2cam

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

def eci2ecr(satatime):
    R_eci2ecr = np.ndarray(shape=(3,3), dtype=float, order='F')
    sate_time = arrow.get(satatime)
    sate_time = sate_time.datetime
    date_str = sate_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/naif0012.tls')
    spice.furnsh('/Users/liumingxuan/code/pycode/transfrom/earth_latest_high_prec.bpc')
    et = spice.str2et(date_str)
    mat = spice.pxform('J2000', 'ITRF93',  et)
    for i in range(3):
        for j in range(3):
            R_eci2ecr[i,j] = mat[i][j] / pow(3,0.5)
    return R_eci2ecr

def cal_pos(major_radius, minor_radius, look_vector, eci_pos):
    
    obs_x, obs_y, obs_z = eci_pos[0], eci_pos[1], eci_pos[2]
    A = major_radius ** 2
    B = minor_radius ** 2
    a = (look_vector[0]**2 + look_vector[1]**2) / A + look_vector[2] ** 2 / B
    b = 2*(( look_vector[0] * obs_x + look_vector[1] * obs_y) / A + look_vector[2] * obs_z / B)
    c = (obs_x ** 2 +obs_y ** 2) / A + obs_z ** 2 / B - 1
    
    d = b**2 - 4.0*a*c

    if d < 0 :
        result = - b / (2 * a)
    elif d == 0:
        result = - b / (2 * a)
    else:
        e = math.sqrt(d)
        x1 = (-b + e) / (2 * a)
        x2 = (-b - e) / (2 * a)
        if abs(x1) > abs(x2):
            result = x2
        else:
            result = x1
    ground_point = result * look_vector + eci_pos
    return ground_point






if __name__=='__main__':
    
    R_eci2ecr = eci2ecr(time_second)
 
    pos_cam_mm = pos_cam(pix_cam_id, Px)
    R_img2cam = img2cam(Px, Py, F, principal_point_x, principal_point_y)
    # print('R_img2cam:\n', R_img2cam)
    look_vector = np.dot(pos_cam_mm, R_img2cam)
    # print('look_vector', look_vector)
   
    
    R_cam2body = cam2body()
    # print('R_cam2body:\n', R_cam2body)
    R_body2orb = body2orb(roll, pitch, yaw)
    # print('R_body2orb:\n', R_body2orb)
    eci_pos, eci_vel = ecr2eci(obs_pos, obs_vel, time_second)
    print('eci_pos',eci_pos)
    print('eci_vel',eci_vel)
    R_orb2eci = orb2eci(eci_pos, eci_vel)
    # print('R_orb2eci:\n', R_orb2eci)
    R_body2eci = R_orb2eci.dot(R_body2orb)
    # print('R_body2eci:\n', R_body2eci)
    # R_img2eci = R_img2cam.dot(R_cam2body.dot( R_body2eci))
    # print('R_img2eci1:\n', R_img2eci)
    R_img2eci = R_body2eci.dot(R_cam2body.dot(R_img2cam))
    # print('R_img2eci:\n', R_img2eci)
    
    v_i = np.dot(R_img2eci, pos_cam_mm)
    # print('v_i', v_i)
    
    ground_point = cal_pos(major_radius, minor_radius, v_i, eci_pos)
    # print('ground_point:\n', ground_point)
    sate_time = arrow.get(time_second)
    sate_time = sate_time.datetime
    lat, lon, alt = pymap3d.eci2geodetic(ground_point[0], ground_point[1], ground_point[2], sate_time)
    print(lat, lon, alt)
    pos_cam_mm_1 = pos_cam(pix_cam_id, Px)
    # print('pos_cam_mm_1', pos_cam_mm_1)
    
