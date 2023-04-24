from quaternions import Quaternion as Quaternion
import math

def cal_q():
    b = [-0.34219244,-0.188026,-0.03816] # ROLL PITCH HEADING
    a = Quaternion.from_euler(b,axes = ['z', 'y', 'x']) # 返回的是 w x y z
    print(a)

def focal2pixel_lines(focal_length, image_resolution, sensor_size):
    """
    将焦距（focal length）转换为像素线（pixel lines）

    参数：
    focal_length: float，相机的焦距，单位：毫米
    image_resolution: tuple，图像的分辨率，包括宽度和高度，单位：像素
    sensor_size: tuple，图像传感器的尺寸，包括宽度和高度，单位：毫米

    返回：
    pixel_lines: float，像素线的长度，单位：像素
    """
    # 计算图像传感器的对角线长度
    sensor_diagonal = (sensor_size[0]**2 + sensor_size[1]**2) ** 0.5

    # 计算像素线的长度
    pixel_lines = image_resolution[1] * focal_length / sensor_diagonal

    return pixel_lines



if __name__=='__main__':
    # result = focal2pixel_lines(focal_length=575, image_resolution=(7920, 7920), sensor_size=(4.6,4.6))
    # print(result)
    cal_q()