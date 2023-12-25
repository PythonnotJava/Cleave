from OptQt.OptimizeQt import *
# 测试布局构造函数
class Appppppppp(AbstractWidget):
    def __init__(self):
        super().__init__()

        self.setUI()

    def setUI(self):
        self.setMinimumSize(400, 600)

    def setWidgets(self):
        self.layoutFactoryConstructor(
            hbox=False,
            widgets_lays=[
                WidgetOrLayoutDict(
                    align=None,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptLabel().setWidgets(
                                text='打开',
                            ),
                            OptLineEdit().setWidgets(
                                text='选择文件链接'
                            )
                        ],
                        aligns=[
                            Qt.AlignCenter, Qt.AlignCenter
                        ]
                    ),
                    dtype=0
                ),
                WidgetOrLayoutDict(
                    align=Qt.AlignCenter,
                    dtype=1,
                    obj=OptLabel().setWidgets(
                        qss='background : red',
                        minw=300
                    )
                ),
                WidgetOrLayoutDict(
                    align=None,
                    dtype=0,
                    obj=OptHBox().setWidgets(
                        widgets=[
                            OptPushButton().setWidgets(
                                text='btn111',
                                icon_model=False,
                                text_model=True
                            ),
                            OptPushButton().setWidgets(
                                text='btn112',
                                icon_model=False,
                                text_model=True
                            ),
                            OptPushButton().setWidgets(
                                text='btn113',
                                icon_model=False,
                                text_model=True
                            ),
                        ],
                        aligns=[
                            Qt.AlignCenter, Qt.AlignCenter, Qt.AlignCenter
                        ]
                    )
                )
            ]
        )

if __name__ == '__main__':
    app = OptAppication([])
    ui = Appppppppp()
    ui.setWidgets()
    ui.show()
    app.exec()