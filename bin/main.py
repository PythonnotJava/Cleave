import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt

from OptQt import *
from SideBar import SideBar
from Face import HomePageView, PluginKit, AnalysisCore, Setting, PluginArea
from Sources import *
from Util import *

class AppCore(AbstractWidget):

    CoreCfg = json_load(CFG_FILE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.SideBar = SideBar()
        self.StackManager = OptStack()
        self.PluginAreas = PluginArea()
        self.HomePage = HomePageView(self.CoreCfg['theme'])
        self.PluginKit = PluginKit(self.PluginAreas)
        self.AnalysisFigure = AnalysisCore()
        self.Settings = Setting(self.CoreCfg['alpha'])
        self.MidSplitter = OptSplitter()
        self.Vbox = QVBoxLayout()

        # State
        self.ShowToolButtons = True

        self.setUI()
        self.setWidgets()

    def setUI(self):
        self.setWindowTitle("Cleave")
        self.SideBar.button_Home.setEnabled(False)
        self.setWindowIcon(QIcon(ImageType.APP_LOGO))
        self.setWindowOpacity(self.CoreCfg['alpha'] / 100)
        self.baseCfg(
            x=200,
            y=100,
            objectName="AppCore",
            minh=self.CoreCfg['minHeight'],
            minw=self.CoreCfg['minWidth'],
            qss=QSSLoader(ThemeType.Dracula)
        )
        self.setLayout(self.Vbox)

    def setWidgets(self):
        self.HomePage.setWidgets(
            objectName='HomePage',
            cursor=CursorType.Busy,
        )

        self.AnalysisFigure.setWidgets(
            objectName='AnalysisFigure',
            cursor=CursorType.Busy,
            familys=self.CoreCfg['ExcelKernel']['familys'],
            sizes=self.CoreCfg['ExcelKernel']['sizes'],
        )

        self.PluginKit.setWidgets(
            objectName='PluginKit',
            cursor=CursorType.Busy,
        ).loadToPluginAreaConnect(
            lambda : self.setSideBar(5)
        )

        self.Settings.setWidgets(
            objectName='Settings',
            cursor=CursorType.Busy
        ).ThemeChanged(
            function_dracula=lambda : self.setTheme(0),
            function_skyblue=lambda : self.setTheme(1),
            function_cyan=lambda : self.setTheme(2),
            function_snow=lambda : self.setTheme(3)
        ).CheckedToggleButton(
            n=self.CoreCfg['theme']
        ).setAlphaSliderConnect(
            function=self.setAlpha
        )

        self.StackManager.setWidgets(
            widgets=[self.HomePage, self.PluginKit, self.AnalysisFigure, self.Settings, self.PluginAreas],
            currentIndex=0,
            objectName="StackManager",
            cursor=CursorType.Busy
        )

        self.SideBar.setWidgets(
            lambda: self.setSideBar(0),
            lambda: self.setSideBar(1),
            lambda: self.setSideBar(2),
            lambda: self.setSideBar(3),
            lambda: self.setSideBar(4),
            lambda: self.setSideBar(5),
            objectName='SideBar',
            cursor=CursorType.Busy
        )

        self.MidSplitter.setWidgets(
            widgets=[self.SideBar, self.StackManager],
            objectName='MidSplitter',
            sizes=[300, 700],
            cursor=CursorType.Move,
            handleIndex=1,
            handleTips="选中按住可拖动",
            horizontal=True,
            handleCursor=CursorType.Move
        )

        self.PluginAreas.setWidgets(
            objectName='PluginAreas',
            cursor=CursorType.Busy
        )

        self.Vbox.addWidget(self.MidSplitter, alignment=Qt.Alignment())

    def setSideBar(self, n : int):
        if n == 0:
            if self.SideBar.button_Hide.isEnabled():
                if self.ShowToolButtons:
                    self.MidSplitter.setSizes([self.MidSplitter.size().width(), 0])
                else:
                    self.MidSplitter.setSizes([0, self.MidSplitter.size().width()])
                self.ShowToolButtons = not self.ShowToolButtons
        if n in self.SideBar.ButtonMapping and self.SideBar.ButtonMapping[n].isEnabled():
            self.StackManager.setCurrentIndex(n - 1)

            for button in self.SideBar.ButtonMapping.values():
                button.setEnabled(True)

            self.SideBar.ButtonMapping[n].setEnabled(False)
            self.SideBar.button_Hide.setEnabled(True)

    def setTheme(self, n : int):
        self.CoreCfg['theme'] = n
        if n == 0:
            self.HomePage.RefreshHtml(PageType.Dracula)
            self.setStyleSheet(QSSLoader(ThemeType.Dracula))
            self.SideBar.TrickLabel.setPixmap(QPixmap(ImageType.Dracula))
            self.SideBar.TrickLabel.setDragEvent(True)
        elif n == 1:
            self.HomePage.RefreshHtml(PageType.Skyblue)
            self.setStyleSheet(QSSLoader(ThemeType.Skyblue))
            self.SideBar.TrickLabel.setPixmap(QPixmap())
            self.SideBar.TrickLabel.setDragEvent(False)
        elif n == 2:
            self.HomePage.RefreshHtml(PageType.Cyan)
            self.setStyleSheet(QSSLoader(ThemeType.Cyan))
            self.SideBar.TrickLabel.setPixmap(QPixmap())
            self.SideBar.TrickLabel.setDragEvent(False)
        elif n == 3:
            self.HomePage.RefreshHtml(PageType.Snow)
            self.setStyleSheet(QSSLoader(ThemeType.Snow))
            self.SideBar.TrickLabel.setPixmap(QPixmap())
            self.SideBar.TrickLabel.setDragEvent(False)
        else : pass

    def setAlpha(self):
        self.setWindowOpacity(self.Settings.AlphaSlider.value() / 100),
        self.CoreCfg['alpha'] = self.Settings.AlphaSlider.value()

    def closeEvent(self, event : QCloseEvent):
        json_dump(self.CoreCfg, CFG_FILE)
        super().closeEvent(event)
        print("Close Successfully!")

    def keyPressEvent(self, e: QKeyEvent, *args):
        if QApplication.keyboardModifiers() == Qt.ControlModifier and e.key() == Qt.Key_Q:
            self.Settings.alphaDown(self.setAlpha)
        elif QApplication.keyboardModifiers() == Qt.ControlModifier and e.key() == Qt.Key_S:
            self.Settings.alphaUp(self.setAlpha)
        else:
            pass

    # def paintEvent(self, e : QPaintEvent, *args):
    #     painter = QPainter(self)
    #     pixmap = QPixmap(ImageType.DefaultBackground)
    #     painter.drawPixmap(
    #         0,
    #         0,
    #         pixmap.scaled(self.width(), self.height(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    #     )

if __name__ == "__main__":
    app = OptAppication(sys.argv)
    app.setWidgets(
        display_name="Version1.1",
        icon=QIcon(ImageType.APP_LOGO)
    )
    ui = AppCore()

    ui.show()
    sys.exit(app.exec())
