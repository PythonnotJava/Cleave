from typing import *
from os.path import expanduser, join
from pandas import read_csv, read_excel, DataFrame
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from OptQt.OptComponent import ReWriteInputDialog, ReWriteAnyWidgetDialog
from OptQt.ColorPalette import ColorPaletter
from OptQt.OptimizeQt import *
from Sources import *

# @self : OptTableWidget

# 重设单元格
def WhenResetAttributes(self,
                        textModel: int | Qt.Alignment = Qt.AlignCenter,
                        common_foregroundColor: QColor | QBrush | QGradient | Qt.GlobalColor = QColor('black'),
                        common_backgroundColor: QColor | QBrush | QGradient | Qt.GlobalColor = QColor(240, 240, 240),
                        select_cells_border_color: QColor = QColor('tan'),
                        select_cells_border_width: int = 2,
                        select_cells_border_style: str = 'solid'
                        ):
    for row in range(self.rowCount()):
        for col in range(self.columnCount()):
            item = self.item(row, col)
            if item is not None:
                item.setTextAlignment(textModel)
                item.setBackground(common_backgroundColor)
                item.setForeground(common_foregroundColor)
    self.CommonCellForegroundColor = common_foregroundColor
    self.CommonCellBackgroundColor = common_backgroundColor
    self.SelectCellStyle.border_color = select_cells_border_color
    self.SelectCellStyle.border_width = select_cells_border_width
    self.SelectCellStyle.border_style = select_cells_border_style
    self.setStyleSheet(self.SelectCellStyle.qss)
    return self

# 矩阵判断
def WhenJudgeMatrix(items: list[QModelIndex]) -> bool:
    size_by_shape = (
            (abs(items[0].row() - items[-1].row()) + 1) * (1 + abs(items[0].column() - items[-1].column()))
    )
    return size_by_shape == len(items) and size_by_shape >= 2

# 获取表格数据
# from OptQt.OptTableWidget import OptTableWidget
def WhenGetTableWidgetDatas(self) -> DataFrame:
    _datas : DataFrame = DataFrame(columns=self.HeaderLabels)
    for row in range(self.rowCount()):
        for col in range(self.columnCount()):
            item = self.item(row, col)
            _datas.at[row, self.HeaderLabels[col]] = item.text() if item is not None else ""
    return _datas

# -----------------------------------------------列菜单栏操作-----------------------------------------------------
# 左/右侧插入一列
def WhenSetInsertToSpecifiedColumn(self, col: int) -> None:
    dialog = ReWriteInputDialog()

    def __func(text: str):
        self.insertColumn(col)
        self.HeaderLabels.insert(col, text)
        self.setHorizontalHeaderLabels(self.HeaderLabels)
        # @发射信号
        self.HeaderChangedSignal.emit()
        dialog.close()

    dialog.setWidgets(
        title='新插入',
        labelText='列标签名称',
        modal=True,
        okBtn_function=lambda: __func(dialog.text()),
        maxh=100,
        minh=100,
        maxw=600
    )
    dialog.exec_()

# 导出列数据--为了避免各种麻烦，这次绝不复用部分代码
def WhenExportColumn_s(self, col_s: int | range) -> None:
    filePath, _ = QFileDialog.getSaveFileName(
        parent=self,
        caption='保存文件',
        directory=join(expanduser('~'), "Desktop"),
        filter="保存类型 建议xlsx(*.xlsx)\n csv(*.csv)"
    )
    if filePath is not None and filePath != '':
        _datas = DataFrame()
        label_s: list[str]
        if isinstance(col_s, int):
            label_s = [self.HeaderLabels[col_s]]
            for row in range(self.rowCount()):
                item = self.item(row, col_s)
                _datas.at[row, 0] = item.text() if item is not None else ""
        else:
            label_s = self.HeaderLabels[col_s.start : col_s.stop]
            for row in range(self.rowCount()):
                for col in col_s:
                    item = self.item(row, col - col_s.start)
                    _datas.at[row, col - col_s.start] = item.text() if item is not None else ""
        _datas.columns = label_s
        try:
            if filePath.endswith('.csv'):
                _datas.to_csv(filePath, index=False)
                MusicPlayer.play(filePath=MusicType.Success, lasting=2)
            elif filePath.endswith('.xlsx'):
                _datas.to_excel(filePath, index=False)
                MusicPlayer.play(filePath=MusicType.Success, lasting=2)
            else:
                # @Msg_Error
                print("Unsupport FileType!")
                MusicPlayer.play(filePath=MusicType.Error, lasting=2)
        except PermissionError:
            # @Msg_Error
            print("File is openning in another Process!")
            MusicPlayer.play(filePath=MusicType.Error, lasting=2)
    else:
        print("Cancel Export...")

# 列替换——只能根据导入文件的第一列，原来rowCount保持不变
# 多余的数据被省去，数据不够只能覆盖到导入数据高度
def WhenSetColumnDatasReplaced(self, col : int):
    filePath, _ = QFileDialog.getOpenFileName(
        parent=self,
        caption='选择文件',
        directory=join(expanduser('~'), "Desktop"),
        filter="选择类型 建议xlsx(*.xlsx)\n xls(*.xls)\n csv(*.csv)"
    )
    if filePath is not None and filePath != '':
        _datas : Optional[DataFrame]
        if filePath.endswith('.csv'):
            _datas = read_csv(filePath)
        elif filePath.endswith('.xlsx') or filePath.endswith('.xls'):
            _datas = read_excel(filePath, sheet_name=0)
        else:
            # @Msg_Error
            MusicPlayer.play(MusicType.Error, lasting=2)
            raise Exception("不支持的文件类型")
        if _datas is not None:
            self.HeaderLabels[col] = str(_datas.columns[0])
            self.horizontalHeaderItem(col).setText(_datas.columns[0])
            for row in range(_datas.shape[0]):
                self.setItem(
                    row,
                    col,
                    OptTableItem().setWidgets(
                        textModel=self.CommonTextModel,
                        text=str(_datas.iat[row, 0]) if str(_datas.iat[row, 0]) != 'nan' else '',
                    ).setAttributes(
                        backgroundColor=self.CommonCellBackgroundColor,
                        foregroundColor=self.CommonCellForegroundColor
                    )
                )
            # @发射信号
            self.HeaderChangedSignal.emit()
            MusicPlayer.play(filePath=MusicType.Success, lasting=2)
        else:
            # @Msg_Error
            MusicPlayer.play(MusicType.Error, lasting=2)
            raise Exception("不支持的文件类型")
    else:
        print("Cancel Replace...")

# 点击时创建--保证全部都是OptTableItem
def WhenSetClickAndCreate(self, row : int, col : int):
    if self.item(row, col) is None:
        print("New Item is Created!")
        self.setItem(
            row, col,
            OptTableItem().setWidgets(
                textModel=self.CommonTextModel,
                text='',
            ).setAttributes(
                foregroundColor=self.CommonCellForegroundColor,
                backgroundColor=self.CommonCellBackgroundColor
            )
        )
# -----------------------------------------------行菜单栏操作-----------------------------------------------------
# 导出行数据
def WhenExportRow_s(self, row_s : Union[int, range]) -> None:
    filePath, _ = QFileDialog.getSaveFileName(
        parent=self,
        caption='保存文件',
        directory=join(expanduser('~'), "Desktop"),
        filter="保存类型 建议xlsx(*.xlsx)\n csv(*.csv)"
    )
    if filePath is not None and filePath != '':
        _datas = DataFrame(columns=self.HeaderLabels)
        if isinstance(row_s, int):
            for col in range(self.columnCount()):
                item = self.item(row_s, col)
                _datas.at[row_s, self.HeaderLabels[col]] = item.text() if item is not None else ""
        else:
            for row in row_s:
                for col in range(self.columnCount()):
                    item = self.item(row, col)
                    _datas.at[row, self.HeaderLabels[col]] = item.text() if item is not None else ""
        try:
            if filePath.endswith('.xlsx'):
                _datas.to_excel(filePath, index=False)
                MusicPlayer.play(filePath=MusicType.Success, lasting=2)
            elif filePath.endswith('.csv'):
                _datas.to_csv(filePath, index=False)
                MusicPlayer.play(filePath=MusicType.Success, lasting=2)
            else:
                # @Msg_Error
                print("Unsupport FileType!")
                MusicPlayer.play(filePath=MusicType.Error, lasting=2)
        except PermissionError:
            # @Msg_Error
            print("File is openning in another Process!")
            MusicPlayer.play(filePath=MusicType.Error, lasting=2)
    else:
        print("Cancel Export...")

# ---------------------------------------------------单一单元格菜单栏-------------------------------------------------------
# 核实单元格是否被标记
def WhenJudgeMarked(self, row: int, col: int) -> Literal[0, 1]:
    item : OptTableItem = self.item(row, col)
    if item is not None and (not item.icon().isNull()):
        return 1
    else:
        return 0

# 核实单元格是否被链接
def WhenJudgeLinked(self, row: int, col: int) -> Literal[0, 2]:
    if self.cellWidget(row, col) is not None:
        return 2
    else:
        return 0

# 核实单元格是否被冻结
def WhenJudgeFrozen(self, row : int, col : int) -> Literal[0, 3]:
    item = self.item(row, col)
    if item is not None and (item.flags() == (item.flags() & ~ Qt.ItemIsEnabled)):
        return 3
    else:
        return 0

# 当一个单元格处于链接、冻结、标记三者之一，不能拥有第二种状态
# 当一个单元格被冻结，无法进行右键菜单栏展开，只能通过标记取消
# 当一个单元格被链接或者标记，可以被取消
# 当一个单元格被链接或者标记，不能二次进行链接或者标记，必须先取消然后重新设置
# 这个方法是用于判断如何展示菜单栏
# 返回值0表示普通单元格、1表示被标记单元格、2表示被链接单元格、3表示被冻结单元格
def WhenJudgeCellState(self, row : int, col : int) -> Literal[0, 1, 2, 3]:
    if self.JudgeMarked(row, col):
        print("J1")
        return 1
    elif self.JudgeLinked(row, col):
        print("J2")
        return 2
    elif self.JudgeFrozen(row, col):
        print("J3")
        return 3
    else:
        print("J0")
        return 0

# 链接
def WhenSetLinkToSpecifiedCell(self, row: int, col: int) -> None:
    linkDialog = ReWriteInputDialog()

    def __func(link: str):
        self.setCellWidget(
            row,
            col,
            OptToolButton().setWidgets(
                buttonStyle=Qt.ToolButtonStyle.ToolButtonTextBesideIcon,
                icon=ImageType.MA_Link,
                text=link,
                function=lambda: QDesktopServices.openUrl(QUrl(link)),
                tips=link,
                qss=self.LinkedCellStyle.qss
            )
        )
        self.SpecificSignedCells['Linked'].append((row, col))
        linkDialog.close()

    linkDialog.setWidgets(
        edit_minw=500,
        labelText='地址',
        okBtn_function=lambda: __func(linkDialog.text()),
        maxLen=500,
        okBtn_text='链接',
        title='输入链接',
        maxh=100,
        minh=100,
        maxw=800,
    )
    linkDialog.exec_()

# 恢复全部被链接的单元格为普通单元格
def WhenSetAllLinkedCellsRecover(self) -> None:
    lis : list = self.SpecificSignedCells['Linked']
    for r_c in lis:
        row, col = r_c
        if self.JudgeLinked(row, col):
            self.removeCellWidget(row, col)
            self.setItem(
                row,
                col,
                OptTableItem().setWidgets(
                    text='',
                    textModel=self.CommonTextModel,
                ).setAttributes(
                    foregroundColor=self.CommonCellForegroundColor,
                    backgroundColor=self.CommonCellBackgroundColor
                )
            )
    lis.clear()

# 恢复被链接的某个单元格为普通单元格
def WhenSetLinkedCellRecover(self, row: int, col: int) -> None:
    self.removeCellWidget(row, col)
    self.SpecificSignedCells['Linked'].remove((row, col))
    self.setItem(
        row,
        col,
        OptTableItem().setWidgets(
            text='',
            textModel=self.CommonTextModel,
        ).setAttributes(
            foregroundColor=self.CommonCellForegroundColor,
            backgroundColor=self.CommonCellBackgroundColor
        )
    )

# 标记一个单元格
def WhenSetCellMarked(self, row: int, col: int) -> None:
    item: Optional[OptTableItem] = self.item(row, col)
    if item is not None:
        item.setIcon(QIcon(ImageType.MA_Marked))
    else:
        self.setItem(
            row, col,
            OptTableItem().setWidgets(
                textModel=self.CommonTextModel,
                text='',
                icon=ImageType.MA_Marked
            ).setAttributes(
                foregroundColor=self.CommonCellForegroundColor,
                backgroundColor=self.CommonCellBackgroundColor
            )
        )
    self.SpecificSignedCells['Marked'].append((row, col))

# 取消一个单元格的标记
def WhenSetMarkedCellCommon(self, row: int, col: int) -> None:
    item = self.item(row, col)
    item.setIcon(QIcon())
    self.SpecificSignedCells['Marked'].remove((row, col))

# 取消全部标记单元格
def WhenSetAllMarkedCellsCommon(self) -> None:
    lis: list = self.SpecificSignedCells['Marked']
    for r_c in lis:
        if self.JudgeMarked(*r_c):
            item = self.item(*r_c)
            item.setIcon(QIcon())
    lis.clear()

# 解冻全部冻结单元格
def WhenSetAllFrozenCellsThaw(self):
    lis : list = self.SpecificSignedCells['Frozen']
    for r_c in lis:
        item : Optional[OptTableItem] = self.item(*r_c)
        if item is not None:
            item.setAttributes(
                foregroundColor=self.CommonCellForegroundColor,
                backgroundColor=self.CommonCellBackgroundColor
            ).setFlags(item.flags() | Qt.ItemIsEnabled)
    lis.clear()

# 解冻一个冻结单元格
def WhenSetFrozenCellThaw(self, row: int, col: int) -> None:
    item : OptTableItem = self.item(row, col)
    item.setAttributes(
        foregroundColor=self.CommonCellForegroundColor,
        backgroundColor=self.CommonCellBackgroundColor
    ).setFlags(item.flags() | Qt.ItemIsEnabled)
    self.SpecificSignedCells['Frozen'].remove((row, col))

# 冻结一个单元格
def WhenSetCellFrozen(self, row: int, col: int) -> None:
    item: Optional[OptTableItem] = self.item(row, col)
    if item is not None:
        item.setAttributes(
            foregroundColor=self.FrozenCellStyle.color,
            backgroundColor=self.FrozenCellStyle.background_color
        ).setFlags(item.flags() & ~Qt.ItemIsEnabled)
    else:
        item = OptTableItem().setWidgets(
            textModel=self.CommonTextModel,
            text=''
        ).setAttributes(
            foregroundColor=self.FrozenCellStyle.color,
            backgroundColor=self.FrozenCellStyle.background_color
        )
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        self.setItem(row, col, item)
    item.setSelected(False)
    self.SpecificSignedCells['Frozen'].append((row, col))

# 选中一个单元格并且解冻——无论单元格是不是已被冻结
def WhenSetPointCellThaw(self) -> None:
    def __func(item):
        if item is not None and self.JudgeFrozen(item.row(), item.column()):
            WhenSetFrozenCellThaw(self, item.row(), item.column())
        QApplication.restoreOverrideCursor()
        self.itemClicked.disconnect()
    QApplication.setOverrideCursor(QCursor(QPixmap(ImageType.MA_Cross).scaledToHeight(40).scaledToWidth(40)))
    self.itemClicked.connect(__func)

# 合并单元格——慎用（没有回退功能）
# @test
def WhenSetCellsMerge_test(self, items : List[QModelIndex]) -> None:
    spans = (items[0].row(),
             items[0].column(),
             (abs(items[0].row() - items[-1].row()) + 1),
             (1 + abs(items[0].column() - items[-1].column()))
             )
    self.setSpan(*spans)

# -------------------------------------------------------------------------------------------------------
# 单元格样式调整
def WhenSetCellsStyle(self, n: int, target : OptPushButton, toColor : bool = True) -> None:
    # 要做三件同步
    # - 按钮本身颜色同步
    # - 属性同步
    # - 相关单元格同步
    if toColor:
        colorPaletter = ColorPaletter()
        match n:
            case 0:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.CommonCellBackgroundColor = colorPaletter.Color
                    for row in range(self.rowCount()):
                        for col in range(self.columnCount()):
                            if self.item(row, col) is not None: self.item(row, col).setBackground(colorPaletter.Color)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.CommonCellBackgroundColor,
                    confirm_function=__func
                )
            case 1:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.CommonCellForegroundColor = colorPaletter.Color
                    for row in range(self.rowCount()):
                        for col in range(self.columnCount()):
                            if self.item(row, col) is not None: self.item(row, col).setForeground(colorPaletter.Color)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.CommonCellForegroundColor,
                    confirm_function=__func
                )
            case 2:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.CommonCellHightlightColor = colorPaletter.Color
                    for item in self.SpecificSignedCells['Hightlighted']:
                        try: item.setData(Qt.BackgroundRole, self.CommonCellBackgroundColor)
                        except RuntimeError: pass
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.CommonCellHightlightColor,
                    confirm_function=__func
                )
            case 3:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.SelectCellStyle.color = colorPaletter.Color
                    self.setStyleSheet(self.SelectCellStyle.qss)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.SelectCellStyle.color,
                    confirm_function=__func
                )
            case 4:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.SelectCellStyle.background_color = colorPaletter.Color
                    self.setStyleSheet(self.SelectCellStyle.qss)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.SelectCellStyle.background_color,
                    confirm_function=__func
                )
            case 5:
                def __func():
                    target.setStyleSheet(f'border : 5px solid {colorPaletter.name()}')
                    self.SelectCellStyle.border_color = colorPaletter.Color
                    self.setStyleSheet(self.SelectCellStyle.qss)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.SelectCellStyle.border_color,
                    confirm_function=__func
                )
            case 6:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.LinkedCellStyle.color = colorPaletter.Color
                    for r_c in self.SpecificSignedCells['Linked']:
                        widget: Optional[QWidget] = self.cellWidget(*r_c)
                        if widget is not None:
                            widget.setStyleSheet(self.LinkedCellStyle.qss)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.LinkedCellStyle.color,
                    confirm_function=__func
                )
            case 7:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.LinkedCellStyle.background_color = colorPaletter.Color
                    for r_c in self.SpecificSignedCells['Linked']:
                        widget: Optional[QWidget] = self.cellWidget(*r_c)
                        if widget is not None:
                            widget.setStyleSheet(self.LinkedCellStyle.qss)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.LinkedCellStyle.background_color,
                    confirm_function=__func
                )
            case 8:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.LinkedCellStyle.border_color = colorPaletter.Color
                    for r_c in self.SpecificSignedCells['Linked']:
                        widget: Optional[QWidget] = self.cellWidget(*r_c)
                        if widget is not None:
                            widget.setStyleSheet(self.LinkedCellStyle.qss)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.LinkedCellStyle.border_color,
                    confirm_function=__func
                )
            case 9:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.FrozenCellStyle.color = colorPaletter.Color
                    for r_c in self.SpecificSignedCells['Frozen']:
                        if self.JudgeFrozen(*r_c):
                            self.item(*r_c).setForeground(colorPaletter.Color)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.FrozenCellStyle.color,
                    confirm_function=__func
                )
            case 10:
                def __func():
                    target.setStyleSheet(f'background-color : {colorPaletter.name()}')
                    self.FrozenCellStyle.background_color = colorPaletter.Color
                    for r_c in self.SpecificSignedCells['Frozen']:
                        if self.JudgeFrozen(*r_c):
                            self.item(*r_c).setBackground(colorPaletter.Color)
                    colorPaletter.close()
                colorPaletter.setWidgets(
                    initial=self.FrozenCellStyle.background_color,
                    confirm_function=__func
                )
        colorPaletter.exec()
    else:
        intSpin = QSpinBox()
        intSpin.setMinimum(0)
        intSpin.setMaximum(10),
        intSpin.setSingleStep(1)
        intDialog = ReWriteAnyWidgetDialog()
        match n:
            case 0:
                intSpin.setValue(self.SelectCellStyle.border_width)
                def __func():
                    target.setText(str(intSpin.value()))
                    self.SelectCellStyle.border_width = intSpin.value()
                    self.setStyleSheet(self.SelectCellStyle.qss)
                    intDialog.close()
                intDialog.setWidgets(
                    title='调整边框宽度',
                    modal=True,
                    labelText='宽度',
                    widget=intSpin,
                    fixSize=(300, 120),
                    okBtn_function=__func
                )
            case 1:
                intSpin.setValue(self.LinkedCellStyle.border_width)
                def __func():
                    target.setText(str(intSpin.value()))
                    self.LinkedCellStyle.border_width = intSpin.value()
                    for r_c in self.SpecificSignedCells['Linked']:
                        widget : Optional[QWidget] = self.cellWidget(*r_c)
                        if widget is not None:
                            widget.setStyleSheet(self.LinkedCellStyle.qss)
                    intDialog.close()
                intDialog.setWidgets(
                    title='调整边框宽度',
                    modal=True,
                    labelText='宽度',
                    widget=intSpin,
                    fixSize=(300, 120),
                    okBtn_function=__func
                )
        intDialog.exec()