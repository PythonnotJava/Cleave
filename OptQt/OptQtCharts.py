from typing import *
from PyQt5.QtChart import *
from OptQt.OptimizeQt import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtChart import *
from PyQt5.QtCore import Qt

from Sources import *


# QChart相当于是展示所有控件的画布
# QChartView相当于是拖住画布的画板
class OptQChartView(QChartView, AbstractWidget):
    def setWidgets(self,
                   chart: Optional[Union[QChart]] = None,
                   hints: Optional[Union[QPainter.RenderHints, QPainter.RenderHint]] = None,
                   **kwargs):
        self.baseCfg(**kwargs)
        if chart is not None: self.setChart(chart)
        if hints is not None: self.setRenderHints(hints)
        return self

    def addSeries(self, series : list[QAbstractSeries]):
        if self.chart() is not None:
            for _series in series:
                self.chart().addSeries(_series)

class OptChartFigure(QChart):
    def setWidgets(self,
                   title: Optional[str] = None,
                   axes_aligns: Dict[QAbstractAxis, Qt.Alignment] = None,
                   createDefaultAxes: bool = False,
                   series: Optional[list[QAbstractSeries]] = None,
                   animationOptions: Optional[Union[QChart.AnimationOption, QChart.AnimationOptions]] = None,
                   theme: Optional[QChart.ChartTheme] = None
                   ):
        if createDefaultAxes: self.createDefaultAxes()
        if theme is not None: self.setTheme(theme)
        if title is not None: self.setTitle(title)
        if animationOptions is not None: self.setAnimationOptions(animationOptions)
        if axes_aligns is not None:
            for key in axes_aligns:
                self.addAxis(key, axes_aligns[key])
        if series is not None:
            for ser in series:
                self.addSeries(ser)
        return self
    @overload
    def addSeries(self, series : QAbstractSeries): ...
    @overload
    def addSeries(self, series : list[QAbstractSeries]): ...
    def addSeries(self, series: list[QAbstractSeries] | QAbstractSeries):
        if isinstance(series, list):
            for se in series: super().addSeries(se)
        else: super().addSeries(series)

# 抽象轴基类
# 抽象轴基类
class AbstractAxis(QAbstractAxis):
    def setWidgets(self,
                   titleText: Optional[str] = None,
                   titleFont: Optional[QFont] = None,
                   labelsAngle: Optional[int] = None,
                   labelsVisible: bool = True,
                   labelsColor: Qt.GlobalColor | QColor = QColor('black'),
                   labelFont: Optional[QFont] = None,
                   lineVisible: bool = True,
                   editable: bool = False,
                   ranges: Union[tuple, list] = None
                   ):
        if titleText is not None: self.setTitleText(titleText)
        if titleFont is not None: self.setTitleFont(titleFont)
        if labelsAngle is not None: self.setLabelsAngle(labelsAngle)
        if labelFont is not None: self.setLabelsFont(labelFont)
        if ranges is not None: self.setRange(ranges)
        self.setLabelsVisible(labelsVisible)
        self.setLineVisible(lineVisible)
        self.setLabelsColor(labelsColor)
        self.setLabelsEditable(editable)
        return self


# 柱坐标轴
class BarAxis(QBarCategoryAxis, AbstractAxis):
    def setSelf(self,
                labels: list[str] | None = None,
                minValue : Optional[str] = None,
                maxValue : Optional[str] = None
                ):
        self.setCategories(labels)
        if minValue is not None: self.setMin(minValue)
        if maxValue is not None: self.setMax(maxValue)
        return self

# 数轴
class ValueAxis(QValueAxis, AbstractAxis):
    def setSelf(self,
                tickType: Optional[QValueAxis.TickType] = None,
                labelFormat: Optional[str] = None,
                tickCount: Optional[int] = None,
                minValue: Optional[float] = None,
                maxValue: Optional[float] = None
                ):
        if minValue is not None: self.setMin(minValue)
        if maxValue is not None: self.setMax(maxValue)
        if labelFormat is not None: self.setLabelFormat(labelFormat)
        if tickCount is not None: self.setTickCount(tickCount)
        if tickType is not None: self.setTickType(tickType)
        return self

# 柱状图的柱子
class Bar(QBarSet):
    def setSelf(self,
                values: list[float],
                label: Optional[str] = None,
                labelColor: Qt.GlobalColor | QColor = QColor('tan'),
                labelFont: Optional[QFont] = None,
                color: Qt.GlobalColor | QColor | None = QColor('yellow'),
                borderColor: Qt.GlobalColor | QColor = QColor('pink')
                ):
        self.append(values)
        self.setLabelColor(labelColor)
        if label is not None: self.setLabel(label)
        if labelFont is not None: self.setLabelFont(labelFont)
        if color is not None: self.setColor(color)
        if borderColor is not None: self.setBorderColor(borderColor)
        return self

# 图的种类
class AbstractSeries(QAbstractSeries):
    def setWidgets(self,
                   attachAxis: list[QAbstractAxis] | QAbstractAxis = None,
                   useOpenGL: bool = False,
                   legend: Optional[str] = None,
                   visible : bool = True
                   ):
        self.setUseOpenGL(useOpenGL)
        self.setVisible(visible)
        if legend is not None: self.setName(legend)
        if attachAxis is not None:
            if isinstance(attachAxis, list):
                for _axis in attachAxis: self.attachAxis(_axis)
            else: self.attachAxis(attachAxis)

        return self

# 柱状图
class BarSeries(QBarSeries, QAbstractBarSeries, AbstractSeries):
    def setSelf(self,
                bar: QBarSet,
                barWidth: Optional[float] = None,
                labelsVisible: bool = True,
                labelsAngle: Optional[int] = None,
                labelsPrecision: Optional[int] = None,
                labelsPosition: Optional[QAbstractBarSeries.LabelsPosition] = None,
                labelsFormat: Optional[str] = None
                ):
        self.setLabelsVisible(labelsVisible)
        self.append(bar)
        if barWidth is not None: self.setBarWidth(barWidth)
        if labelsPosition is not None: self.setLabelsPosition(labelsPosition)
        if labelsAngle is not None: self.setLabelsAngle(labelsAngle)
        if labelsFormat is not None: self.setLabelsFormat(labelsFormat)
        if labelsPrecision is not None: self.setLabelsPrecision(labelsPrecision)
        return self


# 二维点图，散点图、折线图都继承于此
class XYSeries(QXYSeries, AbstractSeries):
    def extend(self, coordinates: list[Union[tuple, list]]) -> None:
        for coordinate in coordinates: self.append(*coordinate)

    def setXYSelf(self,
                  points: list[QPoint] | list[QPointF] | QPoint | QPointF = None,
                  coordinates : list[Union[tuple, list]] = None,
                  penWidth: float = 5.0,
                  pointLabelsColor: QColor | Qt.GlobalColor = QColor('black'),
                  pointLabelsFont: Optional[QFont] = None,
                  pointLabelsVisible: bool = False,
                  pointLabelsFormat: Optional[str] = None,
                  pointLabelsClipping: bool = True,
                  pointsVisible: bool = True,
                  color: Qt.GlobalColor | QColor = QColor('skyblue')
                  ):
        self.setPointLabelsClipping(pointLabelsClipping)
        self.setPointLabelsVisible(pointLabelsVisible)
        self.setPointsVisible(pointsVisible)
        self.setPointLabelsColor(pointLabelsColor)
        self.setColor(color)
        if points is not None: self.append(points)
        if coordinates is not None: self.extend(coordinates)
        if pointLabelsFont is not None: self.setPointLabelsFont(pointLabelsFont)
        if pointLabelsFormat is not None: self.setPointLabelsFormat(pointLabelsFormat)

        pen = self.pen()
        pen.setWidthF(penWidth)
        self.setPen(pen)
        return self

# 散点图
class ScaSeries(QScatterSeries, XYSeries):
    def setSelf(self,
                markerSize: Optional[float] = None,
                markerShape: Optional[QScatterSeries.MarkerShape] = None,
                borderColor: Qt.GlobalColor | QColor = QColor('darkblue')
                ) -> 'ScaSeries':
        self.setBorderColor(borderColor)
        if markerShape is not None: self.setMarkerShape(markerShape)
        if markerSize is not None: self.setMarkerSize(markerSize)
        return self

# 线图
class LineSeries:
    class Curveline(QSplineSeries, XYSeries): ...
    class Polyline(QLineSeries, XYSeries): ...

    @classmethod
    def setSelf(cls, curve : bool = True) -> Union[Curveline, Polyline]:
        # curve为True是曲线，反之折线
        return cls.Curveline() if curve else cls.Polyline()

if __name__ == '__main__':
    app = OptAppication([])
    ui = QMainWindow()
    ui.setMinimumSize(1200, 800)

    import numpy

    points11 = numpy.random.normal(0, 1, 100)
    points12 = numpy.random.normal(0, 1, 100)
    points13 = numpy.random.normal(0, 1, 100)
    points14 = numpy.random.normal(0, 1, 100)

    line1points = [(index, x) for index, x in enumerate(points11)]
    line2points = [(index, x) for index, x in enumerate(points12)]
    line3points = [(index, x) for index, x in enumerate(points13)]
    line4points = [(index, x) for index, x in enumerate(points14)]

    axisx = ValueAxis().setSelf(minValue=0, maxValue=110)
    axisy = ValueAxis().setSelf(minValue=-10, maxValue=100)

    barAxisx = BarAxis().setSelf(labels=['Python', 'Dart', 'Java'])

    ui.setCentralWidget(
        OptQChartView().setWidgets(
            hints=QPainter.RenderHint.Antialiasing,
            chart=OptChartFigure().setWidgets(
                theme=QChart.ChartThemeBlueIcy,
                animationOptions=QChart.AnimationOption.AllAnimations,
                createDefaultAxes=True,
                title='不同数据的汇总',
                axes_aligns={
                    axisx : Qt.AlignBottom,
                    axisy : Qt.AlignLeft,
                    barAxisx : Qt.AlignBottom
                },
                series=[
                    BarSeries().setWidgets(
                        legend='字符串统计',
                        attachAxis=barAxisx
                    ).setSelf(
                        bar=Bar('名字').setSelf(
                            color=Qt.cyan,
                            values=[65, 59, 23]
                        )
                    ),
                    LineSeries.setSelf().setXYSelf(
                        coordinates=line1points, color=Qt.darkBlue, penWidth=3, pointLabelsVisible=False
                    ).setWidgets(legend='数据11', attachAxis=[axisx, axisy]),
                    LineSeries.setSelf().setXYSelf(
                        coordinates=line2points, color=Qt.yellow, penWidth=1, pointLabelsVisible=False
                    ).setWidgets(legend='数据12', attachAxis=[axisx, axisy]),
                    LineSeries.setSelf().setXYSelf(
                        coordinates=line3points, color=Qt.red, penWidth=1, pointLabelsVisible=False
                    ).setWidgets(legend='数据13', attachAxis=[axisx, axisy]),
                    LineSeries.setSelf().setXYSelf(
                        coordinates=line4points, color=Qt.cyan, penWidth=1, pointLabelsVisible=False
                    ).setWidgets(legend='数据14', attachAxis=[axisx, axisy])
                ],
            )
        )
    )
    ui.show()
    app.exec()
