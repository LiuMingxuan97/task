import rasterio
import numpy as np
from pykrige.ok import OrdinaryKriging

low_res_image = gdal.Open('low_res_image.tif')
low_res_band = low_res_image.GetRasterBand(1)
low_res_array = low_res_band.ReadAsArray()
scale_factor = 2
new_height = low_res_image.RasterYSize * scale_factor
new_width = low_res_image.RasterXSize * scale_factor
geotransform = low_res_image.GetGeoTransform()
projection = low_res_image.GetProjection()
x = np.linspace(0, new_width - 1, new_width)
y = np.linspace(0, new_height - 1, new_height)
xv, yv = np.meshgrid(x, y)
z = low_res_array.flatten()
x_l = np.linspace(0, low_res_image.RasterXSize - 1, low_res_image.RasterXSize)
y_l = np.linspace(0, low_res_image.RasterYSize - 1, low_res_image.RasterYSize)
xv_l, yv_l = np.meshgrid(x_l, y_l)

OK = OrdinaryKriging(xv_l.flatten(), yv_l.flatten(), z, variogram_model='linear')
z_interp, _ = OK.execute('grid', xv.flatten(), yv.flatten())
upscaled_array = z_interp.reshape(new_height, new_width)
driver = gdal.GetDriverByName('GTiff')
upscaled_image = driver.Create('upscaled_image.tif', new_width, new_height, 1, gdal.GDT_Float32)
upscaled_image.GetRasterBand(1).WriteArray(upscaled_array)
upscaled_image.SetGeoTransform(geotransform)
upscaled_image.SetProjection(projection)
upscaled_image.FlushCache()
# Close the images
low_res_image = None
upscaled_image = None
