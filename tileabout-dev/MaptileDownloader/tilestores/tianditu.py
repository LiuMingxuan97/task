"""
@author axiner
@version v1.0.0
@created 2022/10/18 11:20
@abstract
@description
@history
"""
import random

from tilecloud.layout.template import TemplateTileLayout
from toollib import useragent

from config import MAPSTYLE
from core.url import URLTileStore

TOKEN = [
    'c00b4864dc9fad76b0b38381dcd90ea7',
    '41de400b4278dbf84f21df4bf434e176',
    'af14e42c5fc14f3549bd0f2e4738bcd9',
    '51074d5cd640d13a55f6b59525197f77',
]


MAPSTYLE_SPLIT = MAPSTYLE.split('_')


tilestore = URLTileStore(
    (
        TemplateTileLayout(f"http://t{SERVICE_NODE}.tianditu.gov.cn/{MAPSTYLE}/wmts?"
                           f"SERVICE=WMTS&"
                           f"REQUEST=GetTile&VERSION=1.0.0&"
                           f"LAYER={MAPSTYLE_SPLIT[0]}&"
                           f"STYLE=default&"
                           f"TILEMATRIXSET={MAPSTYLE_SPLIT[1]}&"
                           f"FORMAT=tiles&TILEMATRIX=%(z)d&TILECOL=%(x)d&TILEROW=%(y)d&"
                           f"tk={random.choice(TOKEN)}")
        for SERVICE_NODE in range(7)
    ),
    headers={
        'User-Agent': useragent.random_ua,
        "Connection": 'keep-alive',
        'Referer': "https://www.tianditu.gov.cn/",
    },
    allows_no_contenttype=True,
    content_type="image/png",
)
