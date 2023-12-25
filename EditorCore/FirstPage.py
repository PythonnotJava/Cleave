from typing import Optional
from OptQt.OptimizeQt import *
from Util import *
from Sources import BACK_UP_EXCEL, ImageType, CursorType

class FirstPage(OptLabel):
    def __init__(self):
        super().__init__()

        self.setWidgets(
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
                    <a href="https://github.com/">https://github.com/</a> 
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
            align=Qt.AlignLeft,
            linkable=True,
            qss='background-color : rgb(240, 240, 240);',
            contentsMargins=(100, 0, 0, 0)
        )
if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='FirstPage',
        icon=ImageType.APP_LOGO
    )
    ui = FirstPage()
    ui.setWidgets()
    ui.setMinimumSize(QSize(800, 600))
    ui.show()
    app.exec()