"""
@author axiner
@version v1.0.0
@created 2022/10/21 22:53
@abstract
@description
@history
"""
import sys
from typing import Any, Iterable, Optional

import requests
from tilecloud import Tile, TileLayout, TileStore

from common.log import getLogger
from core.cache import Cache

logger = getLogger()


class URLTileStore(TileStore):
    def __init__(
            self,
            tilelayouts: Iterable[TileLayout],
            headers: Optional[Any] = None,
            allows_no_contenttype: bool = False,
            **kwargs: Any,
    ) -> None:
        TileStore.__init__(self, **kwargs)
        self.allows_no_contenttype = allows_no_contenttype
        self.tilelayouts = tuple(tilelayouts)
        self.session = requests.session()
        if headers is not None:
            self.session.headers.update(headers)

    def get_one(self, tile: Tile) -> Optional[Tile]:
        if tile is None:
            return None
        if self.bounding_pyramid is not None:
            if tile.tilecoord not in self.bounding_pyramid:
                return None
        tilelayout = self.tilelayouts[hash(tile.tilecoord) % len(self.tilelayouts)]
        try:
            url = tilelayout.filename(tile.tilecoord, tile.metadata)
        except Exception as e:
            logger.error(e)
            tile.error = e
            return tile

        logger.info(f"【发送请求:{tile.tilecoord}】{url}")
        try:
            response = self.session.get(url)
            logger.info(f'【响应状态码】{response.status_code}')
            if response.status_code == 418:
                Cache.Count418 += 1
                if Cache.Count418 > 3:
                    logger.warning('【418警告】爬取已达上限!!!')
                    sys.exit(1)
            if response.status_code in (404, 204):
                return None
            tile.content_encoding = response.headers.get("Content-Encoding")
            tile.content_type = response.headers.get("Content-Type")
            if response.status_code < 300:
                if response.status_code != 200:
                    tile.error = f"Unsupported status code {response.status_code}: {response.reason}"
                resp_content = response.content
                if tile.content_type:
                    if tile.content_type.startswith("image/"):
                        tile.data = resp_content
                    else:
                        if resp_content and isinstance(resp_content, bytes):
                            tile.data = resp_content
                        else:
                            tile.error = f"The Content-Type header is {tile.content_type}"
                else:
                    if self.allows_no_contenttype:
                        tile.data = resp_content
                    else:
                        tile.error = "The Content-Type header is missing"
            else:
                tile.error = response.reason or f'Status-Code: {response.status_code}'
        except requests.exceptions.RequestException as e:
            tile.error = e
        if tile.error:
            logger.error(f'【请求报错】{tile.error}')
            return None
        return tile
