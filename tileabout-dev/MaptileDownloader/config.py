"""
@author axiner
@version v1.0.0
@created 2022/10/20 17:07
@abstract
@description
@history
"""
import os
from pathlib import Path

from common.exceptions import MapstyleError

BASE_DIR = Path(__file__).resolve().parent

# debug
DEBUG = False
# 日志目录
LOG_DIR = BASE_DIR.joinpath('logs').as_posix()
# 存储目录
STORAGE_DIR = BASE_DIR.joinpath('storage').as_posix()

# 允许的地图类型
ALLOW_MAPSTYLES = [
    # 天地图api类型
    'vec_w',  # 矢量底图
    'cva_w',  # 矢量注记
    'img_w',  # 影像底图
    'cia_w',  # 影像注记
    'ter_w',  # 地形晕渲
    'cta_w',  # 地形注记
    'ibo_w',  # 全球境界
    'eva_w',  # 矢量英文注记
    'eia_w',  # 影像英文注记
    # 谷歌api类型
    's',  # 卫星图
    'y',  # 带标签的卫星图
    't',  # 地形图
    'p',  # 带标签的地形图
    'm',  # 路线图
    'h',  # 标签层（路名、地名等）
]

# 地图类型
MAPSTYLE = os.environ.get('MAPSTYLE') or 'img_w'
if not MAPSTYLE:
    raise MapstyleError('MAPSTYLE地图类型不能为空，请配置')
