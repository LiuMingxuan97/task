"""
@author axiner
@version v1.0.0
@created 2022/11/8 20:49
@abstract
@description
@history
"""
import argparse
import sys
from pathlib import Path
import requests
import sqlite3

import typing as t
from toollib.crypto import cmd5
from toollib.utils import now2str

STORAGE_DIR = 'DemNasa30'
storage_dir = Path(STORAGE_DIR)
storage_dir.mkdir(parents=True, exist_ok=True)


class Sqlite:

    CREATE_INITTB_SQL = 'create table if not exists nasa30(' \
                        'id char(128) primary key,' \
                        'url integer not null,' \
                        'is_succeed integer default 0)'
    CHECK_DOWNLOADED_SQL = 'select id from nasa30 where id=? and is_succeed=1'
    UPDATE_DOWNLOADED_SQL = 'insert into nasa30 (id, url, is_succeed) values(?, ?, ?)'

    def __init__(self, dbname: str = 'nasa-30.db'):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def init(self):
        self.cursor.execute(self.CREATE_INITTB_SQL)
        self.conn.commit()

    def check_downloaded(self, uid) -> bool:
        self.cursor.execute(self.CHECK_DOWNLOADED_SQL, (uid, ))
        return self.cursor.fetchone()

    def update_downloaded(self, data: dict):
        params = (
            data.get('uid'),
            data.get('url'),
            data.get('is_succeed'),
        )
        self.cursor.execute(self.UPDATE_DOWNLOADED_SQL, params)
        self.conn.commit()


class Downloader:

    def __init__(self, urls_txt_path: str, scope: t.List[int]):
        self.urls_txt_path = urls_txt_path
        self.scope = scope

    @staticmethod
    def gen_download_urls(fpath):
        with open(fpath, 'r', encoding='utf8') as fp:
            for url in fp.readlines():
                yield url.replace('\n', '')

    @staticmethod
    def get_download_urls(fpath, scope) -> list:
        """
        获取urls
        :param fpath:
        :param scope: 前闭后开
        :return:
        """
        all_urls = []
        start_count, end_count = scope[0], scope[1]
        read_count = 0
        with open(fpath, 'r', encoding='utf8') as fp:
            for url in fp.readlines():
                if read_count >= end_count:
                    break
                if start_count <= read_count < end_count:
                    url = url.replace('\n', '')
                    if url:
                        all_urls.append(url)
                read_count += 1
        return all_urls

    def downloading(self, sqlite):
        for url in self.get_download_urls(self.urls_txt_path, self.scope):
            uid = cmd5(url)
            is_downloaded = sqlite.check_downloaded(uid)
            if is_downloaded:
                print(f'[{now2str()}]【已下载】{url}')
                continue
            print(f'[{now2str()}]【正在下载】{url}')
            filename = storage_dir.joinpath(url.split('/')[-1]).as_posix()
            resp = requests.get(url, stream=True)
            if resp.status_code == 401:
                print(f'[{now2str()}]【认证失败】401')
                sys.exit(1)
            try:
                resp.raise_for_status()
                with open(filename, 'wb') as fp:
                    for chunk in resp.iter_content(chunk_size=1024):
                        if chunk:
                            fp.write(chunk)
                sqlite.update_downloaded(data={
                    'uid': uid,
                    'url': url,
                    'is_succeed': 1
                })
                print(f'[{now2str()}]contents of URL written to ' + filename)
            except:
                sqlite.update_downloaded(data={
                    'uid': uid,
                    'url': url,
                    'is_succeed': 0
                })
                print(f'[{now2str()}]requests.get() returned an error code ' + str(resp.status_code))

    def run(self):
        sqlite = Sqlite()
        sqlite.init()
        self.downloading(sqlite)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=u'下载')
    parser.add_argument('--scope', '-s', required=True, type=str, help=u'下载范围(以逗号隔开，如：1,2)')
    args = parser.parse_args()
    scope = [int(i) for i in args.scope.split(',')]

    urls_path = 'download-urls.txt'
    downloader = Downloader(urls_path, scope)
    downloader.run()
