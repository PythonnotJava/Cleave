from typing import Iterable, Dict
import pyqtgraph
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import numpy as np

pyqtgraph.setConfigOption('background', QColor(240, 240, 240))
pyqtgraph.setConfigOption('foreground', QColor('darkblue'))

class PyQtGraphLinePlot(pyqtgraph.PlotWidget):
    def addPlot(self,
                X : Iterable,
                Y : Iterable,
                pen : str | QColor = 'r',
                name='LinePlot'
                ):
        # 设置图例
        plot = self.plot(X, Y, pen=pen)
        legend : pyqtgraph.LegendItem = self.addLegend()
        legend.addItem(plot, name)
        return self

    def setLabels(self, labels_aligns : Dict[str, Qt.Alignment]):
        for key, value in iter(labels_aligns):
            if value == Qt.AlignBottom:
                self.setLabel('bottom', key)
            elif value == Qt.AlignLeft:
                self.setLabel('left', key)
            elif value == Qt.AlignRight:
                self.setLabel('right', key)
            elif value == Qt.AlignTop:
                self.setLabel('top', key)
            else:
                pass
        return self

if __name__ == '__main__':
    app = QApplication([])
    mainw = QMainWindow()
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    y2 = np.arccos(x)
    widget = PyQtGraphLinePlot()
    widget.addPlot(x, y, name='sin', pen='b').addPlot(x, y2, name='arccos')
    mainw.setCentralWidget(widget)
    mainw.show()
    app.exec()


__all__ = ['PyQtGraphLinePlot']