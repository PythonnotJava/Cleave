from typing import *
from os import system as os_system
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Sources import *
from OptQt.OptimizeQt import *
from OptQt.QTyping import QssSetter


class _CellManager(AbstractWidget):

    def __init__(self):
        super().__init__()
        self.GlobalBackgroundColorBtn = OptPushButton()
        self.GlobalForegroundColorBtn = OptPushButton()
        self.GlobalHighlightColorBtn = OptPushButton()
        self.SelectForegroundColorBtn = OptPushButton()
        self.SelectBackgroundColorBtn = OptPushButton()
        self.SelectBorderWidthBtn = OptPushButton()
        self.SelectBorderColorBtn = OptPushButton()
        self.LinkForegroundColorBtn = OptPushButton()
        self.LinkBackgroundColorBtn = OptPushButton()
        self.LinkBorderWidthBtn = OptPushButton()
        self.LinkBorderColorBtn = OptPushButton()
        self.FrozenBackgroundColorBtn = OptPushButton()
        self.FrozenForegroundColorBtn = OptPushButton()

    def setWidgets(self,
                   common_backgroundcolor: QColor = QColor(240, 240, 240),
                   common_foregroundcolor: QColor = QColor(5, 5, 5),
                   common_hightlightColor: QColor = QColor('skyblue'),
                   linkedCellStyle: QssSetter = QssSetter(
                       color=QColor('gold'),
                       background_color=QColor('#e923fb'),
                       border_radius=15,
                       border_color=QColor('#e923fb')
                   ),
                   selectCellStyle: QssSetter = QssSetter(
                       border_color=QColor('tan'),
                       border_width=12,
                       border_style='solid',
                       color=QColor(5, 5, 5),
                       background_color=QColor(240, 240, 240),
                       target_with_actions='QTableWidget::item:selected'
                   ),
                   frozenCellStyle: QssSetter = QssSetter(
                       background_color=QColor('gray'),
                       color=QColor('cyan')
                   ),
                   global_background_color_function: Callable = lambda: ...,
                   global_foreground_color_function: Callable = lambda: ...,
                   global_highlight_color_function: Callable = lambda: ...,

                   select_foreground_color_function: Callable = lambda: ...,
                   select_background_color_function: Callable = lambda: ...,
                   select_border_width_function: Callable = lambda: ...,
                   select_border_color_function: Callable = lambda: ...,

                   link_foreground_color_function: Callable = lambda: ...,
                   link_background_color_function: Callable = lambda: ...,
                   link_border_width_function: Callable = lambda: ...,
                   link_border_color_function: Callable = lambda: ...,

                   frozen_foreground_color_function: Callable = lambda: ...,
                   frozen_background_color_function: Callable = lambda: ...,
                   **kwargs
                   ) -> '_CellManager':
        return self.layoutFactoryConstructor(
            hbox=False,
            fixSize=(580, 580),
            widgets_lays=[
                WidgetOrLayoutDict(
                    dtype=1,
                    align=Qt.AlignLeft,
                    obj=OptLabel().setWidgets(
                        text='全局单元格设置',
                        maxh=60,
                    )
                ),
                WidgetOrLayoutDict(
                    dtype=1,
                    align=Qt.Alignment(),
                    obj=PartingLine().setWidgets(
                        horizontal=True,
                        width_or_heightr=5,
                    )
                ),
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptVBox().setLays(
                        lays=[
                            OptHBox().setWidgets(
                                widgets=[
                                    OptLabel().setWidgets(text='背景颜色'),
                                    self.GlobalBackgroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=global_background_color_function,
                                        qss=f'background-color : {common_backgroundcolor.name()}',
                                        cursor=CursorType.Link,
                                        objectName='gbtn1'
                                    ),
                                    OptLabel().setWidgets(text='前景颜色'),
                                    self.GlobalForegroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=global_foreground_color_function,
                                        qss=f'background-color : {common_foregroundcolor.name()}',
                                        cursor=CursorType.Link,
                                        objectName='gbtn2'
                                    ),
                                    OptLabel().setWidgets(text='高亮颜色'),
                                    self.GlobalHighlightColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=global_highlight_color_function,
                                        qss=f'background-color : {common_hightlightColor.name()}',
                                        cursor=CursorType.Link,
                                        objectName='gbtn3'
                                    )
                                ]
                            ),
                            OptHBox().setWidgets(
                                widgets=[
                                    OptLabel().setWidgets(text='选中样式'),
                                    self.SelectForegroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=select_foreground_color_function,
                                        qss=f'background-color : {selectCellStyle.color.name()};',
                                        tips='选中时前景颜色',
                                        cursor=CursorType.Link,
                                        objectName='gbtn4'
                                    ),
                                    self.SelectBackgroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=select_background_color_function,
                                        qss=f'background-color : {selectCellStyle.background_color.name()};',
                                        tips='选中时背景颜色',
                                        cursor=CursorType.Link,
                                        objectName='gbtn5'
                                    ),
                                    self.SelectBorderWidthBtn.setWidgets(
                                        text_model=True,
                                        icon_model=False,
                                        function=select_border_width_function,
                                        text=str(selectCellStyle.border_width),
                                        tips='选中时边框厚度',
                                        cursor=CursorType.Link,
                                        objectName='gbtn6'
                                    ),
                                    self.SelectBorderColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=select_border_color_function,
                                        qss=f'border : 5px solid {selectCellStyle.border_color.name()}',
                                        tips='选中时边框颜色（边框厚度至少为1）',
                                        cursor=CursorType.Link,
                                        objectName='gbtn7'
                                    )
                                ]
                            ).setCommonAlign(Qt.AlignVCenter)
                        ]
                    )
                ),
                WidgetOrLayoutDict(
                    dtype=1,
                    align=Qt.Alignment(),
                    obj=PartingLine().setWidgets(
                        horizontal=True,
                        width_or_heightr=10,
                    )
                ),
                WidgetOrLayoutDict(
                    dtype=1,
                    align=Qt.AlignLeft,
                    obj=OptLabel().setWidgets(
                        text='特殊单元格设置',
                        maxh=60
                    )
                ),
                WidgetOrLayoutDict(
                    dtype=1,
                    align=Qt.Alignment(),
                    obj=PartingLine().setWidgets(
                        horizontal=True,
                        width_or_heightr=5,
                    )
                ),
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptVBox().setLays(
                        lays=[
                            OptHBox().setWidgets(
                                widgets=[
                                    OptLabel().setWidgets(text='链接单元格'),
                                    self.LinkForegroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=link_foreground_color_function,
                                        qss=f'background-color : {linkedCellStyle.color.name()}',
                                        tips='链接单元格前景颜色',
                                        cursor=CursorType.Link,
                                        objectName='lbtn1'
                                    ),
                                    self.LinkBackgroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=link_background_color_function,
                                        qss=f'background-color : {linkedCellStyle.background_color.name()}',
                                        tips='链接单元格背景颜色',
                                        cursor=CursorType.Link,
                                        objectName='lbtn2'
                                    ),
                                    self.LinkBorderWidthBtn.setWidgets(
                                        text_model=True,
                                        text=str(linkedCellStyle.border_width),
                                        icon_model=False,
                                        function=link_border_width_function,
                                        tips='链接单元格边框厚度',
                                        cursor=CursorType.Link,
                                        objectName='lbtn3'
                                    ),
                                    self.LinkBorderColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=link_border_color_function,
                                        qss=f'border : 5px solid {linkedCellStyle.border_color.name()}',
                                        tips='链接单元格边框颜色',
                                        cursor=CursorType.Link,
                                        objectName='lbtn4'
                                    )
                                ]
                            ),
                            OptHBox().setWidgets(
                                widgets=[
                                    OptLabel().setWidgets(text='冻结单元格'),
                                    self.FrozenBackgroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=frozen_background_color_function,
                                        cursor=CursorType.Link,
                                        qss=f'background-color : {frozenCellStyle.background_color.name()}',
                                        tips='冻结单元格背景颜色',
                                        objectName='lbtn5'
                                    ),
                                    self.FrozenForegroundColorBtn.setWidgets(
                                        text_model=False,
                                        icon_model=False,
                                        function=frozen_foreground_color_function,
                                        cursor=CursorType.Link,
                                        qss=f'background-color : {frozenCellStyle.color.name()}',
                                        tips='冻结单元格前景颜色',
                                        objectName='lbtn6'
                                    )
                                ]
                            )
                        ]
                    ).setCommonAlign(Qt.AlignVCenter)
                )
            ],
            **kwargs
        )

class AdtDlg(QDialog, AbstractWidget):
    def __init__(self):
        super().__init__()

        self.TabTools = OptTabWidget()
        self.CellManager = _CellManager()
        self.Other = OptLabel()

        self.setUI()

    def setUI(self):
        ...

    def event(self, e: QEvent):
        if e.type() == QEvent.Type.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            os_system('start https://www.robot-shadow.cn')
        return super().event(e)

    def setWidgets(self,
                   modal: bool = True,
                   title: Optional[str] = None,
                   icon: Optional[Union[str, QIcon]] = None,

                   # CellManager
                   common_backgroundcolor: QColor = QColor(240, 240, 240),
                   common_foregroundcolor: QColor = QColor(5, 5, 5),
                   common_hightlightColor: QColor = QColor('skyblue'),
                   linkedCellStyle: QssSetter = QssSetter(
                       color=QColor('gold'),
                       background_color=QColor('#e923fb'),
                       border_radius=15,
                       border_color=QColor('#e923fb')
                   ),
                   selectCellStyle: QssSetter = QssSetter(
                       border_color=QColor('tan'),
                       border_width=12,
                       border_style='solid',
                       color=QColor(5, 5, 5),
                       background_color=QColor(240, 240, 240),
                       target_with_actions='QTableWidget::item:selected'
                   ),
                   frozenCellStyle: QssSetter = QssSetter(
                       background_color=QColor('gray'),
                       color=QColor('cyan')
                   ),
                   global_background_color_function: Callable = lambda: ...,
                   global_foreground_color_function: Callable = lambda: ...,
                   global_highlight_color_function: Callable = lambda: ...,

                   select_foreground_color_function: Callable = lambda: ...,
                   select_background_color_function: Callable = lambda: ...,
                   select_border_width_function: Callable = lambda: ...,
                   select_border_color_function: Callable = lambda: ...,

                   link_foreground_color_function: Callable = lambda: ...,
                   link_background_color_function: Callable = lambda: ...,
                   link_border_width_function: Callable = lambda: ...,
                   link_border_color_function: Callable = lambda: ...,

                   frozen_foreground_color_function: Callable = lambda: ...,
                   frozen_background_color_function: Callable = lambda: ...,

                   currentIndex : int = 0,
                   **kwargs
                   ) -> "AdtDlg":
        self.baseCfg(**kwargs)
        self.setModal(modal)

        if title is not None:
            self.setWindowTitle(title)

        if icon is not None:
            if isinstance(icon, str):
                self.setWindowIcon(QIcon(icon))
            else:
                self.setWindowIcon(icon)

        self.TabTools.setWidgets(
            currentIndex=currentIndex,
            rect=(10, 10, 580, 580),
            parent=self,
            enClosed=False,
            tabSets=[
                TabWidgetDict(
                    text='属性',
                    tips='对单元格属性进行设置',
                    widget=self.CellManager.setWidgets(
                        common_backgroundcolor=common_backgroundcolor,
                        common_foregroundcolor=common_foregroundcolor,
                        common_hightlightColor=common_hightlightColor,
                        linkedCellStyle=linkedCellStyle,
                        selectCellStyle=selectCellStyle,
                        frozenCellStyle=frozenCellStyle,
                        global_background_color_function=global_background_color_function,
                        global_foreground_color_function=global_foreground_color_function,
                        global_highlight_color_function=global_highlight_color_function,
                        select_foreground_color_function=select_foreground_color_function,
                        select_background_color_function=select_background_color_function,
                        select_border_width_function=select_border_width_function,
                        select_border_color_function=select_border_color_function,
                        link_foreground_color_function=link_foreground_color_function,
                        link_background_color_function=link_background_color_function,
                        link_border_width_function=link_border_width_function,
                        link_border_color_function=link_border_color_function,
                        frozen_foreground_color_function=frozen_foreground_color_function,
                        frozen_background_color_function=frozen_background_color_function
                    ),
                    enabled=True,
                    icon=None
                ),
                TabWidgetDict(
                    text='其他',
                    tips='其他',
                    widget=self.Other.factoryConstructor(qss='background-color : green;fixSize=(580, 580)'),
                    enabled=True,
                    icon=None
                )
            ],
        )
        return self


if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='AdtDlg',
        icon=ImageType.APP_LOGO
    )
    ui = AdtDlg()
    ui.setWidgets()
    ui.show()
    app.exec()
