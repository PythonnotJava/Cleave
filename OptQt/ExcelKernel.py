# Excel内核
from OptQt.OptComponent import SearchBar, StatusBarWithSlider
from OptQt.OptTabs import Navigator
from OptQt.AnalysisCore import ASCore
from OptQt.ChartsBoard import ASChartBox
from OptQt.OptTableWidget import OptTableWidget
from OptQt.AdvancedTools import AdtDlg
from OptQt.UtilForTestUI import UTUI
from Util.excelkernel_functions import *
from Sources import ImageType, CursorType

# excel核心
class ExcelKernel(QMainWindow, AbstractWidget):
    """
    有动画效果的弹窗\n
    - GlobalAnimationType：动画弹出类型
    >> 0：从某点开始放大并同时移动到某个位置的动画\n
    >> 1：从某点开始向四周扩散的动画\n
    >> 2：从某位置创建完成后整体弹射出来的动画\n
    """
    GlobalAnimationType: int = 0

    def __init__(self, GlobalAnimationType: int = 0):
        super().__init__()
        self.GlobalAnimationType = GlobalAnimationType
        self.DrapableDockAScore = OptDock()
        self.DrapableDockAttributeCore = OptDock()
        self.DropCoreWidgetAS = ASChartBox()
        self.DropCoreWidgetAT = ASCore()

        self.OprBar = Navigator()
        self.TableWidget = OptTableWidget()
        self.MidSplitter = OptSplitter()
        self.StatusWidget = StatusBarWithSlider()
        self.SearchBar = SearchBar()
        self.UtilUI = UTUI()

        self.setUI()

    def setUI(self):
        self.TableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.TableWidget.customContextMenuRequested.connect(self.setItemMouseMenuActions)

        ver: QHeaderView = self.TableWidget.verticalHeader()
        hor: QHeaderView = self.TableWidget.horizontalHeader()
        ver.setContextMenuPolicy(Qt.CustomContextMenu)
        hor.setContextMenuPolicy(Qt.CustomContextMenu)
        ver.customContextMenuRequested.connect(self.setVerticalLabelsMouseMenuActions)
        hor.customContextMenuRequested.connect(self.setHorizontalLabelsMouseMenuActions)

        # 界面直接相关
        keys_AsCore = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_E), self)
        keys_Attr = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_R), self)
        keys_Search = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        keys_AdtTools = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_T), self)
        keys_UtilUI = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_U), self)

        keys_Attr.activated.connect(
            lambda: self.DrapableDockAttributeCore.setVisible(not self.DrapableDockAttributeCore.isVisible())
        )
        keys_AsCore.activated.connect(
            lambda: self.DrapableDockAScore.setVisible(not self.DrapableDockAScore.isVisible())
        )

        keys_Search.activated.connect(lambda: self.SearchBar.setVisible(not self.SearchBar.isVisible()))
        keys_AdtTools.activated.connect(self.OpenADTools)
        keys_UtilUI.activated.connect(lambda: self.UtilUI.setVisible(not self.UtilUI.isVisible()))

        # 功能
        Keys_RecoverHighlightCells = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_C), self)
        Keys_RecoverLinkedCells = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_G), self)
        Keys_RecoverMarkedCells = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_M), self)
        Keys_RecoverFrozenCells = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_O), self)

        Keys_RecoverHighlightCells.activated.connect(self.setMatchCellsRecover)
        Keys_RecoverLinkedCells.activated.connect(self.TableWidget.setAllLinkedCellsRecover)
        Keys_RecoverMarkedCells.activated.connect(self.TableWidget.setAllMarkedCellsCommon)
        Keys_RecoverFrozenCells.activated.connect(self.TableWidget.setAllFrozenCellsThaw)

    def setWidgets(self,
                   familys: Iterable = ('微软雅黑', '华文行楷', '宋体', '楷书', '黑体'),
                   sizes: Iterable = (8, 12, 16, 18, 24),
                   **kwargs
                   ):
        self.TableWidget.setWidgets(
            objectName='QE-TableWidget',
            cursor=CursorType.Table,
        )

        self.SearchBar.setWidgets(
            objectName='SearchBar',
            maxh=150,
            modal=True,
            maxw=800,
            cursor=CursorType.Busy,
            defaultSets=True,
            title='单元格搜索',
            icon=QIcon(ImageType.MA_Search),
            hightlightColor=QColor('skyblue'),
            search_model=0,
            hightlight_funciton=self.setMatchCellsBackgroundColor,
            confirm_function=self.setMatchCellsShown
        )

        self.StatusWidget.setWidgets(
            objectName='QE-StatusWidget',
            statusTip='已就绪',
            maxh=30,
            cursor=CursorType.Busy,
            defautltSets=True,
            slider_function=self.setSliderToCells
        )

        self.DrapableDockAScore.setWidgets(
            objectName='DrapableDockAScore',
            insiderWidget=self.DropCoreWidgetAS.setWidgets(
                objectName='QE-DropCoreWidgetAS',
            ),
            minh=300,
            minw=300,
            cursor=CursorType.Busy,
            title="图表",
        ).setBeautifulEdgeShadow(
            color=Qt.red,
            offset=(5, 5)
        )

        self.DrapableDockAttributeCore.setWidgets(
            objectName='DrapableDockAttributeCore',
            insiderWidget=self.DropCoreWidgetAT.setWidgets(
                objectName='QE-DropCoreWidgetAT',
            ),
            minh=300,
            minw=300,
            cursor=CursorType.Busy,
            title="分析器"
        ).setBeautifulEdgeShadow(
            color=Qt.blue,
            offset=(5, 5)
        )

        self.MidSplitter.setWidgets(
            widgets=[self.OprBar, self.TableWidget],
            objectName='QE-MidSplitter',
            horizontal=False,
            handleIndex=1,
            handleCursor=CursorType.Move,
            handleWidth=10,
            collapsible=True,
        )

        self.OprBar.setWidgets(
            familys=familys,
            sizes=sizes,
            objectName='QE-OprBar',
            maxh=300,
            cursor=CursorType.Busy,
            align_left_function=lambda: self.setAdjustAlignment(Qt.AlignLeft | Qt.AlignVCenter),
            align_center_function=lambda: self.setAdjustAlignment(Qt.AlignCenter),
            align_right_function=lambda: self.setAdjustAlignment(Qt.AlignRight | Qt.AlignVCenter),
            font_size_function=lambda: self.setAdjustFont('s'),
            font_family_function=lambda: self.setAdjustFont('f'),
            open_function=self.setItemsByFileLoader,
            just_save_function=lambda: self.setSaveModel(justSave=True),
            save_as_function=lambda: self.setSaveModel(justSave=False),
            jump_function=self.setCurrentCellByJump,
            thaw_function=self.TableWidget.setPointCellThaw,
            format_function=self.setFormatMenu
        )

        self.UtilUI.setWidgets(
            minh=600,
            minw=600,
            objectName='QE-UtilUI',
            cursor=CursorType.Working
        )

        self.TableWidget.CellHightlightColor = QColor('skyblue')
        # @接收信号
        self.TableWidget.HeaderChangedSignal.connect(self.setHeaderChangedSignalCore)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.DrapableDockAttributeCore)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.DrapableDockAScore)
        self.setDockOptions(self.dockOptions() | QMainWindow.DockOption.AllowTabbedDocks)
        self.setDockNestingEnabled(True)
        self.tabifyDockWidget(self.DrapableDockAttributeCore, self.DrapableDockAScore)
        self.setCentralWidget(self.MidSplitter)
        self.setStatusBar(self.StatusWidget)
        self.baseCfg(**kwargs)

        return self

    # 打开高级工具
    def OpenADTools(self, currentIndex: int = 0) -> None:
        AdvancedTools = AdtDlg()
        AdvancedTools.setWidgets(
            currentIndex=currentIndex,
            fixSize=(600, 600),
            objectName='AdvancedTools',
            modal=True,
            title='高级设置',
            icon=ImageType.MA_Advanced_Tools,
            common_backgroundcolor=self.TableWidget.CommonCellBackgroundColor,
            common_foregroundcolor=self.TableWidget.CommonCellForegroundColor,
            common_hightlightColor=self.TableWidget.CommonCellHightlightColor,
            linkedCellStyle=self.TableWidget.LinkedCellStyle,
            selectCellStyle=self.TableWidget.SelectCellStyle,
            frozenCellStyle=self.TableWidget.FrozenCellStyle,
            global_background_color_function=lambda: self.TableWidget.setCellsStyle(
                0, AdvancedTools.CellManager.GlobalBackgroundColorBtn, True
            ),
            global_foreground_color_function=lambda: self.TableWidget.setCellsStyle(
                1, AdvancedTools.CellManager.GlobalForegroundColorBtn, True
            ),
            global_highlight_color_function=lambda: self.TableWidget.setCellsStyle(
                2, AdvancedTools.CellManager.GlobalHighlightColorBtn, True
            ),
            select_foreground_color_function=lambda: self.TableWidget.setCellsStyle(
                3, AdvancedTools.CellManager.SelectForegroundColorBtn, True
            ),
            select_background_color_function=lambda: self.TableWidget.setCellsStyle(
                4, AdvancedTools.CellManager.SelectBackgroundColorBtn, True
            ),
            select_border_width_function=lambda: self.TableWidget.setCellsStyle(
                0, AdvancedTools.CellManager.SelectBorderWidthBtn, False
            ),
            select_border_color_function=lambda: self.TableWidget.setCellsStyle(
                5, AdvancedTools.CellManager.SelectBorderColorBtn, True
            ),
            link_foreground_color_function=lambda: self.TableWidget.setCellsStyle(
                6, AdvancedTools.CellManager.LinkForegroundColorBtn, True
            ),
            link_background_color_function=lambda: self.TableWidget.setCellsStyle(
                7, AdvancedTools.CellManager.LinkBackgroundColorBtn, True
            ),
            link_border_width_function=lambda: self.TableWidget.setCellsStyle(
                1, AdvancedTools.CellManager.LinkBorderWidthBtn, False
            ),
            link_border_color_function=lambda: self.TableWidget.setCellsStyle(
                8, AdvancedTools.CellManager.LinkBorderColorBtn, True
            ),
            frozen_foreground_color_function=lambda: self.TableWidget.setCellsStyle(
                9, AdvancedTools.CellManager.FrozenForegroundColorBtn, True
            ),
            frozen_background_color_function=lambda: self.TableWidget.setCellsStyle(
                10, AdvancedTools.CellManager.FrozenBackgroundColorBtn, True
            )
        )
        AdvancedTools.exec_()

    # 单元格菜单栏
    def setItemMouseMenuActions(self, pos: QPoint):
        modelItems: list[QModelIndex] = self.TableWidget.selectionModel().selection().indexes()
        menu = OptMenu(self)
        if len(modelItems) == 1:
            row_col: tuple = modelItems[0].row(), modelItems[0].column()
            menu.JustActions(
                title="",
                actions=[
                    OptAction().setWidgets(
                        parent=menu,
                        text='标记',
                        function=lambda: self.TableWidget.setMatricxActions('mark', items=modelItems),
                        enable=(self.TableWidget.JudgeCellState(*row_col) == 0)
                    ),
                    OptAction().setWidgets(
                        parent=menu,
                        text="链接",
                        function=lambda: self.TableWidget.setMatricxActions('link', items=modelItems),
                        enable=(self.TableWidget.JudgeCellState(*row_col) == 0)
                    ),
                    OptAction().setWidgets(
                        parent=menu,
                        text="冻结",
                        function=lambda: self.TableWidget.setMatricxActions('frozen', items=modelItems),
                        enable=(self.TableWidget.JudgeCellState(*row_col) == 0)
                    ),
                    OptAction().setWidgets(
                        parent=menu,
                        text='恢复',
                        function=lambda: self.TableWidget.setMatricxActions(
                            'recover', items=modelItems, recoverModel=self.TableWidget.JudgeCellState(*row_col)
                        ),
                        enable=(
                                self.TableWidget.JudgeCellState(*row_col) == 1 or
                                self.TableWidget.JudgeCellState(*row_col) == 2
                        )
                    ),
                    OptAction().setWidgets(
                        parent=menu,
                        text='(测试)',
                        function=lambda: self.TableWidget.JudgeCellState(0, 0)
                    ),
                ]
            )
        elif len(modelItems) > 1:
            _subMenu1 = OptMenu()
            _subMenu2 = OptMenu()

            menu.setWidgets(
                title="",
                widgets={
                    OptAction().setWidgets(
                        parent=menu,
                        text="导入分析器",
                        icon=QIcon(ImageType.MA_Load),
                        function=lambda: self.TableWidget.setMatricxActions(
                            'load', items=modelItems, ascore=self.DropCoreWidgetAT
                        )
                    ): 1,
                    OptAction().setWidgets(
                        parent=menu,
                        text="复制",
                        icon=QIcon(ImageType.MA_Copy),
                        function=lambda: self.TableWidget.setMatricxActions('copy')
                    ): 1,
                    OptSeparator(): 2,
                    _subMenu1.JustActions(
                        title='功能函数',
                        icon=QIcon(ImageType.MA_Functions),
                        actions=[
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text="求和",
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'a', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='平均值',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'b', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='数量（非空）',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'c', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='乘积',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'd', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='最值',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'e', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='中位数',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'f', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='众数',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'g', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='标准差',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'h', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu1,
                                text='方差',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    'i', self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            )
                        ]  # _subMenu1
                    ): 0,
                    _subMenu2.JustActions(
                        title='矩阵工具',
                        enable=self.TableWidget.JudgeMatrix(modelItems),
                        icon=QIcon(ImageType.MA_Matrix),
                        actions=[
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='行列式值',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    0, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='特征值',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    1, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='秩',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    2, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='奇异判断',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    3, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='迹',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    4, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='对角化',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    5, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='相似化',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    6, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            ),
                            OptAction().setWidgets(
                                parent=_subMenu2,
                                text='矩阵形状',
                                function=lambda: self.TableWidget.setMatricxActions(
                                    7, self.OprBar.FunctionsBar.FunctionsRecordsCombox, modelItems
                                )
                            )
                        ]  # _subMenu2
                    ): 0,
                    OptSeparator(): 2,
                    OptAction().setWidgets(
                        parent=menu,
                        text="合并(慎用)",
                        icon=QIcon(ImageType.MA_Copy),
                        function=lambda: self.TableWidget.setMatricxActions('merge', items=modelItems),
                        enable=self.TableWidget.JudgeMatrix(modelItems)
                    ): 1
                }  # widgets ： {}
            )
        else:
            pass

        showWhere = QPoint(pos.x() + menu.width() // 3, pos.y() + menu.height() // 2)
        menu.exec_(self.TableWidget.mapToGlobal(showWhere))

    # 列菜单栏
    def setHorizontalLabelsMouseMenuActions(self, pos: QPoint):
        # 同单元格选中一样，行标签的选中也分单列和多列模式，下同
        singleHeader: QHeaderView = self.TableWidget.horizontalHeader()
        col: int = singleHeader.logicalIndexAt(pos.x())
        visual_col: int = singleHeader.visualIndex(col)

        selected_ranges: List[QTableWidgetSelectionRange] = self.TableWidget.selectedRanges()

        start_col: int = visual_col
        end_col: int = visual_col
        for selected_range in selected_ranges:
            start_col = selected_range.leftColumn()
            end_col = selected_range.rightColumn()

        if start_col == end_col == visual_col:
            self.TableWidget.selectColumn(visual_col)

        menu = OptMenu(self)

        menu.setWidgets(
            widgets={
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Load),
                    text='导入分析器',
                    function=lambda: self.TableWidget.setHorizonActions(0, ascore=self.DropCoreWidgetAT)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Datasets),
                    text='导出列数据',
                    function=lambda: self.TableWidget.setHorizonActions(
                        1, col_s=visual_col if start_col == end_col else range(start_col, end_col + 1)
                    )
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Datafix),
                    text='数据集修复',
                    function=lambda: self.TableWidget.setHorizonActions(2),
                    enable=(start_col == end_col)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Newcol),
                    text='左侧插入一列',
                    function=lambda: self.TableWidget.setHorizonActions(
                        '3-1', col=visual_col, pos=self.mapToGlobal(pos)
                    ),
                    enable=(start_col == end_col)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Newcol),
                    text='右侧插入一列',
                    function=lambda: self.TableWidget.setHorizonActions(
                        '3-2', col=visual_col, pos=self.mapToGlobal(pos)
                    ),
                    enable=(start_col == end_col)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Delcol),
                    text='删除该列',
                    function=lambda: self.TableWidget.setHorizonActions(4, col=visual_col),
                    enable=(start_col == end_col)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Up),
                    text='升序排列',
                    function=lambda: self.TableWidget.setHorizonActions(5, col=visual_col),
                    enable=(start_col == end_col)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Down),
                    text='降序排列',
                    function=lambda: self.TableWidget.setHorizonActions(6, col=visual_col),
                    enable=(start_col == end_col)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Exchangedata),
                    text='列数据替换',
                    function=lambda: self.TableWidget.setHorizonActions(7, col=visual_col),
                    enable=(start_col == end_col)
                ): 1
            }
        )

        showWhere = QPoint(pos.x() + menu.width() // 3, pos.y() + menu.height() // 2)
        menu.exec_(self.TableWidget.mapToGlobal(showWhere))

        self.TableWidget.clearSelection()

    # 行菜单栏
    def setVerticalLabelsMouseMenuActions(self, pos: QPoint):
        singleHeader: QHeaderView = self.TableWidget.verticalHeader()
        row: int = singleHeader.logicalIndexAt(pos.y())
        visual_row: int = singleHeader.visualIndex(row)

        selected_ranges: List[QTableWidgetSelectionRange] = self.TableWidget.selectedRanges()

        start_row: int = visual_row
        end_row: int = visual_row
        for selected_range in selected_ranges:
            start_row = selected_range.topRow()
            end_row = selected_range.bottomRow()

        if start_row == end_row == visual_row:
            self.TableWidget.selectRow(visual_row)

        menu = OptMenu(self)

        menu.setWidgets(
            widgets={
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Load),
                    text='导入分析器',
                    function=lambda: self.TableWidget.setVerticalActions(0, row=row, ascore=self.DropCoreWidgetAT),
                    enable=(start_row == end_row)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Newrow),
                    text='上面插入一行',
                    function=lambda: self.TableWidget.setVerticalActions(1, row=visual_row),
                    enable=(start_row == end_row)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Newrow),
                    text='下面插入一行',
                    function=lambda: self.TableWidget.setVerticalActions(2, row=visual_row),
                    enable=(start_row == end_row)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Delrow),
                    text='删除该行',
                    function=lambda: self.TableWidget.setVerticalActions(3, row=visual_row),
                    enable=(start_row == end_row)
                ): 1,
                OptAction().setWidgets(
                    parent=menu,
                    icon=QIcon(ImageType.MA_Datasets),
                    text='导出行数据',
                    function=lambda: self.TableWidget.setVerticalActions(
                        4, row_s=visual_row if start_row == end_row else range(start_row, end_row + 1)
                    )
                ): 1
            }
        )

        showWhere = QPoint(pos.x() + menu.width() // 3 - 20, pos.y() + menu.height() // 2 + 20)
        menu.exec_(self.TableWidget.mapToGlobal(showWhere))
        self.TableWidget.clearSelection()

    def setSliderToCells(self) -> None:
        WhenSetSliderToCells(self)

    def setAdjustAlignment(self, align=Qt.AlignCenter) -> None:
        WhenSetAdjustAlignment(self, align)

    def setAdjustFont(self, family_or_size: str = 'f') -> None:
        WhenSetAdjustFont(self, family_or_size)

    def setItemsByFileLoader(self) -> None:
        WhenSetItemsByFileLoader(self)

    def setSaveModel(self, justSave: bool = True) -> None:
        WhenSetSaveModel(self, justSave)

    def setCurrentCellByJump(self) -> None:
        WhenSetCurrentCellByJump(self)

    def setMatchCellsBackgroundColor(self) -> None:
        WhenSetMatchCellsBackgroundColor(self)

    def setMatchCellsShown(self) -> None:
        WhenSetMatchCellsShown(self)

    def setMatchCellsRecover(self) -> None:
        WhenSetMatchCellsRecover(self)

    def setFormatMenu(self) -> None:
        WhenSetFormatMenu(self)

    # 信号量同步机制——核心功能之一
    # 当TableWidget.HeaderChangedSignal.emit()信号就会调用
    # 目前会导致信号触发的函数有
    """
    1.导入
    2.删除列
    3.新加列
    4.列替换
    """

    def setHeaderChangedSignalCore(self):
        print("信号接收一次!")
        headers: list = self.TableWidget.HeaderLabels
        # @作用一，同步跳转栏内容
        self.OprBar.FunctionsBar.SearchCellEdit.renewModel(headers)

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        icon=QIcon(ImageType.APP_LOGO),
        display_name='QExcel'
    )
    ui = ExcelKernel()
    ui.setWidgets()
    ui.setMinimumSize(QSize(1200, 800))
    ui.show()
    app.exec()
