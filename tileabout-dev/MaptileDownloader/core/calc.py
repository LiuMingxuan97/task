"""
@author axiner
@version v1.0.0
@created 2022/10/19 15:05
@abstract
@description
@history
"""
import math

import typing as t


class Tile:
    """瓦片坐标"""
    z: int
    x: list
    y: list

    def __init__(self, z, x, y):
        self.z = z
        self.x = x
        self.y = y


def wgs84_to_tile(lon, lat, z):
    """
    WGS-84经纬度 => 谷歌地图中的瓦片坐标
    :param lon: longitude 经度
    :param lat: latitude 纬度
    :param z: zoom
    :return:
    """
    def isnum(x): return isinstance(x, int) or isinstance(x, float)

    if not(isnum(lon) and isnum(lat)):
        raise TypeError("lon and lat must be int or float!")
    if not isinstance(z, int) or z < 0 or z > 22:
        raise TypeError("z must be int and between 0 to 22.")

    if lon < 0:
        lon = 180 + lon
    else:
        lon += 180
    lon /= 360  # make lon to (0,1)

    lat = 85.0511287798 if lat > 85.0511287798 else lat
    lat = -85.0511287798 if lat < -85.0511287798 else lat
    lat = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180)
    lat /= 180  # make lat to (-1,1)
    lat = 1 - (lat + 1) / 2  # make lat to (0,1) and left top is 0-point

    num = 2**z
    x = math.floor(lon * num)
    y = math.floor(lat * num)
    return x, y


def tile_to_mercator(tile_x, tile_y, z):
    """
    谷歌地图中的瓦片坐标 => WGS-84经纬度
    :param tile_x:
    :param tile_y:
    :param z:
    :return:
    """
    length = 20037508.3427892
    num = 2**z
    mercator_x = tile_x / num * length * 2 - length
    mercator_y = -(tile_y / num * length * 2) + length
    return mercator_x, mercator_y


def all_level_tiles(bounds: list, levels: list) -> t.Iterator[Tile]:
    """
    所有层级坐标
    :param bounds: 经纬范围(左经度,上纬度,右经度,下纬度)，如：[100,40,120,20]
    :param levels: 层级范围(最小层级,最大层级)
    :return:
    """
    minlevel, maxlevel = levels
    for level in range(minlevel, maxlevel+1):
        left_title_x, top_title_y = wgs84_to_tile(bounds[0], bounds[1], level)
        right_title_x, bottom_title_y = wgs84_to_tile(bounds[2], bounds[3], level)
        yield Tile(
            z=level,
            x=(left_title_x, right_title_x),  # 瓦片横坐标范围（左至右）
            y=(top_title_y, bottom_title_y),  # 瓦片纵坐标范围（上至下）
        )


def zxy_tiles(bounds: list, zxy: list) -> list:
    """具体层级坐标"""
    z, min_x, max_x, min_y, max_y = zxy[0], zxy[1], zxy[2], zxy[3], zxy[4]
    # 判断是不是在给定经纬范围内
    left_title_x, top_title_y = wgs84_to_tile(bounds[0], bounds[1], z)
    right_title_x, bottom_title_y = wgs84_to_tile(bounds[2], bounds[3], z)
    if min_x < left_title_x or max_x > right_title_x:
        raise ValueError(f'{min_x,max_x} 已超出所给定经度范围对应的坐标值{left_title_x,right_title_x}')
    if min_y < top_title_y or max_y > bottom_title_y:
        raise ValueError(f'{min_y,max_y} 已超出所给定纬度范围对应的坐标值{top_title_y,bottom_title_y}')
    return [Tile(
        z=z,
        x=(min_x, max_x),
        y=(min_y, max_y),
    )]
