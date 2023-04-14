import numpy as np

def prosses(wgs_x, wgs_y, wgs_z, rpy:list, vx, vy, vz):
    pass


def img2cam(principal_point_x, principal_point_y,fc,dpi):
    x0_m = principal_point_x * dpi
    y0_m = principal_point_y * dpi
    
    R_img2cam = np.array([[0, -1, x0_m*dpi], [1, 0, -y0_m*dpi], [0, 0, -fc]])
    return RecursionError
image_id = [3960,3960]
pos_cam_mm = np.array([image_id[0], image_id[1], 1])

# img2cam()