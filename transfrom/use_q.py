import numpy as np
import pymap3d
import arrow
from datetime import datetime
from scipy.spatial.transform import Rotation

'''
四元数为卫星本体在j2000坐标系中的姿态四元数,可直接由观测四元数确定卫星本体坐标系到j2000坐标系的转换矩阵
无须经过轨道坐标系的过渡
'''

def img2ecef(pos:list, vel:list, second, qua:list ):
    Samples, Lines = 7920, 7920
    # optical center (pixels) in x,y direction
    Cx, Cy = 3960, 3960
    # focal length (m)
    F=575.0e-3 
    # size of pixels in world units (m)
    Px, Py = 4.6e-6, 4.6e-6 
    # observer position:wgs84
    x, y, z = pos[0], pos[1], pos[2]
    vx, vy, vz = vel[0], vel[1], vel[2]
    #转换utc起始时间
    time_second = 1230768000 + second
    sate_time = arrow.get(time_second)
    sate_time = sate_time.datetime
    obs_x, obs_y, obs_z = pymap3d.ecef2eci(x, y, z, sate_time)
    obs_vx, obs_vy, obs_vz = pymap3d.ecef2eci(vx, vy, vz, sate_time)
    # radius of body (m):
    major_radius=6378137
    minor_radius=6356752.3
    #qua:
    q0, q1,  q2, q3 = qua[0], qua[1], qua[2], qua[3]
    #transform
    image_vector = np.array([Samples, Lines, 1], dtype=float)
    #camera_array像元坐标转到相机坐标
    camera_array = np.array([[Py, 0, 0],[0, Px,0],[-Cy*Py,-Cx*Px,F]], dtype=float)
    print('camera_array',camera_array)
    camera_look_vector = np.matmul(np.transpose(image_vector),camera_array)
    #img2cam
    camera_look_vector=camera_look_vector/np.linalg.norm(camera_look_vector,2)
    print('camera_look_vector:\n',camera_look_vector)
    #cam2body
    R_cam2body = np.array([[1, 0, 0],[0, 1, 0],[0, 0, 1]])
    
    body_look_vector = np.matmul(np.transpose(camera_look_vector), R_cam2body)
    print('body_look_vector:\n',body_look_vector)
    #body2eci
    quat = np.array([q0, q1, q2, q3])

    # 创建旋转矩阵对象
    r = Rotation.from_quat(quat)

    # 将四元数转换为旋转矩阵
    rotation_matrix_q = r.as_matrix()

    look_vector=np.matmul(np.transpose(camera_look_vector),rotation_matrix_q)

    
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
    lon, lat, alt = pymap3d.eci2geodetic(ground_point[0], ground_point[1], ground_point[2], sate_time)
    print(lon,lat,alt)



if __name__=='__main__':
    # img2ecef(pos=[1009105, -5047454, -4568021], vel=[-0.68296, -5.20974, 5.604], second=388728701,
    #          qua=[0.47905656695365, -0.033635303378105, 0.876417875289917, 0.035567])
    img2ecef(pos=[1005694, -5073216, -4540158], vel=[-682.96, -5209.74, 5604], second=388728707.45773,
             qua=[0.4818, -0.03303, 0.874899, 0.0365])

    