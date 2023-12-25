from typing import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from OptQt import *
from Util import PluginsLoader, has_parameter
from Sources import PLUGINS_FILE, ImageType
from Face.PluginArea import PluginArea


class PluginKit(QScrollArea, AbstractWidget):
    loadToPluginArea = pyqtSignal()

    def loadToPluginAreaConnect(self, func: Callable) -> "PluginKit":
        self.loadToPluginArea.connect(func)
        return self

    def LinkedFunc(self, func: Callable) -> Callable:
        if has_parameter(func, 'widget'):
            if self.__TargetArea is not None:
                __keyword: dict = func(widget=True)
                return lambda: (
                    self.__TargetArea.setNewPluginLoad(
                        enabled=True,
                        icon=__keyword.get('icon', None),
                        text=__keyword.get('text', None),
                        widget=__keyword.get('widget', None),
                        tips=__keyword.get('tips', None)
                    ),
                    self.loadToPluginArea.emit()
                )[0]
            else:
                return lambda: print("No TargetArea!!!")
        else:
            return func

    def __init__(self, targetArea: Optional[PluginArea] = None):
        super().__init__()

        self.__TargetArea = targetArea

        self.CoreWidget = AbstractWidget()
        CoreData = PluginsLoader(PLUGINS_FILE)
        CoreData.analysis()

        self.Widgets = [
            OptToolCompose().setWidgets(
                title=CoreData.keys[x],
                version=CoreData.versions[x],
                author=CoreData.infos[x],
                des=CoreData.deses[x],
                buttonIcon=CoreData.icons[x],
                shortcuts=CoreData.shortcuts[x],
                collapsible=True,
                function=self.LinkedFunc(
                    CoreData.linkMainFunction(CoreData.links[x])
                ),
            ) for x in range(len(CoreData.keys))
        ]

        self.setUI()

    def setUI(self):
        self.CoreWidget.setStyleSheet(
            '''
            background-color : #bdeeaf;
            font-size : 18px;
            color : #000000;
            font-family : 微软雅黑;
            font-weight : bold;
            '''
        )
        for widget in self.Widgets:
            widget.Button.setStyleSheet(
                '''
                OptPushButton{
                    border-left,  border-top, border-bottom,: 25px solid darkblue ;
                    border-radius : 15px;
                }
                OptPushButton:hover{
                    border-left,  border-top, border-bottom,: 25px solid darkblue ;
                    border-radius : 15px;
                }
                OptPushButton:pressed{
                    border-left,  border-top, border-bottom,: 25px solid darkblue ;
                    padding-left: 5px;
                    padding-top: 5px;
                    border-radius : 15px;
                }
                '''
            )
            widget.setStyleSheet(
                '''
                border-radius : 30px;
                '''
            )
            widget.HorSplitter.setStyleSheet(
                '''
                QSplitter:handle{
                    background-color : #ecefce;     
                    width : 5px;
                }
                '''
            )
            widget.VerSplitter.setStyleSheet(
                '''
                QSplitter:handle{
                    background-color : #ecefce;     
                    width : 5px;
                }
                '''
            )

    def setScrollBar(self,
                     cursor: Optional[str] = None,
                     objectName: Optional[str] = None,
                     qss: Optional[str] = None,
                     horizontal: bool = True
                     ) -> "PluginKit":
        if horizontal:
            hor: QScrollBar = self.horizontalScrollBar()
            if objectName is not None: hor.setObjectName(objectName)
            if cursor is not None: hor.setCursor(QCursor(QPixmap(cursor)))
            if qss is not None: hor.setStyleSheet(qss)
        else:
            ver: QScrollBar = self.verticalScrollBar()
            if objectName is not None: ver.setObjectName(objectName)
            if cursor is not None: ver.setCursor(QCursor(QPixmap(cursor)))
            if qss is not None: ver.setStyleSheet(qss)
        return self

    def setWidgets(self,
                   **kwargs
                   ) -> 'PluginKit':
        self.setWidgetResizable(True)
        self.baseCfg(**kwargs)
        self.setWidget(self.CoreWidget)
        self.CoreWidget.baseCfg(
            mainlay=OptVBox().setWidgets(widgets=self.Widgets).setCommonAlign(Qt.Alignment()),
            objectName='PluginKitCoreWidget'
        )
        return self

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='PluginKit',
        icon=QIcon(ImageType.APP_LOGO)
    )
    ui = PluginKit()
    ui.setWidgets()
    ui.show()
    app.exec()
