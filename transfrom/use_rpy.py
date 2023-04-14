import numpy as np
import pymap3d
import arrow
from datetime import datetime
from scipy.spatial.transform import Rotation



def img2ecef():
    Samples, Lines = 7920, 7920

    # optical center (pixels) in x,y direction
    Cx, Cy = 3960, 3960
    # focal length (m)
    F=575.0e-3 
    # size of pixels in world units (m)
    Px=4.6e-6 
    Py=4.6e-6 
    # observer position:wgs84
    x=1009105
    y=-5047454
    z=-4568021
    vx, vy, vz = -0.68296, -5.20974, 5.604
    time_second = 1230768000 + 388728701
    sate_time = arrow.get(time_second)
    sate_time = sate_time.datetime
    obs_x, obs_y, obs_z = pymap3d.ecef2eci(x, y, z, sate_time)
    obs_vx, obs_vy, obs_vz = pymap3d.ecef2eci(vx, vy, vz, sate_time)
    # obs_x, obs_y, obs_z = x, y, z
    # obs_vx, obs_vy, obs_vz = vx, vy, vz
    # radius of body (m):
    major_radius=6378140
    minor_radius=6356750
    #Rotation:
    omega=-0.34
    phi=-0.188
    kappa=-0.0381
    q0 = 0.47905656695365
    q1 = -0.033635303378105
    q2 = 0.876417875289917
    q3 = 0.035567
    #transform
    image_vector = np.array([Samples, Lines, 1], dtype=float)
    #camera_array像元坐标转到相机坐标
    camera_array = np.array([[Py, 0, 0],[0, Px,0],[-Cy*Py,-Cx*Px,F]], dtype=float)
    print('camera_array',camera_array)
    camera_look_vector = np.matmul(np.transpose(image_vector),camera_array)
    #img2cam
    camera_look_vector=camera_look_vector/np.linalg.norm(camera_look_vector,2)
    #定义旋转矩阵
    rotation_matrix=np.ndarray(shape=(3,3), dtype=float, order='F')
    rotation_matrix[0,0]=np.cos(phi)*np.cos(kappa)
    rotation_matrix[1,0]=np.cos(omega)*np.sin(kappa)+np.sin(omega)*np.sin(phi)*np.cos(kappa)
    rotation_matrix[2,0]=np.sin(omega)*np.sin(kappa)-np.cos(omega)*np.sin(phi)*np.cos(kappa)
    rotation_matrix[0,1]=-np.cos(phi)*np.sin(kappa)
    rotation_matrix[1,1]=np.cos(omega)*np.cos(kappa)-np.sin(omega)*np.sin(phi)*np.sin(kappa)
    rotation_matrix[2,1]=np.sin(omega)*np.cos(kappa)+np.cos(omega)*np.sin(phi)*np.sin(kappa)
    rotation_matrix[0,2]=np.sin(phi)
    rotation_matrix[1,2]=-np.sin(omega)*np.cos(phi)
    rotation_matrix[2,2]=np.cos(omega)*np.cos(phi)
    # print('rotation_matrix\n',rotation_matrix)
    
    roll=-0.34
    pitch=-0.188
    yaw=-0.0381
    rotation_matrix_zyx = np.array([
    [np.cos(yaw)*np.cos(pitch), np.cos(yaw)*np.sin(pitch)*np.sin(roll)-np.sin(yaw)*np.cos(roll), np.cos(yaw)*np.sin(pitch)*np.cos(roll)+np.sin(yaw)*np.sin(roll)],
    [np.sin(yaw)*np.cos(pitch), np.sin(yaw)*np.sin(pitch)*np.sin(roll)+np.cos(yaw)*np.cos(roll), np.sin(yaw)*np.sin(pitch)*np.cos(roll)-np.cos(yaw)*np.sin(roll)],
    [-np.sin(pitch), np.cos(pitch)*np.sin(roll), np.cos(pitch)*np.cos(roll)]
])
    # print('rotation_matrix_zyx\n',rotation_matrix_zyx)
    
    quat = np.array([q0, q1, q2, q3])

    # 创建旋转矩阵对象
    r = Rotation.from_quat(quat)

    # 将四元数转换为旋转矩阵
    rotation_matrix_q = r.as_matrix()
    # print('rotation_matrix_q\n',rotation_matrix_q)


    look_vector=np.matmul(np.transpose(camera_look_vector),rotation_matrix_q)
    #轨道到j2000的旋转矩阵
    r_ECI = np.array([[obs_x, obs_y, obs_z]])
    v_ECI = np.array([[obs_vx, obs_vy, obs_vz]])
    R_orb2eci = orb2eci(r_ECI, v_ECI)
    
    # look_vector=np.matmul(np.transpose(look_vector),R_orb2eci)
    
    
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

def orb2eci(r_ECI, v_ECI):
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
    return R_orb2eci

if __name__=='__main__':
    img2ecef()

 
    