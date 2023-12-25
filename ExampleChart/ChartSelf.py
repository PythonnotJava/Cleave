from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QBarSet, \
    QPercentBarSeries, QBarCategoryAxis
import sys
from PyQt5.QtGui import QIcon


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # window requirements
        self.setGeometry(200, 200, 600, 400)
        self.setWindowTitle("Creating Barchart")
        self.setWindowIcon(QIcon("python.png"))

        # change the color of the window
        self.setStyleSheet('background-color: rgb(240, 240, 240)')

        # create barseries
        set0 = QBarSet("Parwiz")
        set1 = QBarSet("Karim")
        set2 = QBarSet("Tom")
        set3 = QBarSet("Logan")
        set4 = QBarSet("Bob")

        # insert data to the barseries
        set0 << 1 << 2 << 3 << 4 << 5 << 6
        set1 << 5 << 0 << 0 << 4 << 0 << 7
        set2 << 3 << 5 << 8 << 13 << 8 << 5
        set3 << 5 << 6 << 7 << 3 << 4 << 5
        set4 << 9 << 7 << 5 << 3 << 1 << 2

        # we want to create percent bar series
        series = QPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        # create chart and add the series in the chart
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Barchart Percent Example")
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartTheme.ChartThemeLight)

        # create axis for the chart
        categories = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]

        axis = QBarCategoryAxis()
        axis.append(categories)
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)

        # create chartview and add the chart in the chartview
        chartview = QChartView(chart)

        vbox = QVBoxLayout()
        vbox.addWidget(chartview)

        self.setLayout(vbox)


if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())
