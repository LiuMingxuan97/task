"""
@author axiner
@version v1.0.0
@created 2022/10/26 17:28
@abstract
@description
@history
"""
from tilecloud.layout.template import TemplateTileLayout
from toollib import useragent

from config import MAPSTYLE
from core.url import URLTileStore


tilestore = URLTileStore(
    (
        TemplateTileLayout(f"http://mts{SERVICE_NODE}.google.com/vt/"
                           f"lyrs={MAPSTYLE}&hl=zh-CN&gl=CN&src=app&z=%(z)d&x=%(x)d&y=%(y)d")
        for SERVICE_NODE in range(4)
    ),
    headers={
        'User-Agent': useragent.random_ua,
        "Connection": 'keep-alive',
        'Referer': "https://www.google.com/",
    },
    allows_no_contenttype=True,
    content_type="image/png",
)
