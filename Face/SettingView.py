from typing import Callable, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from OptQt import *
from Sources import *

class Setting(AbstractWidget):

    def __init__(self, alpha: int = 80):
        super().__init__()

        self.alpha = alpha

        self.Vbox = OptVBox()

        self.ThemeComBox = OptComBox()
        self.ThemeLabel = OptLabel()
        self.ThemeHbox = OptHBox()

        self.DraculaToggle = OptToggleButton()
        self.SkyblueToggle = OptToggleButton()
        self.CyanToggle = OptToggleButton()
        self.SnowToggle = OptToggleButton()

        self.DraculaLabel = OptLabel()
        self.SkyblueLabel = OptLabel()
        self.CyanLabel = OptLabel()
        self.SnowLabel = OptLabel()

        self.FontLabel = OptLabel()
        self.FontComBox = OptComBox()
        self.FontHbox = OptHBox()

        self.AlphaLabel = OptLabel()
        self.AlphaSlider = OptSlider()
        self.AlphaHbox = OptHBox()

        self.setUI()

    def setUI(self):
        self.setFont(
            OptFont().setAttributes(
                bold=True,
                weight=900,
                family='黑体'
            )
        )

    def setWidgets(self,
                   FontComBox_function: Optional[Callable] = None,
                   AlphaSlider_function: Optional[Callable] = None,
                   **kwargs):
        self.Vbox.setLays(
            lays=[self.ThemeHbox, self.FontHbox, self.AlphaHbox]
        )

        self.ThemeHbox.setWidgets(
            widgets=[
                self.ThemeLabel.setWidgets(
                    text="主题设置",
                    objectName='ThemeLabel'
                ),
                # theme-togglebuttons
                self.DraculaToggle.setWidgets(
                    objectName='DraculaToggle',
                    cursor=CursorType.Link
                ),
                self.DraculaLabel.setWidgets(
                    objectName='DraculaLabel',
                    text='暗夜酷黑'
                ),
                self.SkyblueToggle.setWidgets(
                    objectName='SkyblueToggle',
                    cursor=CursorType.Link
                ),
                self.SkyblueLabel.setWidgets(
                    objectName='SkyblueLabel',
                    text='清澈天空'
                ),
                self.CyanToggle.setWidgets(
                    objectName='CyanToggle',
                    cursor=CursorType.Link
                ),
                self.CyanLabel.setWidgets(
                    objectName='CyanLabel',
                    text='清新草原'
                ),
                self.SnowToggle.setWidgets(
                    objectName='SnowToggle',
                    cursor=CursorType.Link
                ),
                self.SnowLabel.setWidgets(
                    objectName='SnowLabel',
                    text='浪漫晴雪'
                )
            ],
            aligns=[
                Qt.AlignLeft, Qt.AlignRight, Qt.AlignRight,
                Qt.AlignRight, Qt.AlignRight, Qt.AlignRight,
                Qt.AlignRight, Qt.AlignRight, Qt.AlignRight
            ]
        )

        self.FontHbox.setWidgets(
            widgets=[
                self.FontLabel.setWidgets(
                    text="字体设置",
                    objectName='FontLabel',
                ),
                self.FontComBox.setWidgets(
                    items=['微软雅黑', '黑体', '华文行楷', '宋体', '隶书'],
                    objectName='FontComBox',
                    cursor=CursorType.Link,
                    function=FontComBox_function
                )
            ],
            aligns=[Qt.AlignLeft, Qt.AlignRight]
        )

        self.AlphaHbox.setWidgets(
            widgets=[
                self.AlphaLabel.setWidgets(
                    text="透明度",
                    objectName='AlphaLabel',
                ),
                self.AlphaSlider.setWidgets(
                    minNumber=20,
                    maxNumber=100,
                    defaultValue=self.alpha,
                    step=5,
                    minw=600,
                    horizontal=True,
                    objectName='AlphaSlider',
                    cursor=CursorType.Link,
                    function=AlphaSlider_function,
                )
            ],
            aligns=[Qt.AlignLeft, Qt.AlignRight]
        )

        self.setLayout(self.Vbox)
        super().baseCfg(**kwargs)
        self.update()
        return self

    def ThemeChanged(self,
                     function_dracula: Callable = lambda: ...,
                     function_skyblue: Callable = lambda: ...,
                     function_cyan: Callable = lambda: ...,
                     function_snow: Callable = lambda: ...
                     ) -> 'Setting':
        self.CyanToggle.toggled.connect(function_cyan)
        self.DraculaToggle.toggled.connect(function_dracula)
        self.SkyblueToggle.toggled.connect(function_skyblue)
        self.SnowToggle.toggled.connect(function_snow)
        return self

    def CheckedToggleButton(self, n: int) -> 'Setting':
        if n == 0:
            self.DraculaToggle.setChecked(True)
        elif n == 1:
            self.SkyblueToggle.setChecked(True)
        elif n == 2:
            self.CyanToggle.setChecked(True)
        elif n == 3:
            self.SnowToggle.setChecked(True)
        else:
            pass
        return self

    def setAlphaSliderConnect(self,
                              function: Callable = lambda: ...
                              ) -> 'Setting':
        self.AlphaSlider.valueChanged.connect(function)
        return self

    def alphaDown(self, function):
        self.AlphaSlider.setValue(self.AlphaSlider.value() - 5)
        self.AlphaSlider.valueChanged.connect(function)

    def alphaUp(self, function):
        self.AlphaSlider.setValue(self.AlphaSlider.value() + 5)
        self.AlphaSlider.valueChanged.connect(function)


if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='Setting',
        icon=QIcon(ImageType.APP_LOGO)
    )
    ui = Setting()
    ui.setWidgets()
    ui.show()
    app.exec()
