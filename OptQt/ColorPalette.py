from typing import *
from os import system as os_system
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from OptQt.OptimizeQt import *
from Sources import ImageType, CursorType

class _ColorLabel(OptLabel):
    def __init__(self, initial : QColor):
        super().__init__()
        self.Color = initial
        self.setFrameShape(QFrame.Shape.NoFrame)

    def paintEvent(self, _):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(self.Color)
        painter.drawRoundedRect(self.rect(), 20, 20)

class ColorPaletter(QDialog, AbstractWidget):

    def event(self, e: QEvent):
        if e.type() == QEvent.Type.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            os_system('start https://www.robot-shadow.cn')
        return super().event(e)

    def setWidgets(self,
                   initial: QColor,
                   title: Optional[str] = '调色板',
                   icon: QIcon | str | None = None,
                   confirm_function : Callable = lambda : ...,
                   cancel_function : Optional[Callable] = None,
                   **kwargs
                   ) -> 'ColorPaletter':
        self.setModal(True)
        if title is not None:
            self.setWindowTitle(title)
        if icon is not None:
            self.setWindowIcon(icon) if isinstance(icon, QIcon) else self.setWindowIcon(QIcon(icon))

        return self.layoutFactoryConstructor(
            fixSize=(400, 600),
            qss='background-color : rgb(240, 240, 240);',
            hbox=False,
            widgets_lays=[
                WidgetOrLayoutDict(
                    dtype=1,
                    align=Qt.AlignTop,
                    obj=_ColorLabel(initial=initial).setWidgets(
                        minh=350,
                        minw=350,
                        objectName='ColorLabel'
                    )
                ),
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text='R Channel',
                                qss=
                                '''font-size : 18px;
                                color : red;
                                font-weight : 900;
                                '''
                            ),
                            OptSlider().setWidgets(
                                minNumber=0,
                                maxNumber=255,
                                defaultValue=initial.red(),
                                step=15,
                                function=lambda : self.ModifyChannel(0),
                                horizontal=True,
                                qss='''
                                QSlider::groove:horizontal {
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0, 0, 0), 
                                    stop:1 rgb(255, 0, 0));
                                    height: 10px;
                                    margin: 0px;
                                    border-radius : 5px;
                                }
                                QSlider::handle:horizontal {
                                    background-color: red;
                                    border: 1px solid #5c5c5c;
                                    width: 10px;
                                    margin: -5px 0;
                                    border-radius: 5px;
                                }
                                ''',
                                cursor=CursorType.Link,
                                objectName='R-Channel',
                            )
                        ]
                    ).setCommonAlign(Qt.AlignTop)
                ),
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text='G Channel',
                                qss=
                                '''font-size : 18px;
                                color : green;
                                font-weight : 900;
                                '''
                            ),
                            OptSlider().setWidgets(
                                minNumber=0,
                                maxNumber=255,
                                defaultValue=initial.green(),
                                step=15,
                                function=lambda: self.ModifyChannel(1),
                                horizontal=True,
                                qss='''
                                 QSlider::groove:horizontal {
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0, 0, 0), 
                                    stop:1 rgb(0, 255, 0));
                                    height: 10px;
                                    margin: 0px;
                                    border-radius : 5px;
                                }
                                QSlider::handle:horizontal {
                                    background-color: green;
                                    border: 1px solid #5c5c5c;
                                    width: 10px;
                                    margin: -5px 0;
                                    border-radius: 5px;
                                }
                                ''',
                                cursor=CursorType.Link,
                                objectName='G-Channel'
                            )
                        ]
                    ).setCommonAlign(Qt.AlignTop)
                ),
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text='B Channel',
                                qss=
                                '''font-size : 18px;
                                color : blue;
                                font-weight : 900;
                                '''
                            ),
                            OptSlider().setWidgets(
                                minNumber=0,
                                maxNumber=255,
                                defaultValue=initial.blue(),
                                step=15,
                                function=lambda: self.ModifyChannel(2),
                                horizontal=True,
                                qss='''
                                QSlider::groove:horizontal {
                                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgb(0, 0, 0), 
                                    stop:1 rgb(0, 0, 255));
                                    height: 10px;
                                    margin: 0px;
                                    border-radius : 5px;
                                }
                                QSlider::handle:horizontal {
                                    background-color: blue;
                                    border: 1px solid #5c5c5c;
                                    width: 10px;
                                    margin: -5px 0;
                                    border-radius: 5px;
                                }
                                ''',
                                cursor=CursorType.Link,
                                objectName='B-Channel'
                            )
                        ]
                    ).setCommonAlign(Qt.AlignTop)
                ),
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptPushButton().setWidgets(
                                text_model=True,
                                icon_model=False,
                                text='确定',
                                maxh=40,
                                maxw=150,
                                function=confirm_function,
                                cursor=CursorType.Link,
                                qss='''
                                QPushButton {
                                    background-color: #4CAF50; 
                                    color: white; 
                                    border: 2px solid #45a049; 
                                    border-radius: 5px; 
                                }        
                                QPushButton:hover {
                                    background-color: #45a049;
                                }                   
                                QPushButton:pressed {
                                    background-color: #128725;
                                    padding : 5px 0 0 5px;
                                }
                                '''
                            ),
                            OptPushButton().setWidgets(
                                text_model=True,
                                icon_model=False,
                                text='取消',
                                maxh=40,
                                maxw=150,
                                function=cancel_function if cancel_function is not None else self.close,
                                cursor=CursorType.Link,
                                qss='''
                                QPushButton {
                                    background-color: #4CAF50; 
                                    color: white; 
                                    border: 2px solid #45a049; 
                                    border-radius: 5px; 
                                }
                                QPushButton:hover {
                                    background-color: #45a049;
                                }
                                QPushButton:pressed {
                                    background-color: #128725;
                                    padding : 5px 0 0 5px;
                                }
                                '''
                            )
                        ]
                    )
                )
            ],
            **kwargs
        )

    def ModifyChannel(self, which: int = 0) -> None:
        label: _ColorLabel = self.findChild(_ColorLabel, name='ColorLabel')
        match which:
            case 0:
                slider: OptSlider = self.findChild(OptSlider, name='R-Channel')
                label.Color.setRed(slider.value())
            case 1:
                slider: OptSlider = self.findChild(OptSlider, name='G-Channel')
                label.Color.setGreen(slider.value())
            case 2:
                slider: OptSlider = self.findChild(OptSlider, name='B-Channel')
                label.Color.setBlue(slider.value())
        label.update()

    def name(self) -> str: return self.findChild(_ColorLabel, name='ColorLabel').Color.name()

    def rgb(self, channel_tuples : bool = True) -> Union[tuple, int]:
        color: QColor = self.findChild(_ColorLabel, name='ColorLabel').Color
        if channel_tuples:
            return color.red(), color.green(), color.blue()
        else:
            return color.rgb()

    @property
    def Color(self) -> QColor:
        label: _ColorLabel = self.findChild(_ColorLabel, name='ColorLabel')
        return label.Color

    @Color.setter
    def Color(self, color : QColor) -> None:
        label: _ColorLabel = self.findChild(_ColorLabel, name='ColorLabel')
        label.Color = color
        label.update()

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='ColorPalette',
        icon=ImageType.APP_LOGO
    )
    ui = ColorPaletter()
    ui.setWidgets(
        initial=QColor(150, 150, 150)
    )
    ui.show()
    app.exec()
