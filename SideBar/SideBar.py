from typing import *
from random import choice
from OptQt.OptimizeQt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qtawesome import icon as qticon

from Sources import *

class DragLabel(OptLabel):
    def __init__(self):
        super().__init__()
        self.initDragPos = [0, 0]
        self.__RandomTips = [
            "Tips1", "Tips2", "Tips3", "Tips4", "Tips5", "Tips6"
        ]

        self.setToolTip(choice(self.__RandomTips))

        self.__Timer = QTimer(self)
        self.__Timer.timeout.connect(lambda : self.setToolTip(choice(self.__RandomTips)))
        self.__Timer.start(5000)

    def setDragEvent(self, canDrag: bool = True):
        if canDrag:
            self.mousePressEvent = self.customMousePressEvent
            self.mouseMoveEvent = self.customMouseMoveEvent
        else:
            self.mousePressEvent = super().mousePressEvent
            self.mouseMoveEvent = super().mouseMoveEvent

    def customMousePressEvent(self, e: QMouseEvent) -> None:
        self.initDragPos[0] = e.x()
        self.initDragPos[1] = e.y()

    def customMouseMoveEvent(self, e: QMouseEvent):
        x = e.x() - self.initDragPos[0]
        y = e.y() - self.initDragPos[1]
        pos = QPoint(x, y)
        self.move(self.mapToParent(pos))

class SideBar(QScrollArea, AbstractWidget):
    def __init__(self):
        super().__init__()

        self.VBoxLeft = OptVBox()
        self.VBoxRight = OptVBox()
        self.Hbox = OptHBox()

        # leftArea
        self.button_Hide = OptToolButton()
        self.button_Home = OptToolButton()
        self.button_ToolBox = OptToolButton()
        self.button_Analysis = OptToolButton()
        self.button_Setting = OptToolButton()

        # rightArea
        self.PluginAreaBtn = OptToolButton()
        self.TrickLabel = DragLabel()

        self.ButtonMapping = {
            0: self.button_Hide,
            1: self.button_Home,
            2: self.button_ToolBox,
            3: self.button_Analysis,
            4: self.button_Setting,
            5: self.PluginAreaBtn,
        }

        self.setUI()

    def setUI(self):
        self.setLayout(self.Hbox.setLays(lays=[self.VBoxLeft, self.VBoxRight]))
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        Keys_hide = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_S), self)
        Keys_home = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_H), self)
        Keys_toolbox = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_B), self)
        Keys_analy = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_A), self)
        Keys_setting = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_C), self)
        Keys_plugin = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_P), self)

        Keys_hide.activated.connect(lambda : self.ButtonMapping[0].click())
        Keys_home.activated.connect(lambda: self.ButtonMapping[1].click())
        Keys_toolbox.activated.connect(lambda: self.ButtonMapping[2].click())
        Keys_analy.activated.connect(lambda: self.ButtonMapping[3].click())
        Keys_setting.activated.connect(lambda: self.ButtonMapping[4].click())
        Keys_plugin.activated.connect(lambda: self.ButtonMapping[5].click())

    def setWidgets(self,
                   hide_function: Callable = lambda: ...,
                   home_function: Callable = lambda: ...,
                   toolbox_function: Callable = lambda: ...,
                   analysis_function: Callable = lambda: ...,
                   setting_function: Callable = lambda: ...,
                   plugin_function : Callable = lambda : ...,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)

        self.button_Hide.setWidgets(
            text="Hide      ",
            icon=qticon('ei.align-justify', color='white'),
            maxh=100,
            maxw=600,
            function=hide_function,
            icon_fixed=False,
            icon_size=[400, 100],
            cursor=CursorType.Link,
            objectName='button_Hide',
            tips='主界面面板\nCtrl+Shift+S'
        )
        self.button_Home.setWidgets(
            text="Home      ",
            icon=qticon('fa.home', color='white'),
            maxh=100,
            maxw=600,
            function=home_function,
            icon_fixed=False,
            icon_size=[400, 100],
            cursor=CursorType.Link,
            objectName='button_Home',
            tips='Home界面\nCtrl+Shift+H'
        )
        self.button_ToolBox.setWidgets(
            text="Box       ",
            icon=qticon('fa5s.cubes', color='white'),
            maxh=100,
            maxw=600,
            function=toolbox_function,
            icon_fixed=False,
            icon_size=[400, 100],
            cursor=CursorType.Link,
            objectName='button_ToolBox',
            tips='Home界面\nCtrl+Shift+B'
        )
        self.button_Analysis.setWidgets(
            text="Analysis      ",
            icon=qticon('mdi.table-sync', color='white'),
            maxh=100,
            maxw=600,
            function=analysis_function,
            icon_fixed=False,
            icon_size=[400, 100],
            cursor=CursorType.Link,
            objectName='button_Analysis',
            tips='数据分析\nCtrl+Shift+A'
        )
        self.button_Setting.setWidgets(
            text="Settings      ",
            icon=qticon('fa5s.cogs', color='white'),
            maxh=100,
            maxw=600,
            function=setting_function,
            icon_fixed=False,
            icon_size=[400, 100],
            cursor=CursorType.Link,
            objectName='button_Setting',
            tips='设置\nCtrl+Shift+C'
        )

        self.VBoxLeft.setWidgets(
            widgets=[self.button_Hide, self.button_Home, self.button_ToolBox,
                     self.button_Analysis, self.button_Setting]
        ).setCommonAlign(Qt.AlignTop)

        self.PluginAreaBtn.setWidgets(
            text="PluginsArea      ",
            icon=qticon('ph.package-bold', color='white'),
            maxh=100,
            maxw=600,
            function=plugin_function,
            icon_fixed=False,
            icon_size=[400, 100],
            cursor=CursorType.Link,
            objectName='PluginAreaBtn',
            tips='插件系统\nCtrl+Shift+p'
        )

        self.VBoxRight.setWidgets(
            widgets=[
                self.PluginAreaBtn,
                self.TrickLabel.setWidgets(
                    fixSize=(350, 350),
                    objectName='TrickLabel',
                    text_model=False,
                    img_model=True,
                    cursor=CursorType.Move,
                )
            ],
            aligns=[Qt.AlignTop, Qt.AlignBottom | Qt.AlignRight]
        )
        return self

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='SideBar',
        icon=ImageType.APP_LOGO
    )
    ui = SideBar()
    ui.setWidgets()
    ui.show()
    app.exec()