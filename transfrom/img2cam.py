import numpy as np

# 相机内参矩阵
fx = 575 * 10-3  # 焦距x
fy = 575 * 10-3  # 焦距y
cx = 3960  # 光心x
cy = 3960  # 光心y
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0, 0, 1]])

# 像素坐标
u, v = 100 , 100  # 像素坐标

# 归一化相机坐标系下的坐标
u_norm = (u - cx) / fx
v_norm = (v - cy) / fy

# 相机坐标系下的坐标
camera_coords = np.array([u_norm, v_norm, 1])

print(camera_coords)
