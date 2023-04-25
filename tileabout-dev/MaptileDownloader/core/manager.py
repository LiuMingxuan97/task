"""
@author axiner
@version v1.0.0
@created 2022/10/18 11:05
@abstract
@description
@history
"""
import sqlite3
from pathlib import Path

import typing as t
from tilecloud import BoundingPyramid, TileStore, TileCoord, Tile
from tilecloud.store.boundingpyramid import BoundingPyramidTileStore
from toollib.utils import now2str

from common import utils
from common.exceptions import FailedError
from common.log import getLogger
from common.utils import mock_sleep, valid_mapconfig
from config import STORAGE_DIR
from core.calc import all_level_tiles, zxy_tiles

logger = getLogger()


def download_tiles(
        storename: str,
        mapstyle: str,
        bounds: list,
        levels: list,
        zxy: list,
        mbtiles: str,
        redownload: str,
        max_tries: int,
):
    """
    下载瓦片
    :param storename: 瓦片仓库名称
    :param mapstyle: 瓦片类型
    :param bounds: 经纬范围
    :param levels: 层级范围
    :param zxy: 具体层级坐标
    :param mbtiles: mbtiles文件
    :param redownload: 失败记录文件，内容形如：tilecoord:11/1448/811
    :param max_tries: 最大重试次数
    :return:
    """
    # 设置地图类型
    valid_mapconfig(storename, mapstyle)
    # Create our input and output TileStores
    input_tilestore = TileStore.load(f"tilestores.{storename}")
    if not mbtiles:
        mbtiles = utils.gen_mbtiles_name(storename, mapstyle, bounds, levels, zxy)
    storage_dir = Path(STORAGE_DIR)
    storage_dir.mkdir(parents=True, exist_ok=True)
    mbtiles_path = storage_dir.joinpath(mbtiles).as_posix()

    if redownload:  # 重新下载失败的
        if not Path(mbtiles_path).exists():
            raise FailedError(f'{mbtiles} 数据文件不存在')
        output_tilestore = TileStore.load(mbtiles_path)
        redownload_failed(input_tilestore, output_tilestore, mbtiles_path, mbtiles, max_tries)
    else:  # 正常下载
        if levels:
            all_tiles = all_level_tiles(bounds, levels)
        else:
            all_tiles = zxy_tiles(bounds, zxy)
        output_tilestore = TileStore.load(mbtiles_path)
        failed_record_path = f'{STORAGE_DIR}/failed_{mbtiles.replace("mbtiles", "txt")}'  # 失败记录文件路径
        for tile in all_tiles:
            # 1) Generate a list of tiles to download from a BoundingPyramid
            #    4/8/5 is the root tile, corresponding to Central Europe
            #    +3/+1/+1 specifies up to zoom level 4 + 3 = 7 and an extent of one tile in the X and Y directions
            tile_z, tile_x, tile_y = tile.z, tile.x, tile.y
            bounding_pyramid = BoundingPyramid.from_string("{z}/{min_x}/{min_y}:+{diff_x}/+{diff_y}".format(
                z=tile_z,
                min_x=tile_x[0],
                min_y=tile_y[0],
                diff_x=tile_x[1]-tile_x[0]+1,
                diff_y=tile_y[1]-tile_y[0]+1))
            bounding_pyramid_tilestore = BoundingPyramidTileStore(bounding_pyramid)
            tile_list = bounding_pyramid_tilestore.list()
            # 2) 过滤存在且数据不为空的
            tilestream = (tile for tile in tile_list if not had_dwnloaded_data(tile.tilecoord, mbtiles_path))
            _downloading(input_tilestore, output_tilestore, tilestream, failed_record_path, max_tries)


def had_dwnloaded_data(tilecoord, mbtiles_path) -> bool:
    """是否已经下载数据
    记录存在且数据不为空，则True
    """
    # zxy处理
    z, x, y = tilecoord.z, tilecoord.x, tilecoord.y
    y = (1 << z) - y - 1
    # 查询是否存在且数据不为空
    with sqlite3.connect(mbtiles_path) as conn:
        cur = conn.cursor()
        had_data_sql = "select zoom_level from tiles where zoom_level = ? and tile_column = ? and tile_row = ? " \
                       "and tile_data is not null"
        cur.execute(had_data_sql, [z, x, y])
        result = cur.fetchone()
    return result


def _downloading(input_tilestore, output_tilestore, tilestream, failed_record_path, max_tries: int = 3):
    """下载操作"""
    for i in range(max_tries+1):
        if i > 0:
            logger.info(f'【失败重试】第{i}次...')
        # 1) 下载瓦片
        requested_tiles = input_tilestore.get(tilestream)
        # 2) 瓦片入库
        save_tiles = output_tilestore.put(filter(None, requested_tiles))

        tilestream = []
        for item in save_tiles:
            if item.error or not item.data:  # 对失败的进行记录
                tilestream.append(item)
            mock_sleep()
        if not tilestream:
            break
    else:
        # 把最后失败的记录到文件
        if tilestream:
            with open(failed_record_path, 'a+', encoding='utf8') as fp:
                fp.write('\n' + now2str() + '\n')
                fp.write('\n'.join({f'tilecoord:{ftile.tilecoord}' for ftile in tilestream}))
                fp.write('\n')


def redownload_failed(input_tilestore, output_tilestore, mbtiles_path: str, mbtiles: str, max_tries: int):
    """重新下载失败的"""
    # 1）查询失败的tile
    failed_tiles = _get_failed_tiles(mbtiles_path, mbtiles)
    # 2) 下载
    # 失败记录文件路径
    failed_record_path = f'{STORAGE_DIR}/refailed_{now2str("%Y%m%d%H%M%S")}_{mbtiles.replace("mbtiles", "txt")}'
    _downloading(input_tilestore, output_tilestore, failed_tiles, failed_record_path, max_tries)


def _get_failed_tiles(mbtiles_path, mbtiles) -> t.Iterator[Tile]:
    """获取失败的瓦片"""
    # 查询数据为空的记录
    with sqlite3.connect(mbtiles_path) as conn:
        cur = conn.cursor()
        had_data_sql = "select zoom_level,tile_column,tile_row from tiles where tile_data is null"
        cur.execute(had_data_sql)
        result = cur.fetchall()
        if result:
            for item in result:
                z, x, y = item[0], item[1], item[2]
                y = (1 << z) - y - 1
                yield Tile(TileCoord(z=z, x=x, y=y))
        else:
            logger.info(f'【提醒】没有缺失数据（{mbtiles}）')
