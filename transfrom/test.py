import numpy as np


# 卫星位置向量
satellite_pos = np.array([1004591.08, -5081433.5804, -4531206.1957])

# 测站位置向量
receiver_pos = np.array([1121826.61526021 ,-4623505.4143307 , -4233738.31197042])

# 计算卫星方向向量
satellite_dir = satellite_pos - receiver_pos

# 计算卫星方向向量的长度
satellite_dir_len = np.linalg.norm(satellite_dir)

# 计算卫星方向向量的单位向量
satellite_dir_unit = satellite_dir / satellite_dir_len

# 计算卫星天顶角（单位为弧度）
zenith_angle = np.arccos(np.dot(np.array([0, 0, 1]), satellite_dir_unit))

# 将卫星天顶角转换为角度
zenith_angle_degrees = np.degrees(zenith_angle)

print("卫星天顶角为：{:.2f} 度".format(zenith_angle_degrees))
