# 用于测试调试的UI
from os import system as os_system
from qutepart import Qutepart

from OptQt.OptimizeQt import *
from Sources import ImageType

class CoderColaWidget(Qutepart, AbstractWidget):
    def setWidgets(self,
                   language_support: str = 'Python',
                   **kwargs
                   ) -> 'CoderColaWidget':
        self.baseCfg(**kwargs)
        self.detectSyntax(language=language_support)
        return self
class UTUI(AbstractWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.Dialog)

    def event(self, e: QEvent, *args):
        if e.type() == QEvent.Type.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            os_system('start https://www.robot-shadow.cn')
        return super().event(e)

    def setWidgets(self, **kwargs) -> 'UTUI':
        return self.layoutFactoryConstructor(
            hbox=True,
            widgets_lays=[
                WidgetOrLayoutDict(
                    align=Qt.Alignment(),
                    dtype=1,
                    obj=OptTabWidget().setWidgets(
                        tabSets=[
                            TabWidgetDict(
                                enabled=True,
                                tips='开发调试',
                                text='开发调试',
                                icon=None,
                                widget=AbstractWidget().layoutFactoryConstructor(
                                    hbox=False,
                                    widgets_lays=[
                                        WidgetOrLayoutDict(
                                            align=None,
                                            dtype=0,
                                            obj=OptHBox().setWidgets(
                                                widgets=[
                                                    OptLabel().setWidgets(
                                                        text_model=True,
                                                        text='测试1'
                                                    ),
                                                    OptPushButton().setWidgets(
                                                        icon_model=False,
                                                        text_model=True,
                                                        text='Click!',
                                                        function=lambda: ...,
                                                    )
                                                ],
                                                aligns=[Qt.Alignment(), Qt.Alignment()]
                                            )
                                        ),  # WidgetOrLayoutDict
                                        WidgetOrLayoutDict(
                                            align=None,
                                            dtype=0,
                                            obj=OptHBox().setWidgets(
                                                widgets=[
                                                    OptLabel().setWidgets(
                                                        text_model=True,
                                                        text='测试2'
                                                    ),
                                                    OptLineEdit().setWidgets(
                                                        enable=True,
                                                        text='XXXXXXXXXX'
                                                    )
                                                ],
                                                aligns=[Qt.Alignment(), Qt.Alignment()]
                                            )
                                        )  # WidgetOrLayoutDict
                                    ]
                                )
                            ),  # TabWidgetDict
                            TabWidgetDict(
                                enabled=True,
                                tips='内置模拟器',
                                text='内置模拟器',
                                icon=None,
                                widget=AbstractWidget().layoutFactoryConstructor(
                                    hbox=False,
                                    widgets_lays=[
                                        WidgetOrLayoutDict(
                                            align=None,
                                            dtype=0,
                                            obj=OptHBox().setWidgets(
                                                widgets=[
                                                    OptPushButton().setWidgets(
                                                        text_model=True,
                                                        icon_model=False,
                                                        text='文件',
                                                        maxw=100,
                                                        maxh=50
                                                    ),
                                                    OptComBox().setWidgets(
                                                        items=['语言模式 Python', "语言模式 C", "语言模式 CML"],
                                                        maxh=50,
                                                        maxw=200,
                                                        currentIndex=0,
                                                        objectName='LangModelsComboBox'
                                                    ),

                                                ],
                                            ).setCommonAlign(Qt.AlignLeft)
                                        ),
                                        WidgetOrLayoutDict(
                                            align=Qt.Alignment() & Qt.AlignCenter,
                                            dtype=1,
                                            obj=CoderColaWidget().setWidgets(
                                                language_support='Python',
                                                objectName='CoderColaWidget',
                                                font=OptFont().setAttributes(
                                                    size=8,
                                                    weight=600
                                                )
                                            ),
                                        ),
                                        WidgetOrLayoutDict(
                                            align=None,
                                            dtype=0,
                                            obj=OptHBox().setWidgets(
                                                widgets=[
                                                    OptPushButton().setWidgets(
                                                        text_model=True,
                                                        icon_model=False,
                                                        text='运行(&F5)',
                                                        function=self.runCode,
                                                        minh=25,
                                                    ),
                                                    OptPushButton().setWidgets(
                                                        text_model=True,
                                                        icon_model=False,
                                                        text='清空',
                                                        function=self.clearText,
                                                        minh=25
                                                    )
                                                ]
                                            )
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ),  # WidgetOrLayoutDict
            ],
            **kwargs
        )

    @pyqtSlot()
    def runCode(self) -> Any:
        widget: CoderColaWidget = self.findChild(CoderColaWidget, name='CoderColaWidget')
        try:
            # 这到时候要设计一个可以与ExcelKernel交互的接口函数检测
            exec(widget.toPlainText(), {})
        except Exception as e:
            print(str(e))

    def clearText(self) -> None:
        widget : CoderColaWidget = self.findChild(CoderColaWidget, name='CoderColaWidget')
        widget.text = ''

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='UTUI',
        icon=ImageType.APP_LOGO
    )
    ui = UTUI()
    ui.setWidgets(minw=600, minh=600)
    ui.show()
    app.exec()
