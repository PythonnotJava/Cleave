# 临时音乐插件样例
from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import *

from OptQt.OptimizeQt import *

class MusicMedia(QMainWindow, AbstractWidget):
    def __init__(self):
        super().__init__()

        self.MenuBar = OptMenuBar()
        self.CoreWidget = OptSplitter()
        self.MusicList = QListWidget()
        self.OperatorBar = OptSlider()

        self.setUI()
    def setUI(self):
        self.setMenuWidget(self.MenuBar)
        self.setCentralWidget(self.CoreWidget)

    def setWidgets(self) -> 'MusicMedia':
        fileMenu = OptMenu(self.MenuBar)
        self.MenuBar.setWidgets(
            widgets={
                fileMenu.setWidgets(
                    title='文件',
                    widgets={
                        OptAction().setWidgets(
                            parent=fileMenu,
                            text='载入文件目录'
                        ) : 1,
                        OptAction().setWidgets(
                            parent=fileMenu,
                            text='添加文件目录'
                        ): 1
                    }
                ) : 0,
                OptAction().setWidgets(
                    parent=self.MenuBar,
                    text='设置'
                ) : 1
            }
        )

        self.CoreWidget.setWidgets(
            widgets=[
                self.MusicList,
                self.OperatorBar
            ],
            horizontal=False,
            handleWidth=10,
            qss='QSplitter:handle {background-color : tan;}'
        )

        self.OperatorBar.setWidgets(
            minNumber=0,
            maxNumber=100,
            defaultValue=10,
            step=1
        )

        return self

def main(widget=True,
         icon=None,
         text='音乐',
         tips='临时加载音乐插件'
         ) -> dict:
    return dict(
        widget=MusicMedia().setWidgets(),
        icon=icon,
        text=text,
        tips=tips
    )

if __name__ == '__main__':
    app = OptAppication([])
    ui = MusicMedia()
    ui.setWidgets().setMinimumSize(800, 600)
    ui.show()
    app.exec()


__all__ = ['main']