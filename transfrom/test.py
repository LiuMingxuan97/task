import cv2
import numpy as np


img = cv2.imread("/Users/liumingxuan/code/pycode/transfrom/640.jpg")
pattern_size = (7,7)
ret, corners = cv2.findChessboardCorners(img, pattern_size, None)
cv2.drawChessboardCorners(img, pattern_size, corners, ret)

world_points = np.zeros((pattern_size[0]*pattern_size[1], 3), np.float32)
world_points[:,:2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1,2)

image_points = corners.reshape(-1, 2)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera([world_points], [image_points], img.shape[:-1], None, None)

undistorted_img = cv2.undistort(img, mtx, dist, None, mtx)
print(dist.ravel())

# cv2.imshow('ORI img', img)
# cv2.imshow('Undistored img', undistorted_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
