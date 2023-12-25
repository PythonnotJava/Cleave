
from typing import *
from PyQt5.Qsci import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from OptQt.OptimizeQt import *
from EditorCore.FirstPage import FirstPage
from Sources import *

class EditorSelf(QMainWindow):
    def __init__(self):
        super().__init__()

        self.TabsOperator = OptTabWidget()
        self.MenuBar = OptMenuBar()
        self.FileDirDock = OptDock()
        self.TerminalDock = OptDock()
        self.StatusBar = OptStatusBar()
        self.DefaultTab = FirstPage()

        self.setUI()
    def setUI(self):
        self.setCentralWidget(self.TabsOperator)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.FileDirDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.TerminalDock)
        self.setStatusBar(self.StatusBar)
        self.setMenuBar(self.MenuBar)

    def setWidgets(self,
                   ) -> 'EditorSelf':
        self.TabsOperator.setWidgets(
            enClosed=True,
            qss='background : tan',
            tabSets=[
                TabWidgetDict(
                    text='Home',
                    tips='主界面',
                    icon=ImageType.APP_LOGO,
                    enabled=True,
                    widget=self.DefaultTab
                )
            ],
        )
        self.MenuBar.setWidgets(
            qss='background : red',
            widgets={
                OptMenu().setWidgets(
                    parent=self.MenuBar,
                    title='打开'
                ) : 0,
                OptAction().setWidgets(
                    parent=self.MenuBar,
                    text='事件'
                ) : 1
            }
        )
        self.FileDirDock.setWidgets(
            resize=[200, 200],
            qss='background : green'
        )
        self.TerminalDock.setWidgets(
            minh=150,
            minw=150,
            qss='background : silver'
        )
        self.StatusBar.setWidgets(
            maxh=50,
            qss='background : pink'
        )
        return self

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='',
        icon=ImageType.APP_LOGO
    )
    ui = EditorSelf()
    ui.setWidgets()
    ui.setMinimumSize(QSize(800, 600))
    ui.show()
    app.exec()