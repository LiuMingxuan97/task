import numpy as np


'''
建立相机到地面的转换
1. 像元到相机 line,sample,dpi,f,
2. 相机到卫星  默认没有旋转 和 偏置
3. 卫星到轨道  
4. 轨道到eci
5. eci到ecef
部分姿态信息描述 卫星相对惯性系  不需要步骤3
'''

R_img2eci = R_eci2ecr * R_body2eci * R_cam2body * R_img2cam

pix_cam__id = (pix_img(0), )



# x0_m = principal_point_x * dpi
# y0_m = principal_point_y * dpi

# R_img2cam = np.array([[0, -1, x0_m*dpi], [1, 0, -y0_m*dpi], [0, 0, -fc]])
# image_id = [3960,3960]
# pos_cam_mm = np.array([image_id[0], image_id[1], 1])

# img2cam()

