# 组合类控件的实现
from typing import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from qtawesome import icon as qticon

from Sources import ImageType, CursorType

from OptQt.OptimizeQt import (AbstractWidget, OptPushButton, OptLabel, OptSlider, OptDlg,
                              OptSplitter, OptComBox, OptLineEdit, OptHBox, OptVBox, OptToolButton,
                              OptThread, PartingLine, OptStatusBar, CircleProgressBar, OptAppication)
from Sources import *
from OptQt.QTyping import WidgetOrLayoutDict

# 插件
class OptToolCompose(AbstractWidget):
    __slots__ = ('Button', 'Introduction', 'VerSplitter', 'HorSplitter', 'Description', 'Hbox')

    def __init__(self):
        super().__init__()

        self.Button = OptPushButton()

        self.Introduction = OptLabel()

        self.VerSplitter = OptSplitter()
        self.HorSplitter = OptSplitter()

        self.Description = OptLabel()

        self.Hbox = QHBoxLayout()

        self.setUI()

    def setUI(self):
        self.Hbox.addWidget(self.VerSplitter, alignment=Qt.Alignment())
        self.setLayout(self.Hbox)

    def setWidgets(self,
                   title: Optional[str] = None,
                   version: Optional[str] = None,
                   author: Optional[str] = None,
                   des: Optional[str] = None,
                   buttonIcon: Optional[str] = None,
                   function: Callable = lambda: ...,
                   shortcuts: Optional[str] = None,
                   collapsible: bool = True,
                   TipShortcuts: bool = True,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.Introduction.setWidgets(
            text="名称：{}\n作者：{}\n版本：{}".format(
                title if title is not None else "",
                author if author is not None else "",
                version if version is not None else ""
            ),
            wrap=True,
            maxh=150,
            x=400
        )

        self.Description.setWidgets(
            text=des if des is not None else "",
            wrap=True,
            minh=50
        )

        self.Button.setWidgets(
            icon=QIcon(QPixmap(buttonIcon if buttonIcon is not None else ImageType.Coper_error_Icon)),
            shortcuts=shortcuts,
            function=function,
            minh=200,
            minw=300,
            maxh=400,
            maxw=300,
            tips=shortcuts if TipShortcuts else None,
            cursor=CursorType.Link
        )

        self.HorSplitter.setWidgets(
            widgets=[
                self.Introduction, self.Description
            ],
            sizes=[10, 70],
            horizontal=False,
            handleIndex=1,
            collapsible=collapsible,
            handleCursor=CursorType.Move
        )

        self.VerSplitter.setWidgets(
            widgets=[
                self.Button, self.HorSplitter
            ],
            handleIndex=1,
            horizontal=True,
            collapsible=collapsible,
            handleCursor=CursorType.Move
        )

        return self


# Ctrl+F弹出栏
class SearchBar(OptDlg):
    __slots__ = ('SearchEdit', 'SearchModel', 'SearchHighlight', 'SearchHbox', 'ConfirmButton', 'ConfirmHbox', 'Hbox')

    def __init__(self):
        super().__init__()

        self.SearchEdit = OptLineEdit()
        self.SearchModel = OptComBox()
        self.SearchHighlight = OptPushButton()
        self.SearchHbox = OptHBox()

        self.ConfirmButton = OptPushButton()
        self.ConfirmHbox = OptHBox()

        self.Vbox = OptVBox()
        self.setUI()

    def setUI(self):
        self.setLayout(self.Vbox)

    @overload
    def setWidgets(self, hideWhatThisButton: bool = True, modal: bool = True, **kwargs):
        ...

    @overload
    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   defaultSets: bool = True,
                   title: Optional[str] = None,
                   icon: str | QIcon | None = None,
                   confirm_function: Callable = lambda: ...,
                   hightlightColor: Optional[QColor] = None,
                   search_model: Qt.MatchFlag = Qt.MatchContains,
                   **kwargs
                   ):
        ...

    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   defaultSets: bool = True,
                   title: str = "单元格搜索栏",
                   icon: Optional[QIcon] = None,
                   confirm_function: Callable = lambda: ...,
                   hightlightColor: QColor = QColor('skyblue'),
                   search_model: int = 0,
                   hightlight_funciton: Callable = lambda: ...,
                   **kwargs
                   ):
        if defaultSets:
            self.setWindowTitle(title)
            if icon is not None:
                self.setWindowIcon(icon)

            self.Vbox.setLays(
                lays=[self.SearchHbox, self.ConfirmHbox]
            )

            self.SearchHbox.setWidgets(
                widgets=[
                    self.SearchEdit.setWidgets(
                        enable=True,
                        maxh=40,
                        minw=150,
                        objectName='SearchEdit',
                        cursor=CursorType.Text,
                    ),
                    self.SearchModel.setWidgets(
                        items=['直接搜索（推荐）', '完全匹配', '前缀匹配', '后缀匹配', '正则匹配'],
                        currentIndex=search_model,
                        maxh=40,
                        minw=40,
                        maxw=150,
                        objectName='SearchModel',
                        cursor=CursorType.Link,
                    ),
                    self.SearchHighlight.setWidgets(
                        function=hightlight_funciton,
                        icon_model=False,
                        text_model=False,
                        objectName='SearchHighlight',
                        maxh=40,
                        minw=40,
                        maxw=80,
                        cursor=CursorType.Link,
                        qss=f'background-color : {hightlightColor.name()}'
                    )
                ],
                aligns=[Qt.Alignment(), Qt.Alignment(), Qt.Alignment()]
            )

            self.ConfirmHbox.setWidgets(
                widgets=[
                    self.ConfirmButton.setWidgets(
                        function=confirm_function,
                        objectName='SearchHighlight',
                        maxh=40,
                        minw=60,
                        maxw=100,
                        text='确定',
                        icon_model=False,
                        text_model=True,
                        cursor=CursorType.Link,
                    )
                ],
                aligns=[Qt.AlignRight]
            )

        return super().setWidgets(
            hideWhatThisButton=hideWhatThisButton,
            modal=True,
            **kwargs
        )


# 开始栏，也是默认的操作栏
class StartBar(AbstractWidget):
    __slots__ = (
        'OpenBtn', 'JustSaveBtn', 'SaveAsBtn', 'OpenLabel', 'OpenEdit', 'HelpBtn', 'Hbox1', 'DivideLine',
        'FontFamilyBox',
        'FontSizeBox', 'FormatBoxBtn', 'AlignLeftBtn', 'AlignCenterBtn', 'AlignRightBtn', 'ThawBtn', 'Hbox2', 'Vbox'
    )

    def __init__(self):
        super().__init__()
        # 第一行
        self.OpenBtn = OptPushButton()
        self.JustSaveBtn = OptPushButton()
        self.SaveAsBtn = OptPushButton()
        self.OpenLabel = OptLabel()
        self.OpenEdit = OptLineEdit()
        self.HelpBtn = OptPushButton()
        self.Hbox1 = OptHBox()

        # 分割线
        self.DivideLine = PartingLine()

        # 第二行
        self.FontFamilyBox = OptComBox()
        self.FontSizeBox = OptComBox()
        self.FormatBoxBtn = OptPushButton()
        self.AlignLeftBtn = OptPushButton()
        self.AlignCenterBtn = OptPushButton()
        self.AlignRightBtn = OptPushButton()
        self.ThawBtn = OptPushButton()

        self.Hbox2 = OptHBox()

        self.Vbox = OptVBox()
        self.setUI()

    def setUI(self):
        self.setLayout(self.Vbox)
        self.Vbox.addLayout(self.Hbox1)
        self.Vbox.addWidget(self.DivideLine, alignment=Qt.Alignment())
        self.Vbox.addLayout(self.Hbox2)

    def setWidgets(self,
                   familys: Iterable = ('微软雅黑',),
                   sizes: Iterable = (12,),
                   open_function: Callable = lambda: ...,
                   just_save_function: Callable = lambda: ...,
                   save_as_function: Callable = lambda: ...,
                   help_function: Callable = lambda: ...,
                   font_family_function: Callable = lambda: ...,
                   font_size_function: Callable = lambda: ...,
                   align_left_function: Callable = lambda: ...,
                   align_center_function: Callable = lambda: ...,
                   align_right_function: Callable = lambda: ...,
                   thaw_function: Callable = lambda: ...,
                   format_function: Callable = lambda: ...,
                   **kwargs
                   ):
        self.Hbox1.setWidgets(
            widgets=[
                self.OpenBtn.setWidgets(
                    function=open_function,
                    icon_model=True,
                    icon_fixed=True,
                    icon=qticon('ei.folder-open'),
                    objectName='OperatorBar-OpenBtn',
                    cursor=CursorType.Link,
                    tips='打开文件',
                    maxh=50,
                    maxw=50,
                ),
                self.JustSaveBtn.setWidgets(
                    function=just_save_function,
                    icon_model=True,
                    icon_fixed=True,
                    icon=qticon('fa5s.save'),
                    objectName='OperatorBar-JustSaveBtn',
                    cursor=CursorType.Link,
                    tips='保存',
                    maxh=50,
                    maxw=50,
                ),
                self.SaveAsBtn.setWidgets(
                    function=save_as_function,
                    icon_model=True,
                    icon_fixed=True,
                    icon=qticon('msc.save-as'),
                    objectName='OperatorBar-SaveAsBtn',
                    cursor=CursorType.Link,
                    tips='另存为',
                    maxh=50,
                    maxw=50,
                ),
                self.OpenLabel.setWidgets(
                    text="打开",
                    text_model=True,
                    objectName='OperatorBar-OpenLabel',
                    maxh=50,
                    maxw=60,
                ),
                self.OpenEdit.setWidgets(
                    enable=False,
                    objectName='OperatorBar-OpenEdit',
                    maxh=50,
                    minw=400,
                ),
                self.HelpBtn.setWidgets(
                    tips='帮助',
                    function=help_function,
                    objectName='OperatorBar-HelpBtn',
                    maxh=50,
                    maxw=50,
                    icon_model=True,
                    icon_fixed=True,
                    icon=qticon('ei.question-sign'),
                    cursor=CursorType.Link,
                )
            ],
            aligns=[Qt.Alignment(), Qt.Alignment(), Qt.Alignment(), Qt.Alignment(), Qt.AlignLeft, Qt.AlignRight],
        )

        self.DivideLine.setWidgets(
            horizontal=True,
            width=5,
            width_or_heightr=5,
            objectName='OperatorBar-DivideLine'
        )

        self.Hbox2.setWidgets(
            widgets=[
                self.FontFamilyBox.setWidgets(
                    items=familys,
                    currentIndex=0,
                    objectName='OperatorBar-FontFamilyBox',
                    function=font_family_function,
                    cursor=CursorType.Link,
                    minw=100,
                    maxh=50,
                    maxw=150
                ),
                self.FontSizeBox.setWidgets(
                    items=[str(_) for _ in sizes],
                    currentIndex=0,
                    objectName='OperatorBar-FontSizeBox',
                    function=font_size_function,
                    cursor=CursorType.Link,
                    minw=100,
                    maxh=50,
                    maxw=150
                ),
                self.FormatBoxBtn.setWidgets(
                    function=format_function,
                    minw=50,
                    maxh=50,
                    maxw=100,
                    text_model=True,
                    icon_model=False,
                    text='格式  <',
                    objectName='OperatorBar-FormatBoxBtn',
                    cursor=CursorType.Link,
                ),
                self.AlignLeftBtn.setWidgets(
                    tips='左对齐',
                    function=align_left_function,
                    objectName='OperatorBar-AlignLeftBtn',
                    maxh=50,
                    maxw=50,
                    icon_model=True,
                    icon_fixed=True,
                    icon=qticon('fa.align-left'),
                    cursor=CursorType.Link,
                ),
                self.AlignCenterBtn.setWidgets(
                    tips='居中对齐',
                    function=align_center_function,
                    objectName='OperatorBar-AlignCenterBtn',
                    maxh=50,
                    maxw=50,
                    icon_model=True,
                    icon_fixed=True,
                    icon=qticon('ei.align-justify'),
                    cursor=CursorType.Link,
                    enabled=False
                ),
                self.AlignRightBtn.setWidgets(
                    tips='右对齐',
                    function=align_right_function,
                    objectName='OperatorBar-AlignRightBtn',
                    maxh=50,
                    maxw=50,
                    icon_model=True,
                    icon_fixed=True,
                    icon=qticon('fa.align-right'),
                    cursor=CursorType.Link,
                ),
                self.ThawBtn.setWidgets(
                    tips='解冻单元格',
                    function=thaw_function,
                    maxh=50,
                    maxw=50,
                    icon_model=True,
                    icon_fixed=True,
                    objectName='OperatorBar-ThawBtn',
                    icon=qticon('fa.crosshairs'),
                    cursor=CursorType.Link,
                ),
            ],
            aligns=[
                Qt.Alignment(), Qt.Alignment(), Qt.Alignment(), Qt.Alignment(), Qt.Alignment(), Qt.Alignment(),
                Qt.Alignment()
            ]
        )

        self.baseCfg(**kwargs)
        return self


class ExcelToolBox(QScrollArea, AbstractWidget):
    __slots__ = ('Hbox', 'ExpandBtn', 'LockBtn')

    def __init__(self):
        super().__init__()

        self.Hbox = OptHBox()
        self.ExpandBtn = OptToolButton()
        self.LockBtn = OptToolButton()

        self.setUI()

    def setUI(self):
        self.setLayout(self.Hbox)

    def setWidgets(self,
                   expand_function: Callable = lambda: ...,
                   lock_function: Callable = lambda: ...,
                   **kwargs
                   ) -> "ExcelToolBox":
        self.baseCfg(**kwargs)

        self.Hbox.setWidgets(
            widgets=[self.ExpandBtn, self.LockBtn],
            aligns=[Qt.Alignment(), Qt.Alignment()]
        )

        self.ExpandBtn.setWidgets(
            function=expand_function,
            icon_fixed=False,
            icon=QIcon(ImageType.MA_Expand_Tool),
            text='拓展工具',
            objectName='ExcelToolBox-ExpandBtn',
            cursor=CursorType.Link,
            buttonStyle=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
            maxh=150,
            maxw=150,
        )

        self.LockBtn.setWidgets(
            function=lock_function,
            icon_fixed=False,
            icon=QIcon(ImageType.MA_Lock),
            text='加密',
            objectName='ExcelToolBox-LockBtn',
            cursor=CursorType.Link,
            buttonStyle=Qt.ToolButtonStyle.ToolButtonTextUnderIcon,
            maxh=150,
            maxw=150,
        )

        return self


# 带有滑块的状态栏
class StatusBarWithSlider(OptStatusBar):
    __slots = ('ExcelSizeSlider',)

    def __init__(self):
        super().__init__()

        self.ExcelSizeSlider = OptSlider()

    @overload
    def setWidgets(self, statusTip: Optional[str] = None, **kwargs): ...

    @overload
    def setWidgets(self, statusTip: Optional[str] = None, defautltSets: bool = True,
                   slider_function: Callable = lambda: ..., **kwargs): ...

    def setWidgets(self,
                   statusTip: Optional[str] = None,
                   defautltSets: bool = True,
                   slider_function: Callable = lambda: ...,
                   **kwargs
                   ):
        if defautltSets:
            self.addPermanentWidget(
                self.ExcelSizeSlider.setWidgets(
                    minNumber=50,
                    maxNumber=200,
                    defaultValue=100,
                    step=1,
                    function=slider_function,
                    horizontal=True,
                    maxw=150,
                    maxh=20,
                    minw=100,
                    minh=10,
                    cursor=CursorType.Link,
                    objectName='ExcelSizeSlider'
                )
            )

        return super().setWidgets(statusTip, **kwargs)


class ReWriteInputDialog(QDialog, AbstractWidget):
    __slots__ = ('LineEdit', 'OkBtn', 'CancelBtn')
    def __init__(self):
        super().__init__()
        self.LineEdit = OptLineEdit()
        self.OkBtn = OptPushButton()
        self.CancelBtn = OptPushButton()

    def setWidgets(self,
                   labelText: str = '标签',
                   modal: bool = True,
                   title: Optional[str] = None,
                   icon: Optional[Union[QIcon, str]] = None,
                   okBtn_text: str = "好的",
                   cancel_text: str = '取消',
                   okBtn_function: Callable = lambda: ...,
                   cancelBtn_function: Optional[Callable] = None,
                   maxLen: int = 25,
                   edit_minw: int = 200,
                   placeholderText: Optional[str] = None,
                   **kwargs
                   ) -> 'ReWriteInputDialog':
        self.setModal(modal)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        if icon is not None:
            if isinstance(icon, str):
                self.setWindowIcon(QIcon(icon))
            else:
                self.setWindowIcon(icon)
        if title is not None:
            self.setWindowTitle(title)
        return self.layoutFactoryConstructor(
            hbox=False,
            widgets_lays=[
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text_model=True,
                                text=labelText
                            ),
                            self.LineEdit.setWidgets(
                                minw=edit_minw,
                                maxLen=maxLen,
                                cursor=CursorType.Text,
                                placeholderText=placeholderText
                            ).renewModel(
                                model=['http://', 'https://', 'file:///']
                            )
                        ],
                        aligns=[Qt.AlignCenter, Qt.Alignment()]
                    )
                ),  # WidgetOrLayoutDict
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            self.OkBtn.setWidgets(
                                function=okBtn_function,
                                icon_model=False,
                                text_model=True,
                                text=okBtn_text,
                                cursor=CursorType.Link
                            ),
                            self.CancelBtn.setWidgets(
                                function=cancelBtn_function if cancelBtn_function is not None else self.close,
                                icon_model=False,
                                text_model=True,
                                text=cancel_text,
                                cursor=CursorType.Link
                            )
                        ],
                        aligns=[Qt.AlignCenter, Qt.AlignCenter]
                    )
                )  # WidgetOrLayoutDict
            ],
            **kwargs
        )

    def text(self) -> str: return self.LineEdit.text()

class ReWriteAnyWidgetDialog(QDialog, AbstractWidget):
    __slots__ = ('__AnyWidget', )
    def __init__(self):
        super().__init__()

        self.__AnyWidget: Optional[QWidget] = None

    def widget(self) -> Optional[QWidget]:
        return self.__AnyWidget

    def setWidgets(self,
                   widget: Optional[QWidget] = None,
                   labelText: str = '标签',
                   modal: bool = True,
                   title: Optional[str] = None,
                   icon: Optional[Union[QIcon, str]] = None,
                   okBtn_text: str = "好的",
                   cancel_text: str = '取消',
                   okBtn_function: Callable = lambda: ...,
                   cancelBtn_function: Optional[Callable] = None,
                   **kwargs
                   ) -> 'ReWriteAnyWidgetDialog':
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setModal(modal)
        if icon is not None:
            if isinstance(icon, str):
                self.setWindowIcon(QIcon(icon))
            else:
                self.setWindowIcon(icon)
        if title is not None:
            self.setWindowTitle(title)
        if widget is not None:
            self.__AnyWidget = widget
        return self.layoutFactoryConstructor(
            hbox=False,
            widgets_lays=[
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text=labelText,
                                text_model=True
                            ),
                            widget
                        ],
                        aligns=[Qt.Alignment(), Qt.Alignment()]
                    )
                ),  # WidgetOrLayoutDict
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptPushButton().setWidgets(
                                function=okBtn_function,
                                icon_model=False,
                                text_model=True,
                                text=okBtn_text,
                                cursor=CursorType.Link
                            ),
                            OptPushButton().setWidgets(
                                function=cancelBtn_function if cancelBtn_function is not None else self.close,
                                icon_model=False,
                                text_model=True,
                                text=cancel_text,
                                cursor=CursorType.Link
                            )
                        ],
                        aligns=[Qt.AlignCenter, Qt.AlignCenter]
                    )
                )  # WidgetOrLayoutDict
            ],
            **kwargs
        )
class LoadingDialog(QDialog, AbstractWidget):
    __slots__ = ('GifWidget', 'CancelBtn', 'CoreThread', 'signalFunction', 'terminateFunction')
    def __init__(self,
                 taskFunction : Callable = lambda : ...,
                 signalFunction : Callable = lambda : print("Loading Success!"),
                 terminateFunction : Callable = lambda : print("Cancel Loading!"),
                 parent: Optional[QWidget] = None,
                 *args
                 ):
        super().__init__(parent=parent)

        self.GifWidget = CircleProgressBar()
        self.CancelBtn = OptPushButton()
        self.CoreThread = OptThread(lambda : taskFunction(*args))
        self.signalFunction = signalFunction
        self.terminateFunction = terminateFunction
        self.setUI()

    def setUI(self):
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
        self.setLayout(OptVBox().setWidgets(
            widgets=[self.GifWidget, self.CancelBtn],
            aligns=[Qt.AlignCenter, Qt.AlignCenter]
        ))

    def setWidgets(self,
                   cancelText : str = '取消加载',
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.GifWidget.setWidgets(
            minh=200,
            minw=200
        )
        self.CancelBtn.setWidgets(
            text_model=True,
            icon_model=False,
            text=cancelText,
            function=self.__setCancelFunction,
            maxh=80,
            maxw=150,
            minw=100,
            qss='font-size : 18px;font-weight: 900;border : 3px solid tan;border-radius : 10px;',
            cursor=CursorType.Link
        )
        # 启动线程
        self.CoreThread.start()
        # 线程结束时
        self.CoreThread.signal.connect(
            lambda : (self.close(), self.signalFunction())[0]
        )
        return self

    def __setCancelFunction(self):
        if self.CoreThread.isRunning():
            self.terminateFunction()
            self.CoreThread.terminate()
        self.close()

    def setUnStopped(self):
        self.CancelBtn.setWidgets(
            enabled=False,
            text_model=True,
            icon_model=False,
            text='加载中...',
            cursor=CursorType.Unavailable,
            function=lambda : ...
        )
        return self

    @overload
    def exec_(self): ...
    @overload
    def exec_(self, pos : QPoint = None): ...
    def exec_(self, pos : Optional[QPoint] = None) -> int:
        if pos is not None: self.move(pos)
        return super().exec_()

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        icon=QIcon(ImageType.APP_LOGO),
        display_name='OperatorBar'
    )
    # ui0 = SearchBar()
    # ui0.setWidgets(modal=False)
    # ui0.show()
    # ui1 = StartBar()
    # ui1.setWidgets()
    # ui1.OpenEdit.setStyleSheet('border : 3px solid lightblue;border-radius : 4px')
    # ui1.show()
    # ui2 = ExcelToolBox()
    # ui2.setWidgets()
    # ui2.show()
    # ui3 = StatusBarWithSlider()
    # ui3.setWidgets(defautltSets=True)
    # ui3.setMinimumSize(QSize(800, 100))
    # ui3.show()
    # ui4 = ReWriteInputDialog()
    # ui4.setWidgets(
    #     title='ReWriteInputDialog',
    #     modal=False,
    #     maxh=100,
    #     minh=100,
    #     maxw=800,
    # )
    # ui4.show()
    # ui5 = ReWriteAnyWidgetDialog()
    # ui5.setWidgets(
    #     maxh=150,
    #     maxw=400,
    #     widget=AbstractWidget()
    # )
    # ui5.show()
    def __func():
        from time import sleep
        for i in range(50):
            sleep(.1)
            print(i)
    ui6 = LoadingDialog(
        lambda : __func()
    )
    ui6.setWidgets(
        maxh=550,
        maxw=500
    )
    ui6.show()
    app.exec()
