"""
@author axiner
@version v1.0.0
@created 2022/10/19 14:42
@abstract 主入口
@description
@history
"""
import argparse

from common.log import getLogger
from common.utils import valid_args
from config import MAPSTYLE
from core.manager import download_tiles

logger = getLogger()


def run():
    """执行入口"""
    parser = argparse.ArgumentParser(description=u'地图瓦片下载')
    parser.add_argument('--storename', '-s', required=True, type=str, help=u'瓦片仓库名称, 如：tianditu')
    parser.add_argument('--bounds', '-b', required=True, type=str, help=u'经纬范围(左经度,上纬度,右经度,下纬度)，如：100,40,120,20')
    parser.add_argument('--levels', '-l', type=str, help=u'层级范围(最小层级,最大层级)，如：1,2')
    parser.add_argument('--zxy', type=str, help=u'具体层级坐标(层级,min_x,max_x,min_y,max_y)，如：9,360,448,166,251。若层级范围传值，则该参数自动忽略')
    parser.add_argument('--mbtiles', type=str, help=u'mbtiles文件（也可指定已存在的mbtiles）')
    parser.add_argument('--redownload', action='store_true', help=u'是否重新下载(自动下载数据库中为空的记录)')
    parser.add_argument('--max_tries', default=3, type=int, help=u'最大重试次数')
    # 参数处理
    args = valid_args(parser.parse_args())
    storename = args.get('storename')
    bounds = args.get('bounds')
    levels = args.get('levels')
    zxy = args.get('zxy')
    mbtiles = args.get('mbtiles')
    redownload = args.get('redownload')
    max_tries = args.get('max_tries')
    # 追加瓦片类型
    args['mapstyle'] = MAPSTYLE
    # 开始下载
    logger.info(f'【开始下载】入参:{args}')
    download_tiles(
        storename=storename,
        mapstyle=MAPSTYLE,
        bounds=bounds,
        levels=levels,
        zxy=zxy,
        mbtiles=mbtiles,
        redownload=redownload,
        max_tries=max_tries,
    )


if __name__ == '__main__':
    run()
