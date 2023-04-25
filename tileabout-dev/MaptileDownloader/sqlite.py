"""
@author axiner
@version v1.0.0
@created 2022/10/22 13:06
@abstract sqlite操作
@description
@history
"""
import sqlite3
import argparse
from pathlib import Path


class Sqlite:

    COUNT_ALL_SQL = 'select count(zoom_level) from tiles'
    COUNT_NULL_SQL = 'select count(zoom_level) from tiles where tile_data is null'
    COUNT_GROUP_SQL = 'select zoom_level, count(zoom_level) from tiles group by zoom_level'

    def __init__(self, base_db):
        self.base_db = base_db
        self.conn = sqlite3.connect(base_db)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, sql):
        """查询"""
        sql = self.map_sqls(sql)
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        if raws:
            print('++++++++++')
            print('||'.join([col[0] for col in self.cursor.description]))
            for r in raws:
                print(r)
            print('+++++\nDONE!')
        else:
            print('所查询数据为空!')

    def merge_tiles(self, from_dbs):
        """合并tiles"""
        for index, db in enumerate(from_dbs):
            print(f'【开始合并】从 {db} 到 {self.base_db} (这可能需要一些时间 请等待...)')
            db_as_name = f'db_{index}'
            try:
                self.conn.execute("ATTACH DATABASE ? AS ?", (db, db_as_name))
                self.conn.execute("INSERT INTO tiles SELECT * FROM {dbname}".format(dbname=f'{db_as_name}.tiles'))
                self.conn.commit()
                print(f'【完成合并】{db}')
            except Exception:
                self.conn.close()
                raise
        print(f'所有合并完成!!!')

    def map_sqls(self, key):
        sqls = {
            'all': self.COUNT_ALL_SQL,
            'null': self.COUNT_NULL_SQL,
            'group': self.COUNT_GROUP_SQL,
        }
        r = sqls.get(key)
        if not r:
            raise ValueError(f'{key} SQL未配置')
        return r


def valid_args(args):
    """校验参数"""
    db = args.db
    cmd = args.cmd
    param = args.param
    if not Path(db).exists():
        raise ValueError(f'{db} 不存在')
    if cmd not in ['query', 'merge']:
        raise ValueError(f'cmd 只支持 query, merge')
    if cmd == 'merge':
        param = param.split(',')
        for dbpath in param:
            if not Path(dbpath).exists():
                raise ValueError(f'{dbpath} 不存在')
    return {
        'db': db,
        'cmd': cmd,
        'param': param
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SQLITE相关操作')
    parser.add_argument('--db', '-d', required=True, help='数据库文件')
    parser.add_argument('--cmd', '-c', required=True, help='操作命令(query: 查询，merge: 合并)')
    parser.add_argument('--param', '-p', required=True, help='操作参数(查询命令(all|null|group)或合并数据文件)')
    # 参数处理
    args = valid_args(parser.parse_args())
    # 执行操作
    sqlite = Sqlite(args.get('db'))
    if args.get('cmd') == 'query':
        sqlite.query(args.get('param'))
    else:
        sqlite.merge_tiles(args.get('param'))
    sqlite.close()
