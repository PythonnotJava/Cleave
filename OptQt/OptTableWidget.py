from types import *
from json import dumps as pretty_dict
from OptQt.OptComponent import LoadingDialog
from OptQt.QTyping import QssSetter
from OptQt.AnalysisCore import ASCore
from Util.tablewidget_functions import *
from Util.common_tools import *
from Util.matrix_tools import *
from Util.tackle_datas import *

class OptTableWidget(QTableWidget, AbstractWidget):
    """
    当新的单元格被创建时，如果没有特殊声明，将会遵循以下默认的属性配置，值得注意的是，这些单元格属性可以根据传参修改\n
    - CommonTextModel：记录单元格共同的布局模式
    - CommonFont：单元格共同的字体
    - CommonCellForegroundColor：单元格共同的前景颜色
    - CommonCellBackgroundColor：单元格共同的背景颜色
    - CommonCellHightlightColor：高亮的单元格取消时，恢复到的默认颜色
    - LinkedCellStyle：链接单元格的样式表
    - SelectCellStyle：被选中的单元格的样式表
    - SpecificSignedCells：特殊的单元格交换区
    - HeaderLabels：非常重要！非常重要！非常重要！用于记录标签，大部分数据交换的中介
    - HeaderChangedSignal：非常重要！非常重要！非常重要！是用来同步各种涉及到标签操作的信号量，这里用于作用在OptTableWidget以外的控件
    """
    CommonTextModel: Qt.Alignment | Qt.AlignmentFlag = Qt.AlignCenter
    CommonFont: OptFont = OptFont().setAttributes(
        size=12,
        family='微软雅黑'
    )
    CommonCellForegroundColor = QColor(5, 5, 5)
    CommonCellBackgroundColor = QColor(240, 240, 240)
    CommonCellHightlightColor = QColor('skyblue')
    LinkedCellStyle = QssSetter(
        color=QColor('gold'),
        background_color=QColor('#e923fb'),
        border_radius=15,
        border_color=QColor('#e923fb'),
        border_width=2
    )
    SelectCellStyle = QssSetter(
        border_color=QColor('tan'),
        border_width=2,
        border_style='solid',
        color=QColor(5, 5, 5),
        background_color=QColor(240, 240, 240),
        target_with_actions='QTableWidget::item:selected'
    )
    FrozenCellStyle = QssSetter(
        background_color=QColor('gray'),
        color=QColor('cyan')
    )
    SpecificSignedCells: dict = {
        'Frozen': [],  # 冻结
        'Marked': [],  # 标记
        'Hightlighted': [],  # 高亮
        'Linked': [],  # 链接
        'Span': {}  # 合并，字典的声明方式——左上角元组 ： 右下角元组
    }
    HeaderLabels: list[str] = []
    HeaderChangedSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setUI()

    def setUI(self) -> None:
        self.horizontalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.verticalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.setFont(self.CommonFont)
        self.cellClicked.connect(self.setClickAndCreate)
        self.horizontalHeader().setCascadingSectionResizes(True)
        self.verticalHeader().setCascadingSectionResizes(True)

    def insertRow(self, row: int) -> None:
        super().insertRow(row)
        for col in range(self.columnCount()):
            self.setItem(
                row,
                col,
                OptTableItem().setWidgets(
                    textModel=self.CommonTextModel,
                    text=''
                ).setAttributes(
                    backgroundColor=self.CommonCellBackgroundColor,
                    foregroundColor=self.CommonCellForegroundColor
                )
            )

    def insertColumn(self, col: int) -> None:
        super().insertColumn(col)
        for row in range(self.rowCount()):
            self.setItem(
                row,
                col,
                OptTableItem().setWidgets(
                    textModel=self.CommonTextModel,
                    text=''
                ).setAttributes(
                    backgroundColor=self.CommonCellBackgroundColor,
                    foregroundColor=self.CommonCellForegroundColor
                )
            )

    def setHorizontalHeaderLabels(self, labels: list[str]):
        self.HeaderLabels = labels
        super().setHorizontalHeaderLabels(labels)

    def item(self, row, column) -> OptTableItem | QTableWidgetItem:
        return super().item(row, column)

    def removeColumn(self, column: int):
        super().removeColumn(column)
        self.HeaderLabels.pop(column)
        # @发射信号
        self.HeaderChangedSignal.emit()

    def setWidgets(self,
                   row: int = 5,
                   col: int = 5,
                   rowLabels: Optional[list] = None,
                   visibleGrid: bool = True,
                   # 表格的编辑模式
                   editTriggers=QAbstractItemView.DoubleClicked,
                   # 表格选中行为
                   selectBehavior=QAbstractItemView.SelectItems,
                   # 对齐模式
                   textModel=Qt.AlignCenter,
                   select_cells_border_color: QColor = QColor('tan'),
                   select_cells_border_width: int = 2,
                   select_cells_border_style: str = 'solid',
                   **kwargs
                   ) -> "OptTableWidget":
        self.baseCfg(**kwargs)
        self.setSelectionBehavior(selectBehavior)
        self.setEditTriggers(editTriggers)
        self.setColumnCount(col)
        self.setRowCount(row)
        self.setShowGrid(visibleGrid)

        if rowLabels is not None:
            self.setHorizontalHeaderLabels(rowLabels)
        else:
            rowLabels = [str(x) for x in range(1, col + 1)]
            self.setHorizontalHeaderLabels(rowLabels)
        self.HeaderLabels = rowLabels

        self.CommonTextModel = textModel
        self.SelectCellStyle.border_color = select_cells_border_color
        self.SelectCellStyle.border_width = select_cells_border_width
        self.SelectCellStyle.border_style = select_cells_border_style
        self.setStyleSheet(self.SelectCellStyle.qss)
        return self

    # 单元格菜单栏
    def setMatricxActions(self,
                          n: Union[int, str],
                          combox: QComboBox | OptComBox = None,
                          items: Optional[list[QModelIndex]] = None,
                          recoverModel: Optional[int] = None,
                          ascore : Optional[ASCore] = None
                          ) -> None:
        # 导入数据\复制
        # 行列式值 特征值 秩 奇异判断 迹 对角化 相似化
        # 正确或报错都会输出在FunctionBar的ComboBox中
        # 求和\平均值\数量（非空）\乘积\最值\中位数\众数\标准差\方差
        match n:
            case 'mark':
                self.setCellMarked(items[0].row(), items[0].column())
            case 'link':
                self.setLinkToSpecifiedCell(items[0].row(), items[0].column())
            case 'frozen':
                self.setCellFrozen(items[0].row(), items[0].column())
            case 'recover':
                if recoverModel == 1:
                    self.setMarkedCellCommon(items[0].row(), items[0].column())
                elif recoverModel == 2:
                    self.setLinkedCellRecover(items[0].row(), items[0].column())
                else:
                    pass
            case '__test':
                self.JudgeCellState(items[0].row(), items[0].column())
            case 'load':
                # dialog = LoadingDialog(
                #     getOrganizeClassify,
                #     lambda: print("Loading Success!"),
                #     lambda: print("Cancel Loading!"),
                #     self.selectionModel().selection().indexes(), self
                # ).setWidgets()
                # dialog.exec_()
                _d = getOrganizeClassify(self.selectionModel().selection().indexes(), self)
                print(pretty_dict(_d, indent=2, ensure_ascii=False))
                ascore.RegisterSignal.emit(_d)
            case 'copy':
                print('复制')
            case 'merge':
                self.setCellsMerge_test(items)
            case 0:
                combox.addItem(str(getDet(to_Matrix(items, self))))
            case 1:
                combox.addItem(str(getEigvals(to_Matrix(items, self))))
            case 2:
                combox.addItem(str(getRank(to_Matrix(items, self))))
            case 3:
                combox.addItem(str(isSparseMatrix(to_Matrix(items, self))))
            case 4:
                combox.addItem(str(getTrace(to_Matrix(items, self))))
            case 5:
                combox.addItem('对角化')
            case 6:
                combox.addItem('相似化')
            case 7:
                combox.addItem('Shape : ({}, {})'.format(*getShape(items)))
            case 'a':
                combox.addItem(str(getSumOrAge(items, self, sumMode=True)))
            case 'b':
                combox.addItem(str(getSumOrAge(items, self, sumMode=False)))
            case 'c':
                combox.addItem(str(getCount(items, self)))
            case 'd':
                combox.addItem(str(getProduct(items, self)))
            case 'e':
                combox.addItem('Min : {} Max : {}'.format(*getMinMaxValue(items, self)))
            case 'f':
                combox.addItem(str(getMedium(TackleDatas(items, self))))
            case 'g':
                combox.addItem(str(getMode(TackleDatas(items, self))))
            case 'h':
                combox.addItem(str(getStdValue(TackleDatas(items, self))))
            case 'i':
                combox.addItem(str(getVariance(TackleDatas(items, self))))

    # 列标签菜单栏
    def setHorizonActions(self,
                          n: Union[int, str],
                          col: Optional[int] = None,
                          col_s: Optional[Union[int, range]] = None,
                          lock: bool = False,
                          pos: Optional[QPoint] = None,
                          ascore : Optional[ASCore] = None
                          ) -> None:
        # 导入分析器\导出列数据\数据集修复\左侧插入一列\右侧插入一列\删除该列\升序排列\降序排列\列数据替换
        match n:
            case 0:
                # dialog = LoadingDialog(
                #     getOrganizeClassify,
                #     lambda : print("Loading Success!"),
                #     lambda : print("Cancel Loading!"),
                #     self.selectionModel().selection().indexes(), self
                # ).setWidgets()
                # dialog.exec_()
                _d = getOrganizeClassify(self.selectionModel().selection().indexes(), self)
                print(pretty_dict(_d, indent=2, ensure_ascii=False))
                ascore.RegisterSignal.emit(_d)
            case 1:
                self.exportColumn_s(col_s)
            case 2:
                print('数据集修复')
            case '3-1':
                self.setInsertToSpecifiedColumn(col)
            case '3-2':
                self.setInsertToSpecifiedColumn(col + 1)
            case 4:
                self.removeColumn(col)
            case 5:
                self.sortByColumn(col, Qt.SortOrder.AscendingOrder)
            case 6:
                self.sortByColumn(col, Qt.SortOrder.DescendingOrder)
            case 7:
                self.setColumnDatasReplaced(col)

    # 行标签菜单栏
    def setVerticalActions(self,
                           n: Union[int, str],
                           row: Optional[int] = None,
                           row_s: Optional[Union[int, range]] = None,
                           ascore : Optional[ASCore] = None
                           ) -> None:
        # 导入分析器\上面插入一行\下面插入一行\删除该行\导出行数据
        match n:
            case 0:
                # 行数据数据是不需要创建子线程和加载界面的
                _d = getOrganizeClassify(self.selectionModel().selection().indexes(), self)
                print(pretty_dict(_d, indent=2, ensure_ascii=False))
                ascore.RegisterSignal.emit(_d)
            case 1:
                self.insertRow(row)
            case 2:
                self.insertRow(row + 1)
            case 3:
                self.removeRow(row)
            case 4:
                self.exportRow_s(row_s)

    def ResetAttributes(self,
                        textModel: int | Qt.Alignment = None,
                        common_foregroundColor: QColor | QBrush | QGradient | Qt.GlobalColor = None,
                        common_backgroundColor: QColor | QBrush | QGradient | Qt.GlobalColor = None,
                        select_cells_border_color: QColor = QColor('tan'),
                        select_cells_border_width: int = 2,
                        select_cells_border_style: str = 'solid'
                        ) -> 'OptTableWidget':
        return WhenResetAttributes(self, textModel, common_foregroundColor, common_backgroundColor,
                                   select_cells_border_color, select_cells_border_width, select_cells_border_style)

    @staticmethod
    def JudgeMatrix(items: list[QModelIndex]) -> bool:
        return WhenJudgeMatrix(items)

    def setInsertToSpecifiedColumn(self, col: int) -> None:
        WhenSetInsertToSpecifiedColumn(self, col)

    def exportColumn_s(self, col_s: Union[int, range]) -> None:
        WhenExportColumn_s(self, col_s)

    def exportRow_s(self, row_s: Union[int, range]) -> None:
        WhenExportRow_s(self, row_s)

    def setColumnDatasReplaced(self, col: int) -> None:
        WhenSetColumnDatasReplaced(self, col)

    def setLinkToSpecifiedCell(self, row: int, col: int) -> None:
        WhenSetLinkToSpecifiedCell(self, row, col)

    def setClickAndCreate(self, row: int, col: int) -> None:
        WhenSetClickAndCreate(self, row, col)

    def setAllLinkedCellsRecover(self) -> None:
        WhenSetAllLinkedCellsRecover(self)

    def JudgeMarked(self, row: int, col: int) -> Literal[0, 1]:
        return WhenJudgeMarked(self, row, col)

    def JudgeLinked(self, row: int, col: int) -> Literal[0, 2]:
        return WhenJudgeLinked(self, row, col)

    def JudgeFrozen(self, row: int, col: int) -> Literal[0, 3]:
        return WhenJudgeFrozen(self, row, col)

    def setLinkedCellRecover(self, row: int, col: int) -> None:
        WhenSetLinkedCellRecover(self, row, col)

    def setCellMarked(self, row: int, col: int) -> None:
        WhenSetCellMarked(self, row, col)

    def setMarkedCellCommon(self, row: int, col: int) -> None:
        WhenSetMarkedCellCommon(self, row, col)

    def setAllMarkedCellsCommon(self) -> None:
        WhenSetAllMarkedCellsCommon(self)

    def setCellFrozen(self, row: int, col: int) -> None:
        WhenSetCellFrozen(self, row, col)

    def setFrozenCellThaw(self, row: int, col: int) -> None:
        WhenSetFrozenCellThaw(self, row, col)

    def setAllFrozenCellsThaw(self) -> None:
        WhenSetAllFrozenCellsThaw(self)

    def JudgeCellState(self, row: int, col: int) -> Literal[0, 1, 2, 3]:
        return WhenJudgeCellState(self, row, col)

    def setPointCellThaw(self) -> None:
        WhenSetPointCellThaw(self)

    # 合并单元格——慎用（没有回退功能）
    def setCellsMerge_test(self, items: List[QModelIndex]) -> None:
        WhenSetCellsMerge_test(self, items)

    def setCellsStyle(self, n: int, target: OptPushButton, toColor: bool = True) -> None:
        WhenSetCellsStyle(self, n, target, toColor)


if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        icon=QIcon(ImageType.APP_LOGO),
        display_name='OptTableWidget'
    )
    ui = OptTableWidget()
    ui.setWidgets(
        rowLabels=[str(x) for x in range(1, 101)],
        row=100,
        col=100
    )
    ui.show()
    app.exec()
