import pymap3d

lon, lat, alt = pymap3d.ecef2geodetic(1034064.47455181, -5022494.52544819, -3780158.79823832)
print(lon,lat,alt)