from main import AppCore, QApplication, Qt
from Face import SplashAnimationStart
from random import choice

if __name__ == '__main__':
    random_text = [
        '<h1>Hello, Cleave</h1><br><br><h2>访问本站</h2><a style="color : gold" href="https://www.github.com/">https://www.github.com/</a>',
        '<h1>命令行模式</h1><br><br style="color : gold;font-size: 16px;"><p>查看手册帮助A</p><p>可以快速帮你了解和使用命令行工具!</p>'
    ]

    app = QApplication([])
    SplashAnimationStart(
        _app=app,
        width=600,
        height=400,
        opacity=.75,
        seconds=1,
        labelSets=dict(
            text=choice(random_text),
            qss='''
                font-size : 24px;
                font-family : 楷书;
                font-weight : 900;
                color : gold;
                ''',
            align=Qt.AlignCenter
        )
    )
    ui = AppCore()
    ui.show()
    app.exec()
