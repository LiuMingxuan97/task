import cv2
import numpy as np

# 读取图像
img = cv2.imread('/Users/liumingxuan/code/pycode/transfrom/640.jpg')

# 定义相机内参和畸变参数
mtx = np.array([[1000, 0, 500], [0, 1000, 500], [0, 0, 1]])
dist = np.array([0.1, -0.2, 0.3, 0.1])

# 定义径向畸变和切向畸变参数
k1, k2, p1, p2 = -0.2, 0.1, 0.001, 0.002

# 对图像进行径向畸变矫正
img_distorted = np.copy(img)
h, w = img.shape[:2]
for i in range(h):
    for j in range(w):
        x, y = j, i
        distorted_x = x + x * (k1*(x**2 + y**2) + k2*(x**2 + y**2)**2) + 2*p1*x*y + p2*(x**2 + y**2)
        distorted_y = y + y * (k1*(x**2 + y**2) + k2*(x**2 + y**2)**2) + p1*(x**2 + y**2) + 2*p2*x*y
        # if distorted_x >= 0 and distorted_x < w and distorted_y >= 0 and distorted_y < h:
        if distorted_y > 1079:
            distorted_y == 1080
        if distorted_x > 1079:
            distorted_x == 1080
        img_distorted[i, j] = img[int(distorted_y), int(distorted_x)]

# 显示原始图像和添加径向畸变后的图像
cv2.imshow('Original', img)
cv2.imshow('Distorted', img_distorted)
cv2.waitKey(0)
cv2.destroyAllWindows()
