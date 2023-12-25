# Util是辅助为主的工具类包
from os import PathLike
from json import load, dump
from inspect import signature
from typing import *
from Util.orders import about, getInfos

from Util.plugins_loader import PluginsLoader
from Util.errors import FileLoadError, ErrorCode, _ErrorCode
from Util.matrix_tools import (
    checkNumbers,
    getAverage,
    to_Matrix,
    isSparseMatrix,
    getDet,
    getTrace,
    getRank,
    getEigvals,
    getShape,
    Number,
    Tolerance,
    ScientificCompletion
)

from Util.common_tools import (
    getSumOrAge,
    getProduct,
    getMinMaxValue,
    getMedium,
    TackleDatas,
    getMode,
    getStdValue,
    getVariance,
    getCount
)

from Util.tablewidget_functions import (
    WhenJudgeMatrix,
    WhenResetAttributes,
    WhenGetTableWidgetDatas,
    WhenSetInsertToSpecifiedColumn,
    WhenExportColumn_s,
    WhenExportRow_s,
    WhenSetColumnDatasReplaced,
    WhenSetLinkToSpecifiedCell,
    WhenSetAllLinkedCellsRecover,
    WhenSetAllMarkedCellsCommon,
    WhenSetClickAndCreate,
    WhenSetAllFrozenCellsThaw,
    WhenSetFrozenCellThaw,
    WhenSetCellFrozen,
    WhenSetMarkedCellCommon,
    WhenSetCellMarked,
    WhenSetLinkedCellRecover,
    WhenJudgeMarked,
    WhenJudgeLinked,
    WhenJudgeFrozen,
    WhenJudgeCellState,
    WhenSetPointCellThaw,
    WhenSetCellsMerge_test,
    WhenSetCellsStyle
)

from Util.excelkernel_functions import (
    WhenSetAdjustAlignment,
    WhenSetSliderToCells,
    WhenSetAdjustFont,
    WhenJustLoadFilesToTable,
    WhenSetItemsByFileLoader,
    WhenJustSave,
    WhenSetSaveModel,
    WhenSetCurrentCellByJump,
    WhenSetMatchCellsBackgroundColor,
    WhenSetMatchCellsShown,
    WhenSetMatchCellsRecover,
    WhenSetFormatMenu
)

from Util.tackle_datas import (
    checkData,
    getOrganizeClassify
)

# 判断函数是否有以下参数
def has_parameter(func: Callable, param_name: str):
    try:
        _signature = signature(func)
        return param_name in _signature.parameters
    except ValueError:
        return False


def QSSLoader(file: Union[PathLike, str]) -> str:
    _f = open(file, 'r', encoding='U8')
    data = _f.read()
    _f.close()
    return data


def json_load(file: Union[PathLike, str]) -> dict:
    return load(open(file, 'r', encoding='U8'))


def json_dump(data: dict, file) -> None:
    dump(data, open(file, 'w', encoding='U8'))

def whatthis(*, msg : str):
    def decorate(cls):
        setattr(cls, 'msg', msg)
        setattr(cls, 'getMsg', lambda : cls.msg)
        return cls
    return decorate

__all__ = [
    'has_parameter',
    'QSSLoader',
    'json_dump',
    'json_load',
    'whatthis',
    'PluginsLoader',
    'FileLoadError',
    'checkNumbers',
    'getAverage',
    'to_Matrix',
    'isSparseMatrix',
    'getDet',
    'getTrace',
    'getRank',
    'about',
    'getInfos',
    'getEigvals',
    '_ErrorCode',
    'getShape',
    'Number',
    'Tolerance',
    'ScientificCompletion',
    'getSumOrAge',
    'getProduct',
    'getMinMaxValue',
    'getMedium',
    'TackleDatas',
    'getMode',
    'getStdValue',
    'getVariance',
    'getCount',
    'WhenJudgeMatrix',
    'WhenResetAttributes',
    'WhenSetAdjustAlignment',
    'WhenSetSliderToCells',
    'WhenSetAdjustFont',
    'WhenSetItemsByFileLoader',
    'WhenJustLoadFilesToTable',
    'WhenGetTableWidgetDatas',
    'WhenSetSaveModel',
    'WhenJustSave',
    'WhenSetCurrentCellByJump',
    'WhenSetMatchCellsBackgroundColor',
    'WhenSetMatchCellsShown',
    'WhenSetMatchCellsRecover',
    'WhenSetInsertToSpecifiedColumn',
    'WhenExportColumn_s',
    'WhenExportRow_s',
    'WhenSetColumnDatasReplaced',
    'WhenSetLinkToSpecifiedCell',
    'WhenSetAllLinkedCellsRecover',
    'WhenSetAllMarkedCellsCommon',
    'WhenSetClickAndCreate',
    'WhenSetAllFrozenCellsThaw',
    'WhenSetFrozenCellThaw',
    'WhenSetCellFrozen',
    'WhenSetMarkedCellCommon',
    'WhenSetCellMarked',
    'WhenSetLinkedCellRecover',
    'WhenJudgeMarked',
    'WhenJudgeLinked',
    'WhenJudgeFrozen',
    'WhenJudgeCellState',
    'WhenSetPointCellThaw',
    'WhenSetCellsMerge_test',
    'getOrganizeClassify',
    'WhenSetCellsStyle',
    'WhenSetFormatMenu',
    'checkData'
]
