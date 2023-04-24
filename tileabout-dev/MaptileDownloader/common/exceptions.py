"""
@author axiner
@version v1.0.0
@created 2022/10/20 16:33
@abstract 异常模块
@description
@history
"""


class CustomException(Exception):
    """自定义异常基类"""


class FailedError(CustomException):
    """操作失败"""


class ParamsError(CustomException):
    """参数错误"""


class LoadTileModError(CustomException):
    """加载tile模块失败"""


class MapstyleError(CustomException):
    """地图类型错误"""
