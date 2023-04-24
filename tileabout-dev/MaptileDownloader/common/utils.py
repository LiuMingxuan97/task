"""
@author axiner
@version v1.0.0
@created 2022/10/20 16:24
@abstract
@description
@history
"""
import importlib
import random
import re
import time

from common.exceptions import ParamsError, LoadTileModError, MapstyleError
from config import ALLOW_MAPSTYLES


def gen_mbtiles_name(storename: str, mapstyle: str, bounds: list, levels, zxy):
    """
    生成mbtiles文件名称
    :param storename:
    :param mapstyle:
    :param bounds:
    :param levels:
    :param zxy:
    :return:
    """
    if levels:
        scope = '_'.join(map(str, levels))
    else:
        scope = '_'.join(map(str, zxy))
    mbtiles_name = "{storename}-{mapstyle}-{bounds}-{scope}.mbtiles".format(
        storename=storename,
        mapstyle=mapstyle,
        bounds='_'.join(map(str, bounds)),
        scope=scope,
    )
    return mbtiles_name


def valid_mapconfig(storename: str, mapstyle: str):
    """校验地图配置"""
    try:
        importlib.import_module(f"tilestores.{storename}")
    except ModuleNotFoundError:
        raise LoadTileModError(f'{storename} 仓库名称未配置，请修改重试')
    if mapstyle not in ALLOW_MAPSTYLES:
        raise MapstyleError(f'{mapstyle} 瓦片类型错误，请修改重试')


def valid_args(args) -> dict:
    """校验参数"""
    bounds = args.bounds or ''
    levels = args.levels or ''
    zxy = args.zxy or ''
    mbtiles = args.mbtiles or ''
    if not re.match(r'^(-?\d+(\.-?\d+)?,){3}-?\d+$', bounds):
        raise ParamsError(f'{bounds} 经纬范围错误，应形如：116,39,120,42')
    if not any([levels, zxy]):  # 全假则报错
        raise ParamsError(f'层级范围(-l)与具体层级坐标(--zxy)必须输入一个(全为真取层级范围，具体层级坐标自动忽略)')
    else:
        if levels:
            if not re.match(r'^\d{1,2},\d{1,2}$', levels):
                raise ParamsError(f'{levels} 层级范围错误，应形如：1,2')
            levels = [int(i) for i in levels.split(',')]
            if levels[0] < 0 or levels[1] > 22:
                raise ParamsError(f'{args.levels} 层级超出范围 0,22')
        else:
            if not re.match(r'^\d{1,2},\d+,\d+,\d+,\d+$', zxy):
                raise ParamsError(f'{zxy} 具体层级坐标错误，应形如：9,360,448,166,251')
            zxy = [int(i) for i in zxy.split(',')]
            if zxy[0] < 0 or zxy[0] > 22:
                raise ParamsError(f'{zxy[0]} 层级超出范围 0,22')
    if mbtiles:
        if not mbtiles.endswith('.mbtiles'):
            raise ParamsError(f'{mbtiles} mbtiles文件后缀应为 .mbtiles')
    v_args = {
        'storename': args.storename,
        'bounds': [float(i) for i in bounds.split(',')],
        'levels': levels,
        'zxy': zxy,
        'max_tries': args.max_tries,
        'mbtiles': args.mbtiles,
        'redownload': args.redownload
    }
    return v_args


def mock_sleep():
    """模拟休眠"""
    s = random.choice([
        0,
        0.1, 0.2, 0.3, 0.4, 0.5,
        # 0.6, 0.7, 0.8, 0.9, 1.0,
        # 1.1, 1.2, 1.3, 1.4, 1.5,
    ])
    if s:
        time.sleep(s)
