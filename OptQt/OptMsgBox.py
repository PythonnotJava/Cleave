# 组合类控件的实现
from typing import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from Sources import ImageType, CursorType
from OptQt.OptimizeQt import OptAppication, OptDlg, OptPushButton, OptLabel, OptVBox, OptHBox

# 单按钮动画弹窗
class SingleButtonMessageBox(OptDlg):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Msg = OptLabel()
        self.Button = OptPushButton()
        self.Vbox = OptVBox()

        self.setUI()

    def setUI(self):
        self.setLayout(self.Vbox)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.Dialog)

    @overload
    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   **kwargs
                   ):
        ...

    @overload
    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   isMsgBox: bool = True,
                   msg: Optional[str] = None,
                   button_function: Callable = lambda: ...,
                   button_text: str = '知道了',
                   visible: bool = True,
                   **kwargs
                   ):
        ...

    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   isMsgBox: bool = True,
                   msg: Optional[str] = None,
                   button_function: Callable = lambda: ...,
                   button_text: str = '知道了',
                   visible : bool = True,
                   **kwargs
                   ):
        if isMsgBox:
            self.setVisible(visible)
            self.Vbox.setWidgets(
                widgets=[self.Msg, self.Button],
                aligns=[Qt.AlignCenter, Qt.AlignCenter]
            )

            self.Msg.setWidgets(
                align=Qt.AlignTop,
                text_model=True,
                text=msg,
                objectName='Single-Msg',
                cursor=CursorType.Working,
                wrap=True,
                linkable=True,
                maxw=int(self.width() * .9),
                minw=int(.8 * self.width()),
                minh=int(.7 * self.height()),
            )

            self.Button.setWidgets(
                function=button_function,
                minw=int(.2 * self.width()),
                minh=int(.08 * self.height()),
                maxw=int(.3 * self.width()),
                maxh=int(.15 * self.height()),
                text_model=True,
                icon_model=False,
                objectName='Single-Button',
                cursor=CursorType.Link,
                text=button_text
            )

        return super().setWidgets(
            hideWhatThisButton=hideWhatThisButton,
            modal=modal,
            **kwargs
        )

# 双按钮动画弹窗
class DoubleButtonMessageBox(OptDlg):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.Msg = OptLabel()
        self.LeftButton = OptPushButton()
        self.RightButton = OptPushButton()
        self.Vbox = OptVBox()
        self.Hbox = OptHBox()

        self.setUI()

    def setUI(self):
        self.setLayout(self.Vbox)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint | Qt.Dialog)

    @overload
    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   **kwargs
                   ):
        ...

    @overload
    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   isMsgBox: bool = True,
                   msg: Optional[str] = None,
                   left_button_function: Callable = lambda: ...,
                   left_button_text: str = '知道了',
                   right_button_function: Callable = lambda: ...,
                   right_button_text: str = '知道了',
                   visible: bool = True,
                   **kwargs
                   ):
        ...

    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   isMsgBox: bool = True,
                   msg: Optional[str] = None,
                   left_button_function: Callable = lambda: ...,
                   left_button_text: str = '知道了',
                   right_button_function: Callable = lambda: ...,
                   right_button_text: str = '知道了',
                   visible: bool = True,
                   **kwargs
                   ):
        if isMsgBox:
            self.setVisible(visible)
            self.Vbox.addWidget(self.Msg, Qt.AlignCenter)
            self.Vbox.addLayout(self.Hbox)
            self.Hbox.setWidgets(
                widgets=[self.LeftButton, self.RightButton],
                aligns=[Qt.AlignCenter, Qt.AlignCenter]
            )

            self.Msg.setWidgets(
                align=Qt.AlignTop,
                text_model=True,
                text=msg,
                objectName='Double-Msg',
                cursor=CursorType.Working,
                wrap=True,
                linkable=True,
                maxw=int(self.width() * .9),
                minw=int(.8 * self.width()),
                minh=int(.7 * self.height()),
            )

            self.LeftButton.setWidgets(
                function=left_button_function,
                minw=int(.2 * self.width()),
                minh=int(.08 * self.height()),
                maxw=int(.3 * self.width()),
                maxh=int(.15 * self.height()),
                text_model=True,
                icon_model=False,
                objectName='Double-LButton',
                cursor=CursorType.Link,
                text=left_button_text
            )

            self.RightButton.setWidgets(
                function=right_button_function,
                minw=int(.2 * self.width()),
                minh=int(.08 * self.height()),
                maxw=int(.3 * self.width()),
                maxh=int(.15 * self.height()),
                text_model=True,
                icon_model=False,
                objectName='Double-RButton',
                cursor=CursorType.Link,
                text=right_button_text
            )

        return super().setWidgets(
            hideWhatThisButton=hideWhatThisButton,
            modal=modal,
            **kwargs
        )

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        icon=QIcon(ImageType.APP_LOGO),
        display_name='SingleButtonMessageBox'
    )
    ui = SingleButtonMessageBox()
    ui.setWidgets(
        objectName='ui',
        msg='''
            <h1 >代码</h1><br><br>
                self.Button.setWidgets(
                    function=button_function,
                    maxw=int(.2 * self.width()),
                    maxh=int(.15 * self.height()),
                    text_model=True,
                    icon_model=False,
                    objectName='Single-Button',
                    cursor=CursorType.Link,
                    text=button_text
                )
            ''',
        minw=600,
        minh=400,
        isMsgBox=True,
        button_text="Ok",
        qss='''
        #Single-Msg{
            border-radius : 15px;
            background : yellow;
        }
        #Single-Button{
             border-radius : 15px;
            background : red;
        }
        #ui {
            background : lightskyblue;
        }
        ''',
        button_function=ui.close
    )
    ui.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)

    ui.show()

    ui2 = DoubleButtonMessageBox()
    ui2.setWidgets(
        objectName='ui2',
        msg='''
            <h1 >代码</h1><br><br>
                self.Button.setWidgets(
                    function=button_function,
                    maxw=int(.2 * self.width()),
                    maxh=int(.15 * self.height()),
                    text_model=True,
                    icon_model=False,
                    objectName='Single-Button',
                    cursor=CursorType.Link,
                    text=button_text
                )
                self.Button.setWidgets(
                    function=button_function,
                    maxw=int(.2 * self.width()),
                    maxh=int(.15 * self.height()),
                    text_model=True,
                    icon_model=False,
                    objectName='Single-Button',
                    cursor=CursorType.Link,
                    text=button_text
                )
            ''',
        minw=600,
        minh=400,
        isMsgBox=True,
        left_button_text="Ok",
        right_button_text="Ok",
        qss='''
            #Double-Msg{
                border-radius : 15px;
                background : yellow;
            }
            #Double-LButton, #Double-RButton{
                 border-radius : 15px;
                background : red;
            }
            #ui2 {
                background : lightskyblue;
            }
            ''',
        left_button_function=ui2.close,
        right_button_function=ui2.close,
    )
    ui2.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
    ui2.show()
    app.exec()
