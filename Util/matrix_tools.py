"""
针对传入的list[QModelIndex]进行解析。注意的是，此处的QModelItem必须全在一个框出的矩阵中，此外，需要对元素是否为数据类型进行检测\n
到时候进行计算的时候，会出现以下的行为：\n
- 正确的输出会出现在ComboBox持续记录，也就是说，可以看到历史记录
- 错误的数据会被展示在状态栏里
"""
from typing import *

from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QTableWidget
from numpy import *
from Util.errors import ErrorCode, _ErrorCode

# 指定容忍误差范围
Tolerance = 1e-6

# 泛型
T = TypeVar("T")

# 数字类型
Number = NewType('Number', Union[int, float])

# 使用机器学习的数据预处理模型来补全，但是耗费性能
# 这是针对列或者行选中的操作的
ScientificCompletion = NewType('ScientificCompletion', str)

# 该函数核实是否全是数字类型
# 考虑到一堆连续的数据突然出现一个空值的情况，也计入数字类型
# 最简单的方式就是直接算，对于出现字符串的情景会报错，然后自定义处理
def checkNumbers(func : Callable) -> T:
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as E:
            return ErrorCode(E)
    return wrapper

# 求平均值
@checkNumbers
def getAverage(
        items : list[QModelIndex],
        table : QTableWidget,
        preprocessing : Number = 0
        ) -> Number | ErrorCode:
    _sum = 0
    _count = 0
    for item in items:
        _count += 1
        _item = table.item(item.row(), item.column())
        if _item.text() is not None and _item.text() != '':
            _sum += float(_item.text())
            _sum += preprocessing
    return _sum / _count

# 对选择的矩阵块转真正的矩阵
# 幸运的是，选中矩阵返回的List[QModelIndex]从左上角的单元格开始，到右下角的单元格结束
# 然而不幸的是，Table的每一个数据都是str，需要频繁转换
def to_Matrix(
        items : List[QModelIndex],
        table : QTableWidget,
) -> ndarray | ErrorCode:
    try:
        _row = items[-1].row() - items[0].row() + 1
        _col = items[-1].column() - items[0].column() + 1
        _matrix_list = []
        for item in items:
            _matrix_list.append(
                float(table.item(item.row(), item.column()).text())
            )
        return reshape(
            array(_matrix_list),
            newshape=[_row, _col]
        )
    except Exception as _:
        return ErrorCode(_ErrorCode(2, TypeError))

# 是否为奇异矩阵
# 仅支持方阵，源于《同济大学线性代数》第六版，下面涉及到方阵为前提的同此
@checkNumbers
def isSparseMatrix(
        _matrix : ndarray
) -> bool | ErrorCode:
    if _matrix.shape[0] == _matrix.shape[1]:
        # 有精度问题，因此采用精度容忍方式
        return abs(linalg.det(_matrix)) <= Tolerance
    else:
        raise _ErrorCode(1, ValueError)

# 行列式值
@checkNumbers
def getDet(
    _matrix : ndarray
) -> Number | ErrorCode:
    return linalg.det(_matrix)

# 方阵求迹
@checkNumbers
def getTrace(
        _matrix : ndarray
) -> Number | ErrorCode:
    if _matrix.shape[0] == _matrix.shape[1]:
        return trace(_matrix)
    else:
        raise _ErrorCode(1, ValueError)

# 求秩
@checkNumbers
def getRank(
        _matrix : ndarray
) -> int | ErrorCode:
    return linalg.matrix_rank(_matrix)

# 矩阵特征值
@checkNumbers
def getEigvals(
        _matrix : ndarray
) -> list[Number] | ErrorCode:
    if _matrix.shape[0] == _matrix.shape[1]:
        n : ndarray = linalg.eigvals(_matrix)
        return n.tolist()
    else:
        raise _ErrorCode(1, ValueError)

# 获取选中的矩阵的范围
def getShape(
        items: List[QModelIndex]
) -> [int, int]:
    return [items[-1].row() - items[0].row() + 1, items[-1].column() - items[0].column() + 1]