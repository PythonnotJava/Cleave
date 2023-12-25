from typing import Callable

from qtawesome import icon as qticon
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout

from OptQt.OptComponent import ReWriteInputDialog
from OptQt.OptimizeQt import *
from Sources import ImageType, CursorType

# Excel数据分析栏的核心绘图控件
# 通过选定数据分析可视化，但是可视化是独立的
class ASChartBox(AbstractWidget):
    __slots__ = ('Vbox', 'ApiToolBox', 'QtChartBox', 'QtChartBox', 'MatChartBox', 'Qt3dChartBox', 'grid_qtchart',
                 'grid_matplotlib', 'grid_qt3d')

    def __init__(self):
        super().__init__()

        # QtChart-api
        # self.QtLine = OptPushButton()
        # self.QtPolar = OptPushButton()
        # self.QtPie = OptPushButton()
        # self.QtHorizontalBar = OptPushButton()
        # self.QtVerticalBar = OptPushButton()
        # self.QtComplexHorizontalBars = OptPushButton()
        # self.QtComplexVerticalBars = OptPushButton()
        # self.QtScatter = OptPushButton()
        # self.QtBoxPlot = OptPushButton()
        # self.QtMinxin = OptPushButton()

        # matplotlib-api
        # self.MatLine = OptPushButton()
        # self.MatPolar = OptPushButton()
        # self.MatPie = OptPushButton()
        # self.MatHorizontalBar = OptPushButton()
        # self.MatVerticalBar = OptPushButton()
        # self.MatComplexHorizontalBars = OptPushButton()
        # self.MatComplexVerticalBars = OptPushButton()
        # self.MatScatter = OptPushButton()
        # self.MatStem = OptPushButton()
        # self.MatBoxPlot = OptPushButton()
        # self.MatErrorPlot = OptPushButton()
        # self.MatMinxin = OptPushButton()

        # Qt3d-DataVisualization-api
        # self.Qt3dSurface = OptPushButton()
        # self.Qt3dBars = OptPushButton()
        # self.Qt3dScatter = OptPushButton()

        # pyqtgraph
        ...

        self.Vbox = OptVBox()
        self.ApiToolBox = OptToolBox()
        self.QtChartBox = AbstractWidget()
        self.MatChartBox = AbstractWidget()
        self.Qt3dChartBox = AbstractWidget()

        self.grid_qtchart = QGridLayout()
        self.grid_matplotlib = QGridLayout()
        self.grid_qt3d = QGridLayout()

        self.setUI()

    def setUI(self):
        self.setLayout(self.Vbox)
        self.Vbox.addWidget(self.ApiToolBox, Qt.AlignCenter)

    def setWidgets(self,
                   qtcharts_functions : list[Callable] | None = None,
                   matplots_functions : list[Callable] | None = None,
                   qt3dplots_functions : list[Callable] | None = None,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        qtcharts = [
            '线型图', '极线图', '饼状图', '水平柱状图', '垂直柱状图',
            '复合水平柱状图', '复合垂直柱状图', '散点图', '箱型图', '混合模式'
        ]  # len == 10
        qtcharts_icons = [
            ImageType.Line, ImageType.Polar, ImageType.Pie, ImageType.Bar, ImageType.Bar,
            ImageType.Bar, ImageType.Bar, ImageType.Scatter, ImageType.Box, ImageType.Mixin
        ]

        matplots = [
            '线型图', '极线图', '饼状图', '水平柱状图', '垂直柱状图',
            '复合水平柱状图', '复合垂直柱状图', '散点图', '棉棒图', '箱型图',
            '误差图', '混合模式'
        ]  # len == 12
        matplots_icons = [
            ImageType.Line, ImageType.Polar, ImageType.Pie, ImageType.Bar, ImageType.Bar,
            ImageType.Bar, ImageType.Bar, ImageType.Scatter, ImageType.Cotton, ImageType.Box,
            ImageType.Cotton, ImageType.Mixin
        ]

        qt3dplots = [
            '曲面图', '三维柱状图', '三维散点图'
        ]  # len == 3
        qt3dplots_icons = [
            ImageType.Surface3d, ImageType.Bar3d, ImageType.Scatter3d
        ]

        for i, name in enumerate(qtcharts):
            row = i // 4
            col = i % 4
            button = OptToolButton().setWidgets(
                function=qt3dplots_functions[i] if qtcharts_functions is not None else lambda: ...,
                icon=qtcharts_icons[i],
                tips=qtcharts[i],
                icon_fixed=True,
                maxh=100,
                maxw=100,
                cursor=CursorType.Link
            )
            self.grid_qtchart.addWidget(button, row, col)

        for i, name in enumerate(matplots):
            row = i // 4
            col = i % 4
            button = OptToolButton().setWidgets(
                function=matplots_functions[i] if matplots_functions is not None else lambda: ...,
                icon=matplots_icons[i],
                tips=matplots[i],
                icon_fixed=True,
                maxh=100,
                maxw=100,
                cursor=CursorType.Link
            )
            self.grid_matplotlib.addWidget(button, row, col)

        for i, name in enumerate(qt3dplots):
            row = i // 2
            col = i % 2
            button = OptToolButton().setWidgets(
                function=qt3dplots_functions[i] if qt3dplots_functions is not None else lambda: ...,
                tips=qt3dplots[i],
                icon=qt3dplots_icons[i],
                icon_fixed=True,
                maxh=100,
                maxw=100,
                cursor=CursorType.Link
            )
            self.grid_qt3d.addWidget(button, row, col)

        self.ApiToolBox.setWidgets(
            items={
                self.QtChartBox.factoryConstructor(
                    objectName='QtChartBox',
                    mainlay=self.grid_qtchart
                ): 'QtChart',
                self.MatChartBox.factoryConstructor(
                    objectName='MatChartBox',
                    mainlay=self.grid_matplotlib
                ): 'Matplotlib',
                self.Qt3dChartBox.factoryConstructor(
                    objectName='Qt3dChartBox',
                    mainlay=self.grid_qt3d
                ): 'Qt3d'
            },
            icons=[qticon('fa.area-chart'), qticon('ei.graph'), qticon('mdi.graph')],
            currentIndex=0,
            objectName='ApiToolBox'
        )

        scs: list[QScrollArea] = self.ApiToolBox.findChildren(QScrollArea)
        for sc in scs:
            sc.verticalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))
            sc.horizontalScrollBar().setCursor(QCursor(QPixmap(CursorType.Move)))

        return self
if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='ASChartBox',
        icon=ImageType.APP_LOGO
    )
    ui = ASChartBox()
    ui.setWidgets()
    ui.show()
    app.exec()