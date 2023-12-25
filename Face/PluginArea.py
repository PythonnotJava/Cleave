from typing import *
from importlib.util import spec_from_file_location, module_from_spec
from OptQt.OptimizeQt import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from qtawesome import icon as qticon
from Sources import *
from Util import has_parameter


class _ToolsCore(OptTabWidget):
    visibleSelf = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.visibleSelf.connect(lambda: self.setVisible(bool(self.count())))

    def removeTab(self, index: int) -> None:
        super().removeTab(index)
        self.visibleSelf.emit()

    def addTab(self, *args) -> None:
        super().addTab(*args)
        self.visibleSelf.emit()


class PluginArea(AbstractWidget):

    def __init__(self):
        super().__init__()

        self.ToolsCore = _ToolsCore()

        self.PluginHomePage = OptLabel().setWidgets(
            text_model=True,
            text='''
                    <br>
                    <br>
                    <h1><em>CML Editor</em></h1>
                    <br><br>
                    <h2>CML Editor是Cleave内置的CML语言的专用编辑器，为您提供了一套独特的效率工作流
                    <br>
                    <br>
                    <p>
                        访问开源地址：
                        <a href="https://github.com/PythonnotJava">https://github.com/PythonnotJava</a>
                    </p>
                    </h2>        
                    <h2>
                        <p>
                            快速开始一个文档的建立：
                            <b style="color:gold;font-size:26px;"><kbd>Ctrl</kbd>+<kbd>R</kbd></b>
                        </p>
                        <p>
                            快速开始一个文档的建立：
                            <b style="color:gold;font-size:26px;"><kbd>Ctrl</kbd>+<kbd>R</kbd></b>
                        </p>
                        <p>
                            快速开始一个文档的建立：
                            <b style="color:gold;font-size:26px;"><kbd>Ctrl</kbd>+<kbd>R</kbd></b>
                        </p>
                    </h2> 
                ''',
        )
        self.setUI()

    def setUI(self):
        self.setAcceptDrops(True)
        self.setLayout(OptHBox().setWidgets(widgets=[self.ToolsCore], aligns=[Qt.Alignment()]))

    def dragEnterEvent(self, e: QDragEnterEvent, *args):
        if e.mimeData() is not None and e.mimeData().hasUrls() and self.ToolsCore.count() == 0:
            e.acceptProposedAction()

    def dropEvent(self, e: QDropEvent, *args):
        if e.mimeData().hasUrls() and self.ToolsCore.count() == 0:
            url = e.mimeData().urls()[0]
            filePath = url.toLocalFile()
            if filePath.endswith('.py'):
                try:
                    self.setDynamicPluginLoad(filePath)
                except:
                    print("载入错误!")
            else:
                print("不支持的文件类型!")

    def paintEvent(self, e: QPaintEvent, *args):
        cenpos: QPoint = self.getSelfCenterPos()
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(5)
        painter.setFont(
            OptFont().setAttributes(
                size=14,
                bold=True,
                family='黑体',
                weight=900
            )
        )
        painter.setPen(pen)
        pixmap = QPixmap(ImageType.Drag)
        painter.drawPixmap(
            cenpos.x() - 200,
            cenpos.y() - 300,
            pixmap.scaled(400, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        )
        painter.drawText(QPoint(cenpos.x() - 200, cenpos.y() + 40), "1. 拖入插件文件可以临时载入")
        painter.drawText(QPoint(cenpos.x() - 200, cenpos.y() + 90), '2. 鼠标右键任意区域可以打开菜单栏')
        painter.drawText(QPoint(cenpos.x() - 200, cenpos.y() + 140), '3. 最多允许加载一个临时插件')
        if painter.isActive():
            painter.end()

    def setWidgets(self,
                   **kwargs
                   ) -> "PluginArea":
        self.baseCfg(**kwargs)
        self.ToolsCore.setWidgets(
            tabCursor=CursorType.Link,
            tabsShape=QTabWidget.TabShape.Rounded,
            position=QTabWidget.TabPosition.North,
            enClosed=True,
            movable=True,
            closeTab=lambda index: self.ToolsCore.removeTab(index),
        ).addWidget(
            TabWidgetDict(
                enabled=True,
                icon=qticon('mdi.home-circle-outline'),
                text='插件主页介绍',
                tips='插件主页',
                widget=self.PluginHomePage
            )
        )
        return self

    def setNewPluginLoad(self, **kwargs) -> None:
        self.ToolsCore.addWidget(TabWidgetDict(**kwargs))

    def setDynamicPluginLoad(self, linkFile: str):
        if linkFile is not None:
            spec = spec_from_file_location("pkg", linkFile)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, 'main'):
                func = getattr(module, 'main')
                if has_parameter(func, 'widget'):
                    __keyword: dict = func(widget=True)
                    self.setNewPluginLoad(
                        enabled=True,
                        icon=__keyword.get('icon', None),
                        text=__keyword.get('text', None),
                        widget=__keyword.get('widget', None),
                        tips=__keyword.get('tips', None)
                    )
                else:
                    func()
            else:
                print("没有main入口!!")
        else:
            print('没有相关文件!')

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.MouseButton.RightButton and self.ToolsCore.count() == 0:
            menu = OptMenu(self)
            menu.setWidgets(
                enable=True,
                widgets={
                    OptAction().setWidgets(
                        parent=menu,
                        text='主页',
                        function=lambda: self.ToolsCore.addWidget(
                            TabWidgetDict(
                                enabled=True,
                                icon=qticon('mdi.home-circle-outline'),
                                text='插件主页介绍',
                                tips='插件主页',
                                widget=self.PluginHomePage
                            )
                        )
                    ): 1,
                    OptAction().setWidgets(
                        parent=menu,
                        text='打开插件路径',
                        function=lambda: ...
                    ): 1,
                    OptAction().setWidgets(
                        parent=menu,
                        text='永久导入插件',
                        function=lambda: ...
                    ): 1,
                    OptAction().setWidgets(
                        parent=menu,
                        text='移除插件',
                        function=lambda: ...
                    ): 1,
                    OptAction().setWidgets(
                        parent=menu,
                        text='禁用插件',
                        function=lambda: ...
                    ): 1
                }
            )
            menu.exec_(self.mapToGlobal(e.pos()))
        super().mousePressEvent(e)


if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='PluginArea',
        icon=ImageType.APP_LOGO
    )
    ui = PluginArea().setWidgets()
    ui.show()
    app.exec()
