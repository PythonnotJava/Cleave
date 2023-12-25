"""
梳理数据\n
- 分为行梳理和列梳理
行细分
- 单行导入
列细分
- 单列导入
- 多列导入
"""
from collections import defaultdict
from typing import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from OptQt.OptTableWidget import OptTableWidget

T = TypeVar("T")

# 检查一个数据是否是数字并转换为数字，否则保持字符串形式
def checkData(data : str) -> Literal[0, 1, 2]:
    if data.isdigit():
        return 0
    else:
        try:
            float(data)
            return 1
        except ValueError:
            return 2

# Datas把数据输出为如下形式，其实质就是未经可视化的histogram
# 如果行标签不存在将会被命名为UnNamed + (列数 + 1)
"""
{
    "Type1" : [2, 6, 3, .8],
    "Type2" : [6, 0, 2, .01],
    "Type2_string" : ["A", "null", "B", "1.02.5", "名字"],
    "UnNamed1" : [3, 2, 6, 9, 4, 5],
    ...
}
"""

# 根据传入的数据整理成行标签的分类的字典，分为6个主键值对
# Datas、StringDataPosition、DataCounts、StringDataCounts NullDataCounts、NumberCounts
# Datas把数据输出为如下形式，其实质就是未经可视化的histogram
# 如果单元格数据不存在会被记录为（null字符串），所以请提前使用数据修复器把数据修复好
# 同种标签下不存在的数据以及字符串数据会被分开标识为两种数据，一类是数字类标签（保持原标签名称），另一种是字符串类标签（原标签_string）
# 如果行标签不存在将会被命名为UnNamed + (列数 + 1)
# DataCountsPosition记录了非空数据和空数据（null）的位置
# DataCounts记录了包含多少数据
# StringDataCounts记录了包含非数字数据（空数据会被记为字符串）
# NullDataCounts记录了包含空数据个数
# NumberCounts记录了包含多少个数字型数据
# 下面是一个输出案例
"""
{
  "Datas" : {
    "Type1" : [2, 6, 3, 0.8],
    "Type2" : [6, 0, 2, 0.01],
    "Type2_string" : ["A", "null", "B", "1.02.5", "名字"],
    "UnNamed1" : [3, 2, 6, 9, 4, 5],
    "UnNamed1_string" : ["QQ", "null", "2.0.0", "II"],
    ...
  },
  "StringDataPosition" : {
    "A" :  [["Type2", 7]],
    "QQ" : [["UnNamed1", 2]],
    "名字" : [["标签坐标", "行坐标"]],
    "null" : [["UnNamed1", 65], ["Type2", 5]],
    ...
  },
  "DataCounts" : "xxx",
  "StringDataCounts" : "xxx",
  "NullDataCounts" : "xxx",
  "NumberCounts" : "xxx"
}
"""

def getOrganizeClassify(items: List[QModelIndex], table) -> Dict[str, Any]:
    _dict = defaultdict(list)
    _pos = defaultdict(list)
    _count = 0
    _s_count = 0
    _n_count = 0
    _num_count = 0
    cell : str
    for _item in items:
        row, col = _item.row(), _item.column()
        headLabel = table.HeaderLabels[col] if col < len(table.HeaderLabels) else f'UnNamed{row}'
        if table.item(row, col) is not None and table.item(row, col).text() != '':
            cell = table.item(row, col).text()
        else:
            cell = 'null'
            _n_count += 1

        if checkData(cell) == 0:  # 是数
            _dict[headLabel].append(int(cell))
            _num_count += 1
        elif checkData(cell) == 1:  # 是数
            _dict[headLabel].append(float(cell))
            _num_count += 1
        elif checkData(cell) == 2:  # 不是数
            _dict[f"{headLabel}_string"].append(cell)
            _pos[cell].append([headLabel, row])
            _s_count += 1
        _count += 1
    _return_dict: Dict[str, Any] = {
        "Datas": dict(_dict),
        "StringDataPosition": dict(_pos),
        "NumberCounts" : _num_count,
        "DataCounts": _count,
        "StringDataCounts" : _s_count,
        "NullDataCounts" : _n_count
    }
    return _return_dict