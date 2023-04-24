import math

def latlon_to_xyz(lat, lon, zoom):
    n = 2.0 ** zoom
    xtile = int((lon + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(math.radians(lat)) + (1 / math.cos(math.radians(lat)))) / math.pi / 2.0 * n))
    return (xtile, ytile, zoom)

# Example usage:
lat = 40.7128
lon = -74.0060
zoom = 12
x, y, z = latlon_to_xyz(lat, lon, zoom)
print(x,y,z)