from typing import overload, Optional, Iterable
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon, QCursor, QPixmap
from OptQt import ExcelKernel, OptAppication
from Sources import ImageType

class AnalysisCore(ExcelKernel):

    __slots__ = 'Vbox'

    def __init__(self):
        super().__init__()

        self.Vbox = QVBoxLayout()

    def setWidgets(self, familys: Iterable = ('微软雅黑',), sizes: Iterable = (12,), **kwargs):
        return super().setWidgets(
            familys=familys,
            sizes=sizes,
            **kwargs
        )

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        icon=QIcon(ImageType.APP_LOGO),
        display_name='AnalysisCore'
    )
    ui = AnalysisCore()
    ui.setWidgets()
    ui.show()
    app.exec()