"""
普通的工具\n
"""
from typing import *
from numpy import *

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTableWidget
from Util.matrix_tools import Number, checkNumbers
from Util.errors import ErrorCode, _ErrorCode

T = TypeVar('T')

# 求和和求平均值
@checkNumbers
def getSumOrAge(
        items: list[QModelIndex],
        table: QTableWidget,
        preprocessing : Number = 0,
        sumMode : bool = True
) -> Number | ErrorCode:
    _sum = 0
    _count = 0
    for item in items:
        _count += 1
        _item = table.item(item.row(), item.column())
        if _item.text() is not None and _item.text() != '':
            _sum += float(_item.text())
        else:
            _sum += preprocessing
    return _sum if sumMode else _sum / _count

# 计数
def getCount(
        items : list[QModelIndex],
        table : QTableWidget
) -> int:
    _c = 0
    for item in items:
        _item = table.item(item.row(), item.column())
        if _item is not None and _item != '':
            _c += 1
    return _c

# 乘积
def getProduct(
        items: list[QModelIndex],
        table: QTableWidget,
        preprocessing : Number = 1
) -> Number | ErrorCode:
    try:
        _p = 1
        for item in items:
            _item = table.item(item.row(), item.column())
            if _item.text() is not None and _item.text() != '':
                _p *= float(_item.text())
            else:
                _p *= preprocessing
        return _p
    except Exception as _:
        return ErrorCode(_ErrorCode(2, ValueError))

# 最值
@checkNumbers
def getMinMaxValue(
        items: list[QModelIndex],
        table: QTableWidget
) -> list | ErrorCode:
    _min = _max = float(table.item(0, 0).text())
    for item in items[1:]:
        data = float(table.item(item.row(), item.column()).text())
        if data < _min:
            _min = data
        if data > _max:
            _max = data
    return [_min, _max]


# 数据整合为一维（包含数值类以及其他）
# 空值会被跳过
def TackleDatas(
        items: list[QModelIndex],
        table: QTableWidget
) -> Generator | ErrorCode:
    for item in items:
        _ = table.item(item.row(), item.column())
        if _.text() is not None and _ != '':
            yield _.text()

# 中位数
@checkNumbers
def getMedium(
        lis: Generator
) -> Number | ErrorCode:
    return median(array(lis))

# 众数
@checkNumbers
def getMode(
        lis : Generator
) -> Number | ErrorCode:
    return argmax(bincount(array(lis)))

# 标准差
@checkNumbers
def getStdValue(
        lis : Generator
) -> Number | ErrorCode:
    return std(array(lis))

# 方差
@checkNumbers
def getVariance(
        lis : Generator
) -> Number | ErrorCode:
    return var(array(lis))

