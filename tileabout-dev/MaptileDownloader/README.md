# MapTileDownloader

### 介绍
- 地图瓦片下载器

### 使用
- 1）安装python环境
- 2）安装python依赖
    - pip install -r requirements.txt
- 3）修改下载瓦片类型
    - 修改文件config.py内的 MAPSTYLE，如：MAPSTYLE = 'vec_w'
- 4）运行
    - 查看帮助：python main.py -h
    - python main.py --storename=${STORENAME} --bounds=${BOUNDS} --levels=${LEVELS}
    - 如：
        - python main.py --storename=tiantidu --bounds=73.33,53.3,135.05,3.51 --levels=1,1
        - python main.py --storename=google --bounds=73.33,53.3,135.05,3.51 --levels=1,1
- 5）操作使用
```text
usage: main.py [-h] --storename STORENAME --bounds BOUNDS [--levels LEVELS] [--zxy ZXY] [--mbtiles MBTILES] [--redownload]
               [--max_tries MAX_TRIES]

地图瓦片下载

optional arguments:
  -h, --help                            show this help message and exit
  --storename STORENAME, -s STORENAME   瓦片仓库名称, 如：tianditu
  --bounds BOUNDS, -b BOUNDS            经纬范围(左经度,上纬度,右经度,下纬度)，如：100,40,120,20
  --levels LEVELS, -l LEVELS            层级范围(最小层级,最大层级)，如：1,2
  --zxy ZXY                             具体层级坐标(层级,min_x,max_x,min_y,max_y)，如：9,360,448,166,251。若层级范围传值，则该参数自动忽略
  --mbtiles MBTILES                     mbtiles文件（也可指定已存在的mbtiles）
  --redownload                          是否重新下载(自动下载数据库中为空的记录)
  --max_tries MAX_TRIES                 最大重试次数
```
