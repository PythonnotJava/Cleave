from os import PathLike
from typing import overload

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWebEngineWidgets import QWebEngineSettings

from OptQt import *
from Sources import *

class HomePageView(OptWebView):

    __slots__ = 'defaultHtml'

    def __init__(self, defaultHtml: int = 0):
        super().__init__()

        self.defaultHtml = defaultHtml
        self.setUI()

    def setUI(self):
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent, *args):
        if e.mimeData() is not None and e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent, *args):
        if e.mimeData().hasUrls():
            url = e.mimeData().urls()[0]
            filePath = url.toLocalFile()
            if filePath.endswith('.html'):
                self.RefreshHtml(filePath)
            else:
                print("Unsupport FileType!")

    @overload
    def setWidgets(self, htmlFile: PathLike | str = None, **kwargs): ...

    @overload
    def setWidgets(self, htmlFile: PathLike | str = None, defaultSets : bool = True, **kwargs): ...

    def setWidgets(self, htmlFile: PathLike | str = None, defaultSets: bool = True, **kwargs):
        if defaultSets:
            if self.defaultHtml == 0:
                return super().setWidgets(
                    htmlFile=PageType.Dracula,
                    **kwargs
                )
            elif self.defaultHtml == 1:
                return super().setWidgets(
                    htmlFile=PageType.Skyblue,
                    **kwargs
                )
            elif self.defaultHtml == 2:
                return super().setWidgets(
                    htmlFile=PageType.Cyan,
                    **kwargs
                )
            else : pass
        else:
            return super().setWidgets(
                htmlFile=htmlFile,
                **kwargs
            )
    def RefreshHtml(self, htmlFile=PageType.Dracula):
        self.defaultHtml = htmlFile
        self.setHtml(open(htmlFile, 'r', encoding='u8').read())
        return self

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='HomePageView',
        icon=ImageType.APP_LOGO
    )
    ui = HomePageView()
    ui.setWidgets()
    ui.show()
    app.exec()
