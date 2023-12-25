from typing import Optional
from PyQt5.QtWidgets import QWidget, QApplication, QSplashScreen, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QPixmap, QPainter
from OptQt import OptLabel, OptVBox, OptProgressBar
from Sources import CursorType, ImageType
from time import sleep


class SplashAnimation(QSplashScreen):
    def __init__(self):
        super().__init__()

        self.SplashLabel = OptLabel()
        self.SplashProgressBar = OptProgressBar()

        self.Vbox = OptVBox()
        self.setUI()

    def setUI(self):
        self.setLayout(self.Vbox)
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    def setWidgets(self,
                   width: Optional[int] = None,
                   height: Optional[int] = None,
                   objectName: Optional[str] = None,
                   qss: Optional[str] = None,
                   parent: Optional[QWidget] = None,
                   cursor: Optional[str] = None,
                   opacity: float = .9,
                   picture: Optional[str] = None,
                   labelSets: Optional[dict] = None
                   ) -> 'SplashAnimation':
        self.setWindowOpacity(opacity)
        if width is not None:
            self.setFixedWidth(width)

        if height is not None:
            self.setFixedHeight(height)

        if objectName is not None:
            self.setObjectName(objectName)

        if qss is not None:
            self.setStyleSheet(qss)

        if cursor is not None:
            self.setCursor(QCursor(QPixmap(cursor)))

        if parent is not None:
            self.setParent(parent)

        if picture is not None:
            self.setPixmap(QPixmap(picture).scaled(self.size()))

        self.Vbox.setWidgets(
            widgets=[
                self.SplashLabel.setWidgets(**labelSets if labelSets is not None else {}),
                self.SplashProgressBar.setWidgets(
                    value=0,
                    maxh=80,
                    minw=int(width * .9),
                    minNumber=0,
                    maxNumber=1000,
                    objectName='SplashProgressBar',
                    horizontal=True,
                    qss="""
                    QProgressBar{
                        border-radius : 10px;
                        text-align: center;
                        color: white;
                        background: rgb(48, 50, 51);
                    }
                    QProgressBar::chunk {
                        background: rgb(0, 160, 230);  border-radius : 10px;
                    } 
                    QProgressBar#progressBar {
                        border-radius : 10px;
                        text-align: center;
                        color: white;
                        background-color: transparent;
                        background-repeat: repeat-x;
                    }
                    QProgressBar#progressBar::chunk {
                        border-radius : 10px;
                        background-color: transparent;
                        background-repeat: repeat-x;
                    }
                    """
                )
            ],
            aligns=[Qt.AlignCenter, Qt.AlignCenter | Qt.AlignBottom]
        )

        return self

    def mousePressEvent(self, a0):
        ...

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)


def SplashAnimationStart(_app: QApplication,
                         width=600,
                         height=400,
                         cursor=CursorType.Busy,
                         opacity=1,
                         picture=ImageType.Splash,
                         seconds: int = 1,
                         labelSets: Optional[dict] = None
                         ):
    ui = SplashAnimation()
    desk: QDesktopWidget = _app.desktop()
    ui.setWidgets(
        width=width,
        height=height,
        cursor=cursor,
        opacity=opacity,
        picture=picture,
        labelSets=labelSets
    )
    ui.move(desk.width() // 2 - ui.width() // 2, desk.height() // 2 - ui.height() // 2)
    ui.show()
    for i in range(0, seconds * 10):
        _app.processEvents()
        _ = int(100 / seconds)
        ui.SplashProgressBar.setValue(ui.SplashProgressBar.value() + _)
        sleep(.1)

    ui.finish(None)


if __name__ == '__main__':
    app = QApplication([])
    SplashAnimationStart(app,
                         seconds=2,
                         labelSets=dict(
                             text='<h1>Cleave</h1>'
                                  '<br>'
                                  '<br>'
                                  '<h2>访问本站</h2>'
                                  '<a href="https://www.github.com/">'
                                  'https://www.github.com/</a>',
                             qss=
                             'font-size : 24px;'
                             'font-family : 楷书;'
                             'font-weight : 900;'
                             'color : gold;',
                             align=Qt.AlignCenter
                         )
                         )
    appCore = QWidget()
    appCore.show()
    app.exec()
