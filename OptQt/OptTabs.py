from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from typing import *
from PyQt5.QtGui import *
from OptQt.OptimizeQt import *
from OptQt.OptComponent import *
from Sources import CursorType
from OptQt.FunctionBar import FunctionsBar

# 上部头部操作栏目
class Navigator(AbstractWidget):
    __slots__ = ('ToolBar', 'StackManager', 'FunctionsBar', 'StartTab', 'ToolTab', 'HelpTab', 'Vbox')

    def __init__(self):
        super().__init__()

        self.ToolBar = OptTabBar()
        self.StackManager = OptStack()
        self.FunctionsBar = FunctionsBar()

        # tabs
        self.StartTab = StartBar()
        self.ToolTab = ExcelToolBox()
        self.HelpTab = OptLabel()

        self.Vbox = OptVBox()

        self.setUI()
    def setUI(self):
        self.setLayout(self.Vbox)

    def setWidgets(self,
                   familys : Iterable = ('微软雅黑',),
                   sizes : Iterable = (12, ),
                   open_function: Callable = lambda: ...,
                   just_save_function: Callable = lambda: ...,
                   save_as_function: Callable = lambda: ...,
                   help_function: Callable = lambda: ...,
                   font_family_function: Callable = lambda: ...,
                   font_size_function: Callable = lambda: ...,
                   align_left_function: Callable = lambda: ...,
                   align_center_function: Callable = lambda: ...,
                   align_right_function: Callable = lambda: ...,
                   jump_function : Callable = lambda : ...,
                   thaw_function : Callable = lambda : ...,
                   format_function : Callable = lambda : ...,
                   **kwargs
                   ) -> 'Navigator':

        self.baseCfg(**kwargs)

        self.Vbox.setWidgets(
            widgets=[
                self.ToolBar,
                self.StackManager,
                self.FunctionsBar
            ],
            aligns=[Qt.AlignLeft, Qt.Alignment(), Qt.AlignLeft]
        )

        self.ToolBar.setWidgets(
            tabs=['开始', '工具', '帮助'],
            drawBase=True,
            objectName='TabView-ToolBar',
            cursor=CursorType.Link,
            maxh=40,
            toggle_function=self.setToggleTab
        )

        self.StackManager.setWidgets(
            currentIndex=0,
            widgets=[
                self.StartTab.setWidgets(
                    familys=familys,
                    sizes=sizes,
                    open_function=open_function,
                    just_save_function=just_save_function,
                    save_as_function=save_as_function,
                    help_function=help_function,
                    font_family_function=font_family_function,
                    font_size_function=font_size_function,
                    align_left_function=align_left_function,
                    align_center_function=align_center_function,
                    align_right_function=align_right_function,
                    thaw_function=thaw_function,
                    format_function=format_function,
                    cursor=CursorType.Working,
                    objectName='StartTab'
                ),
                self.ToolTab.setWidgets(
                    cursor=CursorType.Working,
                    objectName='ToolTab',
                ),
                self.HelpTab.setWidgets(
                    text_model=True,
                    text='Help',
                    cursor=CursorType.Working,
                    objectName='HelpTab',
                    qss='background : tan'
                )
            ],
            objectName='TabView-StackManager',
            cursor=CursorType.Busy,
        )

        self.FunctionsBar.setWidgets(
            maxh=50,
            objectName='TabView-FunctionsBar',
            cursor=CursorType.Busy,
            jump_function=jump_function
        )

        return self

    def setToggleTab(self):
        self.StackManager.setCurrentIndex(self.ToolBar.currentIndex())

if __name__ == '__main__':
    app = QApplication([])
    ui = Navigator()
    ui.setWidgets()
    ui.show()
    app.exec()