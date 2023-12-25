import random
from typing import Callable
import asyncio
from qtawesome import icon as qticon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout

from OptQt.OptComponent import ReWriteInputDialog
from OptQt.OptimizeQt import *
from Sources import ImageType, CursorType

from OptQt.OptQtCharts import *

class _TreeWidget(QTreeWidget, AbstractWidget):
    def __init__(self):
        super().__init__()

        self.setUI()

    def setUI(self):
        self.setHeaderLabels(['值', '坐标'])
        header: QHeaderView = self.header()
        header.setSectionResizeMode(QHeaderView.Stretch)

    def addItem(self, coordinate: str, value: str, flags: Optional[Union[Qt.ItemFlags, Qt.ItemFlag]] = None
                ) -> QTreeWidgetItem:
        item = QTreeWidgetItem(self, [value, coordinate])
        if flags is not None:
            item.setFlags(flags)
        return item

    def addItems(self, coordinates: list[str], values: list[str],
                 flags: Optional[Union[Qt.ItemFlags, Qt.ItemFlag]] = None) -> List[QTreeWidgetItem]:
        lis = []
        if flags is not None:
            for index, coordinate in enumerate(coordinates):
                item = QTreeWidgetItem(self, [values[index], coordinate])
                item.setFlags(flags)
                lis.append(item)
        else:
            for index, coordinate in enumerate(coordinates):
                item = QTreeWidgetItem(self, [values[index], coordinate])
                lis.append(item)
        return lis

    def setWidgets(self,
                   **kwargs
                   ) -> "_TreeWidget":
        self.baseCfg(**kwargs)
        return self

# Excel数据分析的分析过程，会对数据进行筛选提示，
# 从而在绘图之前知道哪些工作未完善以及哪些使用工具更适合
class ASCore(QScrollArea):
    """
    ASCore在接受新的数据时，会更新以下的数据结构\n
    - RegisterHistogramDatas：用于寄存当前新导入由getOrganizeClassify解析的数据，并作简单的分析展示在ASCore控件上，
    之后，你可以根据这些极其有用的简单分析作出进一步可视化选择
    - RegisterSignal：是用于RegisterHistogramDatas传收并做出功能更新的信号量
    """
    RegisterHistogramDatas: Dict[str, Any] = None
    RegisterSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.MainWidget = AbstractWidget()
        self.Vbox = OptVBox()

        # 记录非数字类型
        self.StringDatasLabel = OptLabel()
        self.StringDatasList = _TreeWidget()


        # 记录被选中标签并提供操作
        self.SelectLabels = OptLabel()
        self.SelectLabelsList = OptListWidget()


        # 呈现数据占比
        self.ChartView = OptQChartView()
        self.__ChartViewChart = OptChartFigure()
        # 呈现数字型数据趋势
        self.NumberTraces = OptQChartView()
        self.__NumberTracesChart = OptChartFigure()

        # 更新TreeWidget
        self.__Worker1 = None
        # 更新ListWidget
        self.__Worker2 = None
        # 更新图表
        # self.__Worker3 = None
        # self.__Worker4 = None

        self.setUI()

    def setUI(self):
        self.setWidgetResizable(True)
        self.setWidget(self.MainWidget)
        self.MainWidget.setLayout(self.Vbox)
        self.horizontalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.verticalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.SelectLabelsList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.SelectLabelsList.horizontalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.SelectLabelsList.verticalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.SelectLabelsList.customContextMenuRequested.connect(self.selectLabelsMenu)
        self.StringDatasList.horizontalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.StringDatasList.verticalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
        self.RegisterSignal.connect(self.acceptDataSets)

    @pyqtSlot()
    def __refreshStringDatasList(self, dataSets : Dict):
        self.StringDatasList.clear()
        for _key in dataSets['StringDataPosition']:
            coordinates: list[list] = self.RegisterHistogramDatas['StringDataPosition'][_key]
            for coordinate in coordinates:
                self.StringDatasList.addItem(str(coordinate), _key)

    @pyqtSlot()
    def __refreshCommonListItems(self, dataSets : Dict) -> None:
        self.SelectLabelsList.clear()
        for name in dataSets['Datas'].keys():
            self.SelectLabelsList.addItem(
                OptListWidgetItem().setWidgets(
                    text=name,
                    checkState=Qt.CheckState.Checked,
                    flags=Qt.ItemIsEnabled | Qt.ItemIsUserCheckable
                )
            )

    def __refreshHistChart(self, dataSets : Dict) -> None:
        self.__ChartViewChart.removeAllSeries()
        self.__ChartViewChart.removeAxis(self.__ChartViewChart.axisX())
        _axisx = BarAxis().setWidgets(editable=True).setSelf(
            ['数据总数(100%)', f'数字类数据{(dataSets['NumberCounts'] * 100 / dataSets['DataCounts']):.2f}%',
             f'字符型数据{(dataSets['StringDataCounts'] * 100 / dataSets['DataCounts']):.2f}%',
             f'空数据{(dataSets['NullDataCounts'] * 100 / dataSets['DataCounts']):.2f}%'],
        )
        self.__ChartViewChart.addSeries(
            BarSeries().setWidgets(attachAxis=[_axisx]).setSelf(
                bar=Bar('数据量').setSelf(
                    values=[dataSets['DataCounts'], dataSets['NumberCounts'],
                            dataSets['StringDataCounts'], dataSets['NullDataCounts']],
                    labelColor=QColor('black'),
                    color=QColor('skyblue')
                ),
            )
        )
        self.__ChartViewChart.addAxis(_axisx, Qt.AlignBottom)

    def __refreshLineChart(self, dataSets : Dict) -> None:
        self.__NumberTracesChart.removeAllSeries()
        label_name: str
        lineSeries = []
        for label_name in dataSets['Datas']:
            # 只统计数字型数据
            if not label_name.endswith('_string'):
                print("label_name", label_name)
                lineSeries.append(
                    LineSeries.setSelf(True).setXYSelf(
                        points=[QPointF(k, v) for k, v in enumerate(dataSets['Datas'][label_name])],
                        penWidth=1.5, color=random.choice(RandomColorLists)
                    ).setWidgets(legend=label_name)
                )
        self.__NumberTracesChart.addSeries(lineSeries)

    def acceptDataSets(self, dataSets: Dict[str, Any]) -> None:
        self.RegisterHistogramDatas = dataSets

        self.__Worker1 = OptThread(lambda : self.__refreshStringDatasList(dataSets))
        self.__Worker2 = OptThread(lambda: self.__refreshCommonListItems(dataSets))
        self.__refreshLineChart(dataSets)
        self.__refreshHistChart(dataSets)
        # self.__Worker3 = OptThread(lambda: self.__refreshHistChart(dataSets))
        # self.__Worker4 = OptThread(lambda: self.__refreshLineChart(dataSets))

        # 连接信号和槽
        self.__Worker1.finished.connect(self.__Worker1.quit)
        self.__Worker2.finished.connect(self.__Worker2.quit)
        # self.__Worker3.finished.connect(self.__Worker3.quit)
        # self.__Worker4.finished.connect(self.__Worker4.quit)

        # 启动线程
        self.__Worker1.start()
        self.__Worker2.start()
        # self.__Worker3.start()
        # self.__Worker4.start()

        # 等待所有线程完成
        self.__Worker1.wait()
        self.__Worker2.wait()
        # self.__Worker3.wait()
        # self.__Worker4.wait()

    def setWidgets(self,
                   **kwargs) -> 'ASCore':
        self.MainWidget.baseCfg(**kwargs)

        self.Vbox.addLayout(
            OptHBox().setWidgets(
                widgets=[
                    OptPushButton().setWidgets(
                        icon=ImageType.MA_Tips,
                        function=lambda: ...,
                        tips='提示',
                        maxh=50,
                        maxw=50,
                        icon_fixed=True,
                        cursor=CursorType.Link,
                        qss='''
                        QPushButton{ border-radius : 25px; }
                        QPushButton:hover { background-color : silver; }
                        QPushButton:pressed{ background-color : purple;padding : 10px;}
                        '''
                    )
                ]
            ).setCommonAlign(Qt.AlignRight)
        )

        self.Vbox.setWidgets(
            widgets=[
                self.StringDatasLabel.setWidgets(
                    text='字符类数据',
                    maxh=50,
                    objectName='StringDatasLabel'
                ),
                self.StringDatasList.setWidgets(
                    minw=250,
                    maxh=400,
                    objectName='StringDatasList'
                ),
                self.SelectLabels.setWidgets(
                    text='选中标签',
                    maxh=50,
                    objectName='SelectLabels'
                ),
                self.SelectLabelsList.setWidgets(
                    align=Qt.AlignLeft,
                    minw=250,
                    maxh=400,
                ),
                self.ChartView.setWidgets(
                    self.__ChartViewChart.setWidgets(
                        title="数据量以及占比",
                        animationOptions=OptChartFigure.GridAxisAnimations,
                        theme=OptChartFigure.ChartThemeBlueIcy
                    ),
                    minh=400,
                    minw=250
                ),
                self.NumberTraces.setWidgets(
                    self.__NumberTracesChart.setWidgets(
                        title='数据趋势',
                        createDefaultAxes=True,
                        animationOptions=OptChartFigure.AnimationOption.SeriesAnimations,
                        theme=OptChartFigure.ChartThemeBlueIcy
                    ),
                    minh=400,
                    minw=250
                ),
                AbstractWidget().factoryConstructor(minh=400)
            ]
        ).setCommonAlign(Qt.AlignTop)
        return self

    # 标签右键菜单栏
    def selectLabelsMenu(self, pos: QPoint) -> None:
        item: Optional[QListWidgetItem] = self.SelectLabelsList.itemAt(pos)
        if item is not None:
            menu = OptMenu(self)
            menu.setWidgets(
                widgets={
                    OptAction().setWidgets(
                        parent=menu,
                        text='临时重命名',
                        function=lambda: self.setTempRename(item),
                        icon=ImageType.MA_Rename
                    ): 1,
                    OptAction().setWidgets(
                        parent=menu,
                        text='向上下移',
                        function=lambda: self.setItemMoved(item),
                        icon=ImageType.MA_Up
                    ): 1,
                    OptAction().setWidgets(
                        parent=menu,
                        text='向下下移',
                        function=lambda: self.setItemMoved(item, False),
                        icon=ImageType.MA_Down
                    ): 1
                }
            )
            menu.exec_(self.SelectLabelsList.mapToGlobal(pos))

    # 标签下移、上移
    def setItemMoved(self, item: QListWidgetItem, Up: bool = True) -> None:
        row = self.SelectLabelsList.row(item)
        if Up:
            if row > 0:
                self.SelectLabelsList.takeItem(row)
                self.SelectLabelsList.insertItem(row - 1, item)
        else:
            if row < self.SelectLabelsList.count() - 1:
                self.SelectLabelsList.takeItem(row)
                self.SelectLabelsList.insertItem(row + 1, item)

    # 重命名
    @staticmethod
    def setTempRename(item: QListWidgetItem) -> None:
        dialog = ReWriteInputDialog()

        def __func(_text):
            item.setText(_text) if _text is not None and not _text.isspace() and _text != '' \
                else item.setText(item.text())
            dialog.close()

        dialog.setWidgets(
            labelText='名称',
            modal=True,
            title='临时重命名',
            icon=ImageType.APP_LOGO,
            okBtn_function=lambda: __func(dialog.text()),
            placeholderText=item.text(),
            fixSize=(280, 100)
        )
        dialog.exec_()


if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='ASCore',
        icon=QIcon(ImageType.APP_LOGO)
    )
    ui = ASCore()
    ui.StringDatasList.addItems(
        ["[A, 6]", "[B, 4]", "[B, 14]", "[E, 4]"], ["0.0.0", "A", "QQ", "M", "Y"]
    )
    ui.setWidgets()
    ui.show()
    app.exec()
