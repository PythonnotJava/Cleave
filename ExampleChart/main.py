from ChartSelf import Window
from OptQt.OptimizeQt import *
from qt_material import apply_stylesheet
from Sources import ImageType

class ExampleChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.StatusWidget = OptStatusBar()
        self.MenuWidget = OptMenuBar()
        self.MidSplitter = OptSplitter()
        self.LeftArea = OptLabel()
        self.RightArea = Window()

        self.setUI()

    def setUI(self):
        self.setStatusBar(self.StatusWidget)
        self.setMenuBar(self.MenuWidget)
        self.setCentralWidget(self.MidSplitter)
        self.setMinimumSize(1200, 800)

    def setWidgets(self,
                   ):
        self.MidSplitter.setWidgets(
            widgets=[
                self.LeftArea, self.RightArea
            ],
            horizontal=True,
            sizes=[300, 500],
            handleWidth=5
        )

        self.LeftArea.layoutFactoryConstructor(
            qss='background-color : rgb(240, 240, 240)',
            hbox=False,
            widgets_lays=[
                WidgetOrLayoutDict(
                    align=None,
                    dtype=0,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text_model=True,
                                text='标题'
                            ),
                            OptLineEdit().setWidgets(
                                text="Barchart Percent Example",
                                minw=150
                            )
                        ],
                        aligns=[Qt.AlignLeft, Qt.AlignCenter]
                    )
                ),  # WidgetOrLayoutDict
                WidgetOrLayoutDict(
                    align=None,
                    dtype=0,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text_model=True,
                                text='X轴'
                            ),
                            OptSlider().setWidgets(
                                minNumber=0,
                                maxNumber=100,
                                step=1,
                                defaultValue=50,
                                horizontal=True,
                                maxh=20
                            )
                        ],
                        aligns=[Qt.AlignLeft, Qt.AlignCenter]
                    )
                ),  # WidgetOrLayoutDict
                WidgetOrLayoutDict(
                    align=None,
                    dtype=0,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text_model=True,
                                text='Y轴'
                            ),
                            OptSlider().setWidgets(
                                minNumber=0,
                                maxNumber=100,
                                step=1,
                                defaultValue=70,
                                horizontal=True,
                                maxh=20
                            )
                        ],
                        aligns=[Qt.AlignLeft, Qt.AlignCenter]
                    )
                ),  # WidgetOrLayoutDict
                WidgetOrLayoutDict(
                    align=None,
                    dtype=0,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text_model=True,
                                text='Z轴'
                            ),
                            OptSlider().setWidgets(
                                minNumber=0,
                                maxNumber=100,
                                step=1,
                                defaultValue=30,
                                horizontal=True,
                                maxh=20
                            )
                        ],
                        aligns=[Qt.AlignLeft, Qt.AlignCenter]
                    )
                ),  # WidgetOrLayoutDict
                WidgetOrLayoutDict(
                    dtype=0,
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text_model=True,
                                text='调色板'
                            ),
                            OptPushButton().setWidgets(
                                text_model=False,
                                icon_model=False,
                                qss='background : red',
                                minw=150,
                            )
                        ],
                        aligns=[Qt.AlignLeft, Qt.AlignCenter]
                    )
                ),  # WidgetOrLayoutDict
                WidgetOrLayoutDict(
                    align=None,
                    dtype=0,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text_model=True,
                                text='数据项',
                            ),
                            OptPushButton().setWidgets(
                                text_model=True,
                                text='新添',
                                icon_model=False
                            ),
                            OptPushButton().setWidgets(
                                text_model=True,
                                text='筛查',
                                icon_model=False
                            ),
                            OptPushButton().setWidgets(
                                text_model=True,
                                text='定位',
                                icon_model=False
                            )
                        ],
                        aligns=[Qt.AlignLeft, Qt.AlignCenter, Qt.AlignCenter, Qt.AlignCenter]
                    )
                )
            ]
        )

        outputMunu = OptMenu().setWidgets(
            parent=self.MenuWidget,
            title="输出项",
        )

        inputMunu = OptMenu().setWidgets(
            parent=self.MenuWidget,
            title='输入项',
        )

        settingMenu = OptMenu().setWidgets(
            parent=self.MenuWidget,
            title='设置',
        )

        self.MenuWidget.setWidgets(
            widgets={
                outputMunu: 0,
                inputMunu: 0,
                settingMenu: 0
            }
        )

        self.StatusWidget.setWidgets()
        return self


if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='样例',
        icon=ImageType.APP_LOGO
    )
    ui = ExampleChart()
    ui.setWidgets()
    apply_stylesheet(ui, theme='light_purple_500.xml')
    ui.show()
    app.exec()
