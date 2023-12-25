from os import PathLike
from typing import *
from time import sleep

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import Qt
from QTyping import WidgetOrLayoutDict, TabWidgetDict

# 性能类
class OptThread(QThread):
    signal = pyqtSignal()

    def __init__(self, func: Callable):
        super().__init__()
        self.func = func

    def run(self):
        self.func()
        self.signal.emit()

# 效果类
class ShadowEffects(QGraphicsDropShadowEffect):
    def __init__(self,
                 parent: QWidget,
                 offset: tuple = (0., 0.),
                 radius: float = 10.,
                 color=Qt.gray,
                 object_name: Optional[str] = None,
                 ):
        super().__init__()
        self.setParent(parent)
        self.setOffset(*offset)
        self.setBlurRadius(radius)

        self.setColor(color)

        if object_name is not None:
            self.setObjectName(object_name)

class OpacityEffects(QGraphicsOpacityEffect):
    def __init__(self,
                 opacity: float = 1.,
                 object_name: Optional[str] = None):
        super().__init__()
        self.setOpacity(opacity)

        if object_name is not None:
            self.setObjectName(object_name)

class OptFont(QFont):
    def setAttributes(self,
                      size: Optional[int] = None,
                      family: Optional[str] = "微软雅黑",
                      bold: bool = True,
                      weight: Optional[int] = None
                      ):
        self.setBold(bold)

        if family is not None:
            self.setFamily(family)

        if size is not None:
            self.setPointSize(size)

        if weight is not None:
            self.setWeight(weight)
        return self

class MusicPlayer:
    @staticmethod
    def play(filePath: str,
             volume: int = 50,
             lasting: float = 2,
             ) -> None:
        player = QMediaPlayer()
        player.setMedia(
            QMediaContent(
                QUrl.fromLocalFile(
                    filePath
                )
            )
        )
        player.setVolume(volume)
        player.play()
        sleep(lasting)
        player.deleteLater()


# 统一型布局
class OptVBox(QVBoxLayout):
    def setWidgets(self,
                   widgets: Optional[list] = None,
                   aligns: Optional[list] = None,
                   stretch: int = 10
                   ):
        if widgets is not None and aligns is not None:
            for i in range(len(widgets)): self.addWidget(widgets[i], alignment=aligns[i], stretch=stretch)
        elif widgets is not None and aligns is None:
            for i in range(len(widgets)): self.addWidget(widgets[i], alignment=Qt.Alignment(), stretch=stretch)
        else:
            pass
        return self

    def setLays(self,
                lays: Optional[list] = None
                ):
        if lays is not None:
            for lay in lays: self.addLayout(lay)
        return self

    def setCommonAlign(self, align : Qt.Alignment = Qt.AlignCenter):
        self.setAlignment(align)
        return self

class OptHBox(QHBoxLayout):
    def setWidgets(self,
                   widgets: Optional[list] = None,
                   aligns: Optional[list] = None,
                   stretch: int = 10
                   ):
        if widgets is not None and aligns is not None:
            for i in range(len(widgets)): self.addWidget(widgets[i], alignment=aligns[i], stretch=stretch)
        elif widgets is not None and aligns is None:
            for i in range(len(widgets)): self.addWidget(widgets[i], alignment=Qt.Alignment(), stretch=stretch)
        else:
            pass
        return self

    def setLays(self,
                lays: Optional[list] = None
                ):
        if lays is not None:
            for lay in lays: self.addLayout(lay)
        return self

    def setCommonAlign(self, align : Qt.Alignment = Qt.AlignCenter):
        self.setAlignment(align)
        return self

# 抽象基类
class AbstractWidget(QWidget):

    def factoryConstructor(self,
                           **kwargs
                           ) -> 'AbstractWidget':
        self.baseCfg(**kwargs)
        return self

    def baseCfg(self,
                *,
                parent: Optional[QWidget] = None,
                rect: Optional[list] = None,
                flags: Optional[Any] = None,
                x: Optional[int] = None,
                y: Optional[int] = None,
                w: Optional[int] = None,
                h: Optional[int] = None,
                minw: Optional[int] = None,
                minh: Optional[int] = None,
                maxw: Optional[int] = None,
                maxh: Optional[int] = None,
                fixSize: Optional[Iterable] = None,
                resize: Optional[Iterable] = None,
                objectName: Optional[str] = None,
                qss: Optional[str] = None,
                shadow: Optional[ShadowEffects] = None,
                cursor: Optional[str] = None,
                font: Union[QFont, OptFont] = None,
                tips: Optional[str] = None,
                contentsMargins: tuple | QMargins = None,
                mainlay: Optional[QLayout] = None,
                propertyName: Optional[str] = None,
                propertyValue: Any = None,
                sizePolicy: QSizePolicy | list[QSizePolicy.Policy] | None = None,
                focusPolicy: Optional[Qt.FocusPolicy] = None,
                palette : Optional[QPalette] = None,
                ) -> None:
        if parent is not None:
            self.setParent(parent)

        if rect is not None:
            self.setGeometry(QRect(*rect))

        if flags is not None:
            self.setWindowFlags(flags)

        if x is not None and y is not None:
            self.move(x, y)
        elif w is not None and h is not None:
            self.setBaseSize(w, h)
        else:
            pass

        if fixSize is not None:
            self.setFixedSize(*fixSize)

        if maxh is not None:
            self.setMaximumHeight(maxh)

        if maxw is not None:
            self.setMaximumWidth(maxw)

        if minw is not None:
            self.setMinimumWidth(minw)

        if minh is not None:
            self.setMinimumHeight(minh)

        if resize is not None:
            self.resize(*resize)

        if objectName is not None:
            self.setObjectName(objectName)

        if qss is not None:
            self.setStyleSheet(qss)

        if shadow is not None:
            self.setGraphicsEffect(shadow)

        if cursor is not None:
            self.setCursor(QCursor(QPixmap(cursor)))

        if tips is not None:
            self.setToolTip(tips)

        if font is not None:
            self.setFont(font)

        if contentsMargins is not None:
            if isinstance(contentsMargins, tuple):
                self.setContentsMargins(*contentsMargins)
            elif isinstance(contentsMargins, QMargins):
                self.setContentsMargins(contentsMargins)
            else:
                pass

        if mainlay is not None:
            self.setLayout(mainlay)

        if propertyName is not None and propertyValue is not None:
            self.setProperty(propertyName, propertyValue)

        if sizePolicy is not None:
            if isinstance(sizePolicy, QSizePolicy):
                self.setSizePolicy(sizePolicy)
            else:
                self.setSizePolicy(QSizePolicy(*sizePolicy))

        if focusPolicy is not None:
            self.setFocusPolicy(focusPolicy)

        if palette is not None:
            self.setPalette(palette)

    # 获取本身中心点的坐标，相对于自身
    def getSelfCenterPos(self) -> QPoint:
        return QPoint(self.width() // 2, self.height() // 2)

    # 获取本身中心点的坐标，相对于桌面
    def getGlobalCenterPos(self) -> QPoint:
        return self.pos() + self.getSelfCenterPos()

    # 一个子控件在本身中心展示应该从哪个起点开始
    @overload
    def whereBegin(self, widget: QWidget) -> QPoint:
        ...

    @overload
    def whereBegin(self, size: QSize) -> QPoint:
        ...

    def whereBegin(self, param: Union[QWidget, QSize]) -> QPoint:
        if isinstance(param, QWidget):
            return self.getSelfCenterPos() - QPoint(param.width() // 2, param.height() // 2)
        elif isinstance(param, QSize):
            return self.getSelfCenterPos() - QPoint(param.width() // 2, param.height() // 2)
        else:
            pass

    # 选择核心布局方式之后，然后往布局里面放置控件或者子布局，暂时只支持上面两种布局
    def layoutFactoryConstructor(self,
                                 hbox: bool = True,
                                 widgets_lays: List[WidgetOrLayoutDict] = None,
                                 **kwargs
                                 ):

        self.baseCfg(**kwargs)
        if hbox:
            Box = QHBoxLayout()
        else:
            Box = QVBoxLayout()
        for wl in widgets_lays:
            if wl['dtype'] == 0:  # 0表示布局、1表示控件
                Box.addLayout(wl['obj'])
            elif wl['dtype'] == 1:
                Box.addWidget(wl['obj'], alignment=wl['align'] if wl['align'] is not None else Qt.Alignment())
            else:
                pass
        self.setLayout(Box)
        return self

class OptDlg(QDialog, AbstractWidget):
    def setWidgets(self,
                   hideWhatThisButton: bool = True,
                   modal: bool = True,
                   **kwargs
                   ):
        self.setModal(modal)
        self.baseCfg(**kwargs)
        if hideWhatThisButton:
            self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        return self


# 核心控件
class OptLabel(QLabel, AbstractWidget):
    def setWidgets(self,
                   text: Optional[str] = None,
                   text_model: bool = True,
                   img: Optional[str] = None,
                   img_model: bool = False,
                   wrap: bool = True,
                   linkable: bool = True,
                   align: Optional[Qt.Alignment] = None,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setOpenExternalLinks(linkable)

        if text_model:
            self.setWordWrap(wrap)
            if text is not None:
                self.setText(text)
        elif img_model:
            if img is not None:
                self.setPixmap(QPixmap(img))
            else:
                self.setPixmap(QPixmap())
        else:
            pass

        if align is not None:
            self.setAlignment(align)

        return self

    def addMovie(self,
                 movie: QMovie
                 ):
        self.setMovie(movie)
        movie.start()
        return self

class OptPushButton(QPushButton, AbstractWidget):
    def setWidgets(self,
                   function: Callable = lambda: ...,
                   icon: Optional[Union[QIcon, str]] = None,
                   icon_model: bool = True,
                   icon_fixed: bool = True,
                   icon_size: [int, int] = None,
                   text: Optional[str] = None,
                   text_model: bool = False,
                   shortcuts: Optional[str] = None,
                   enabled: bool = True,
                   **kwargs
                   ):
        self.clicked: pyqtBoundSignal
        self.clicked.connect(function)
        self.setEnabled(enabled)
        self.baseCfg(**kwargs)
        self.setAutoRepeat(False)

        if icon_model:
            if isinstance(icon, QIcon):
                self.setIcon(icon)
            elif isinstance(icon, str):
                self.setIcon(QIcon(icon))
            else:
                self.setIcon(QIcon())
            if icon_fixed:
                self.setIconSize(self.size())
            elif icon_size is not None:
                self.setIconSize(QSize(*icon_size))
            else:
                pass

        elif text_model:
            self.setText(text)
        else:
            pass

        if shortcuts is not None:
            self.setShortcut(shortcuts)

        return self


class OptToolButton(QToolButton, AbstractWidget):
    def setWidgets(self,
                   function: Callable = lambda: ...,
                   icon: QIcon | str = None,
                   icon_fixed: bool = True,
                   icon_size: Optional[list] = None,
                   text: Optional[str] = None,
                   buttonStyle: Qt.ToolButtonStyle = Qt.ToolButtonTextBesideIcon,
                   shortcuts: Optional[str] = None,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.clicked: pyqtBoundSignal
        self.clicked.connect(function)
        self.setText(text)
        self.setToolButtonStyle(buttonStyle)
        self.setAutoRepeat(False)

        if icon is not None:
            if isinstance(icon, QIcon):
                self.setIcon(icon)
            else:
                self.setIcon(QIcon(icon))
            if icon_fixed:
                self.setIconSize(self.size())
            elif icon_size is not None:
                self.setIconSize(QSize(*icon_size))
            else:
                self.setIconSize(QSize(int(self.width() * .75), int(self.height() * .75)))

        if shortcuts is not None:
            self.setShortcut(shortcuts)

        return self

    def TextIcon(self,
                 function=lambda: ...,
                 text: Optional[str] = None,
                 **kwargs
                 ):
        self.baseCfg(**kwargs)

        if text is not None:
            self.setText(text)

        self.clicked.connect(function)
        return self


class OptWebView(QWebEngineView, AbstractWidget):

    def setWidgets(self,
                   htmlFile: Union[PathLike, str] = None,
                   **kwargs
                   ):
        self.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.baseCfg(**kwargs)

        if htmlFile is not None:
            self.setHtml(open(htmlFile, 'r', encoding='u8').read())

        return self


class OptLineEdit(QLineEdit, AbstractWidget):
    Model: QStringListModel = QStringListModel([''])
    Completer = QCompleter(Model)

    def setWidgets(self,
                   enable: bool = True,
                   text: Optional[str] = None,
                   menuPolicy: Qt.ContextMenuPolicy = Qt.NoContextMenu,
                   maxLen: Optional[int] = None,
                   placeholderText : Optional[str] = None,
                   **kwargs
                   ):
        self.setEnabled(enable)
        self.setContextMenuPolicy(menuPolicy)
        self.baseCfg(**kwargs)

        self.Completer.setMaxVisibleItems(5)
        self.Completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.Completer.setFilterMode(Qt.MatchContains)
        self.Completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.setCompleter(self.Completer)
        if placeholderText is not None:
            self.setPlaceholderText(placeholderText)

        if text is not None:
            self.setText(text)

        if maxLen is not None:
            self.setMaxLength(maxLen)

        return self

    def renewModel(self, model: List[str]) -> 'OptLineEdit':
        self.Model.setStringList(model)
        return self


class OptSlider(QSlider, AbstractWidget):
    def setWidgets(self,
                   minNumber: int,
                   maxNumber: int,
                   step: int,
                   defaultValue: int,
                   horizontal: bool = False,
                   function: Callable = lambda: ...,
                   **kwargs
                   ):
        self.setMinimum(minNumber)
        self.setMaximum(maxNumber)
        self.setSingleStep(step)
        self.setValue(defaultValue)
        self.baseCfg(**kwargs)
        self.valueChanged: pyqtBoundSignal
        self.valueChanged.connect(function if function is not None else lambda: ...)
        self.setOrientation(Qt.Horizontal if horizontal else Qt.Vertical)
        return self


class OptComBox(QComboBox, AbstractWidget):

    def wheelEvent(self, e: QWheelEvent, *args): ...

    def setWidgets(self,
                   items: Iterable,
                   currentIndex: int = 0,
                   function: Callable = lambda: ...,
                   **kwargs):
        self.addItems(items)
        self.baseCfg(**kwargs)
        self.setCurrentIndex(currentIndex)
        self.currentIndexChanged: pyqtBoundSignal
        self.currentIndexChanged.connect(function if function is not None else lambda: ...)
        return self


class OptGroup(QGroupBox, AbstractWidget):
    def setWidgets(self,
                   title: Optional[str] = None,
                   items: list[QWidget] = None,
                   items_kwargs: list[dict] = None,
                   **kwargs
                   ):
        if title is not None:
            self.setTitle(title)

        if items is not None and items_kwargs is not None and len(items) == len(items_kwargs):
            for item in items:
                item.setParent(self)
                item.setWidgets(items_kwargs)

        self.baseCfg(**kwargs)
        return self


class OptToggleButton(QRadioButton, AbstractWidget):
    def setWidgets(self,
                   function: Callable = lambda: ...,
                   shortcuts: Optional[str] = None,
                   **kwargs
                   ):
        self.toggled: pyqtBoundSignal
        self.toggled.connect(function if function is not None else lambda: ...)
        self.baseCfg(**kwargs)

        if shortcuts is not None:
            self.setShortcut(shortcuts)

        return self


class ToggleButtonGroup(AbstractWidget):
    ToggleButtonLists: [OptToggleButton] = []

    def setWidgets(self, widgets: list[OptToggleButton], **kwargs):
        super().__init__()

        for widget in widgets:
            widget.setParent(self)
            if isinstance(widget, OptToggleButton): self.ToggleButtonLists.append(widget)

        self.baseCfg(**kwargs)
        return self


class OptAppication(QApplication):
    def __init__(self, argv: list):
        super().__init__(argv)

    def setWidgets(self,
                   attribute=Qt.AA_EnableHighDpiScaling,
                   display_name: Optional[str] = None,
                   icon: QIcon | str = None
                   ):
        if display_name is not None:
            self.setApplicationDisplayName(display_name)

        if isinstance(icon, str):
            self.setWindowIcon(QIcon(icon))
        else:
            self.setWindowIcon(icon)
        self.setAttribute(attribute)
        return self


class OptStack(QStackedWidget, AbstractWidget):
    def setWidgets(self,
                   widgets: list[QWidget],
                   currentIndex: int = 0,
                   **kwargs):
        self.baseCfg(**kwargs)
        for widget in widgets:
            self.addWidget(widget)
        self.setCurrentIndex(currentIndex)
        return self


class OptSplitter(QSplitter, AbstractWidget):
    def setWidgets(self,
                   widgets: list[QWidget],
                   sizes: Optional[list] = None,
                   collapsible: bool = True,
                   handleWidth: int = 10,
                   handleIndex: Optional[int] = None,
                   handleTips: Optional[str] = None,
                   handleCursor: Optional[str] = None,
                   horizontal: bool = False,
                   **kwargs
                   ):
        self.setChildrenCollapsible(collapsible)
        self.setHandleWidth(handleWidth)
        self.setOrientation(Qt.Horizontal if horizontal else Qt.Vertical)
        self.baseCfg(**kwargs)

        for widget in widgets:
            self.addWidget(widget)

        if handleIndex is not None:
            handle: QSplitterHandle = self.handle(handleIndex)
            if handleTips is not None: handle.setToolTip(handleTips)
            if handleCursor is not None: handle.setCursor(QCursor(QPixmap(handleCursor)))

        if sizes is not None:
            self.setSizes(sizes)

        return self

class OptToolBar(QToolBar, AbstractWidget):
    def setWidgets(self,
                   widgets: Optional[Iterable] = None,
                   actions: Optional[Iterable] = None,
                   horizontal: bool = True,
                   **kwargs
                   ):

        self.baseCfg(**kwargs)

        if horizontal:
            self.setOrientation(Qt.Horizontal)
        else:
            self.setOrientation(Qt.Vertical)

        if widgets is not None:
            for widget in widgets:
                self.addWidget(widget)
        if actions is not None: self.addActions(actions)

        self.setAcceptDrops(True)

        return self

    def addWidgets(self, widgets: Iterable[QWidget]):
        for widget in widgets:
            self.addWidget(widget)


class OptDock(QDockWidget, AbstractWidget):
    def setWidgets(self,
                   title: Optional[str] = None,
                   titleBarWidget: Optional[QWidget] = None,
                   insiderWidget: Optional[QWidget] = None,
                   **kwargs):
        self.baseCfg(**kwargs)

        if title is not None:
            self.setWindowTitle(title)

        if titleBarWidget is not None:
            self.setTitleBarWidget(titleBarWidget)

        if insiderWidget is not None:
            self.setWidget(insiderWidget)

        return self

    def setBeautifulEdgeShadow(self,
                               offset: tuple = (10., 10.),
                               radius: int = 15,
                               color=Qt.red
                               ):
        self.setGraphicsEffect(
            ShadowEffects(
                parent=self,
                offset=offset,
                radius=radius,
                color=color
            )
        )

        return self

    def closeEvent(self, event, _QCloseEvent=None):
        self.setVisible(not self.isVisible())

class OptAction(QAction):
    def setWidgets(self,
                   parent: Optional[QWidget] = None,
                   icon: Optional[QIcon] = None,
                   text: Optional[str] = None,
                   function: Callable = lambda: ...,
                   objectName: Optional[str] = None,
                   tips: Optional[str] = None,
                   shortcuts: Optional[str] = None,
                   enable: bool = True,
                   ):
        self.setEnabled(enable)
        if parent is not None:
            self.setParent(parent)

        if icon is not None:
            self.setIcon(icon)
            self.setIconVisibleInMenu(True)
        if text is not None:
            self.setText(text)
        if function is not None:
            self.triggered.connect(function)
        if objectName is not None:
            self.setObjectName(objectName)
        if tips is not None:
            self.setToolTip(tips)
        if shortcuts is not None:
            self.setShortcut(shortcuts)
        return self
class OptSeparator: pass

class OptMenu(QMenu, AbstractWidget):
    def setWidgets(self,
                   title: Optional[str] = None,
                   icon: Optional[QIcon] = None,
                   widgets: Optional[dict] = None,
                   enable: bool = True,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setEnabled(enable)

        if title is not None:
            self.setTitle(title)
        if icon is not None:
            self.setIcon(icon)
        if widgets is not None:
            '''
            0代表QMenu一类
            1代表QAction一类
            2代表分割线
            '''
            for _, key in enumerate(widgets):
                if widgets[key] == 0:
                    self.addMenu(key)
                elif widgets[key] == 1:
                    self.addAction(key)
                elif widgets[key] == 2:
                    self.addSeparator()
                else:
                    pass

        return self

    def JustActions(self,
                    actions: List[OptAction] | list[QAction],
                    title: Optional[str] = None,
                    icon: Optional[QIcon] = None,
                    enable: bool = True,
                    **kwargs
                    ):
        self.setEnabled(enable)
        self.baseCfg(**kwargs)

        if title is not None:
            self.setTitle(title)

        if icon is not None:
            self.setIcon(icon)

        self.addActions(actions)
        return self

    def JustMenus(self,
                  menus: List['OptMenu'] | List[QMenu],
                  title: Optional[str] = None,
                  icon: Optional[QIcon] = None,
                  enable: bool = True,
                  **kwargs
                  ):
        self.baseCfg(**kwargs)
        self.setEnabled(enable)

        if title is not None:
            self.setTitle(title)

        if icon is not None:
            self.setIcon(icon)

        for menu in menus:
            self.addMenu(menu)
        return self

class OptMenuBar(QMenuBar, AbstractWidget):
    def setWidgets(self,
                   widgets: Optional[dict] = None,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        if widgets is not None:
            for _, key in enumerate(widgets):
                if widgets[key] == 0:
                    self.addMenu(key)
                elif widgets[key] == 1:
                    self.addAction(key)
                elif widgets[key] == 2:
                    self.addSeparator()
                else:
                    pass
        return self


class OptStatusBar(QStatusBar, AbstractWidget):
    def setWidgets(self,
                   statusTip: Optional[str] = None,
                   **kwargs
                   ):
        if statusTip is not None:
            self.setStatusTip(statusTip)
        self.baseCfg(**kwargs)

        return self

class OptTableItem(QTableWidgetItem):
    def __hash__(self):
        return hash(id(self))

    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError or TypeError:
            return super().__lt__(other)

    def setWidgets(self,
                   text: str,
                   icon: str | QIcon | None = None,
                   textModel: Qt.Alignment | int = Qt.AlignCenter,
                   tips: Optional[str] = None,
                   checkState : Optional[Qt.CheckState] = None,
                   flags : Qt.ItemFlag | Qt.ItemFlags | None = None
                   ):
        self.setText(text)
        self.setTextAlignment(textModel)
        if isinstance(icon, str):
            self.setIcon(QIcon(icon))
        elif isinstance(icon, QIcon):
            self.setIcon(icon)
        else:
            pass
        if tips is not None:
            self.setToolTip(tips)
        if checkState is not None:
            self.setCheckState(checkState)
        if flags is not None:
            self.setFlags(flags)
        return self

    def setAttributes(self,
                      font: Optional[QFont] = None,
                      foregroundColor: QBrush | QColor | QGradient | None = None,
                      backgroundColor: QBrush | QColor | QGradient | None = None
                      ):
        if foregroundColor is not None:
            self.setForeground(foregroundColor)

        if backgroundColor is not None:
            self.setBackground(backgroundColor)

        if font is not None:
            self.setFont(font)
        return self

class OptProgressBar(QProgressBar, AbstractWidget):
    def setWidgets(self,
                   value: int = 10,
                   horizontal: bool = True,
                   minNumber: int = 0,
                   maxNumber: int = 100,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setValue(value)
        self.setOrientation(Qt.Horizontal if horizontal else Qt.Vertical)
        self.setMinimum(minNumber)
        self.setMaximum(maxNumber)

        return self

class OptTabBar(QTabBar, AbstractWidget):
    def setWidgets(self,
                   tabs: Optional[List] = None,
                   shape_direct: Optional[QTabBar.Shape] = None,
                   drawBase: bool = True,
                   toggle_function: Callable = lambda: ...,
                   **kwargs
                   ) -> 'OptTabBar':
        if tabs is not None:
            for tab in tabs:
                self.addTab(tab)

        if shape_direct is not None:
            self.setShape(shape_direct)

        self.currentChanged.connect(toggle_function)

        self.setDrawBase(drawBase)
        self.baseCfg(**kwargs)

        return self


class PartingLine(QFrame, AbstractWidget):
    def setWidgets(self,
                   shadow: QFrame.Shadow | int = QFrame.Shadow.Plain,
                   horizontal: bool = True,
                   width: int = 10,
                   width_or_heightr: int = 10,
                   color: Optional[QColor] = None,
                   **kwargs
                   ) -> 'PartingLine':
        self.baseCfg(**kwargs)
        self.setFrameShadow(shadow)
        self.setLineWidth(width)
        if horizontal:
            self.setFrameShape(QFrame.Shape.HLine)
            self.setMinimumHeight(width_or_heightr)
        else:
            self.setFrameShape(QFrame.Shape.VLine)
            self.setMinimumWidth(width_or_heightr)
        if color is not None:
            self.setStyleSheet(f'color : {color};')
        return self


class OptToolBox(QToolBox, AbstractWidget):
    def setWidgets(self,
                   items: dict[QWidget, str],
                   icons: Optional[list[QIcon]] = None,
                   currentIndex: int = 0,
                   frameStyle: QFrame.Shape = QFrame.Sunken,
                   frameShadow: QFrame.Shadow = QFrame.Raised,
                   currentChanged_function: Callable = lambda: ...,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setCurrentIndex(currentIndex)
        self.setFrameStyle(frameStyle)
        self.setFrameShadow(frameShadow)
        self.currentChanged.connect(currentChanged_function)
        if icons is None:
            for _, key in enumerate(items):
                self.addItem(key, items[key])
        else:
            for index, key in enumerate(items):
                self.addItem(
                    key, icons[index], items[key]
                )

        return self

class OptTabWidget(QTabWidget, AbstractWidget):
    HistoryTabs: list[QWidget] = []

    def addWidget(self, tabSet: TabWidgetDict) -> None:
        widget: Optional[QWidget] = tabSet['widget'] if 'widget' in tabSet else AbstractWidget()
        icon: Optional[Union[str, QIcon]] = tabSet['icon'] if 'icon' in tabSet else None
        text: Optional[str] = tabSet['text'] if 'text' in tabSet else ''
        enabled: Optional[bool] = tabSet['enabled'] if 'enabled' in tabSet else True
        tips: Optional[str] = tabSet['tips'] if 'tips' in tabSet else None
        self.HistoryTabs.append(widget)
        self.addTab(widget, text)
        index = self.count() - 1
        if icon is not None:
            self.setTabIcon(index, QIcon(icon) if isinstance(icon, str) else icon)
        if text is not None:
            self.setTabText(index, text)
        if enabled is not None:
            self.setTabEnabled(index, enabled)
        if tips is not None:
            self.setTabToolTip(index, tips)

    def addWidgets(self, tabSets: List[TabWidgetDict]) -> None:
        each_tab_cfg: TabWidgetDict
        for _, each_tab_cfg in enumerate(tabSets):
            widget: Optional[QWidget] = each_tab_cfg['widget'] if 'widget' in each_tab_cfg else AbstractWidget()
            icon: Optional[Union[str, QIcon]] = each_tab_cfg['icon'] if 'icon' in each_tab_cfg else None
            text: Optional[str] = each_tab_cfg['text'] if 'text' in each_tab_cfg else ''
            enabled: Optional[bool] = each_tab_cfg['enabled'] if 'enabled' in each_tab_cfg else True
            tips: Optional[str] = each_tab_cfg['tips'] if 'tips' in each_tab_cfg else None
            self.HistoryTabs.append(widget)
            self.addTab(widget, text)
            if icon is not None:
                self.setTabIcon(self.count() - 1, QIcon(icon) if isinstance(icon, str) else icon)
            if text is not None:
                self.setTabText(self.count() - 1, text)
            if enabled is not None:
                self.setTabEnabled(self.count() - 1, enabled)
            if tips is not None:
                self.setTabToolTip(self.count() - 1, tips)

    def setWidgets(self,
                   tabSets: List[TabWidgetDict] | None = None,
                   enClosed: bool = False,
                   tabsShape: QTabWidget.TabShape = QTabWidget.TabShape.Rounded,
                   position: QTabWidget.TabPosition = QTabWidget.TabPosition.North,
                   currentIndex : int = 0,
                   movable : bool = False,
                   handleTabMoved : Callable = lambda : ...,
                   closeTab : Callable = lambda : ...,
                   tabCursor : Optional[str] = None,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setTabsClosable(enClosed)
        self.setTabShape(tabsShape)
        self.setTabPosition(position)
        self.setCurrentIndex(currentIndex)
        tabBar : QTabBar = self.tabBar()
        tabBar.setMovable(movable)
        tabBar.tabMoved.connect(handleTabMoved)
        if tabCursor is not None:
            tabBar.setCursor(QCursor(QPixmap(tabCursor)))
        self.tabCloseRequested.connect(closeTab)

        if tabSets is not None:
            self.addWidgets(tabSets)

        return self

class OptCheckBox(QCheckBox, AbstractWidget):
    def setWidgets(self,
                   text_model: bool = True,
                   text: str = '',
                   icon_model: bool = False,
                   icon: str | QIcon | None = None,
                   enabled: bool = True,
                   isChecked: bool = False,
                   ceckState: Qt.CheckState = Qt.CheckState.Checked,
                   triState: bool = False,
                   state_changed_function: Optional[Callable] = None,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setEnabled(enabled)
        self.setChecked(isChecked)
        self.setCheckState(ceckState)
        self.setTristate(triState)

        if text_model:
            self.setText(text)
        elif icon_model:
            if isinstance(icon, QIcon):
                self.setIcon(icon)
            elif isinstance(icon, str):
                self.setIcon(QIcon(icon))
            else:
                pass
        else:
            pass

        if state_changed_function is not None:
            self.stateChanged.connect(state_changed_function)

        return self


class OptTreeView(QTreeView, AbstractWidget):
    def setWidgets(self,
                   headerView: Optional[QHeaderView] = None,
                   model: Optional['OptStandardItemModel'] = None,
                   expandAll: bool = True,
                   style: Optional[Union[QStyleFactory, QStyle]] = QStyleFactory.create('windows'),
                   itemsModel: QAbstractItemView.EditTrigger | QAbstractItemView.EditTriggers | None = None,
                   rootIsDecorated: bool = True,
                   frameStyle=QFrame.NoFrame,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setFrameStyle(frameStyle)
        self.setRootIsDecorated(rootIsDecorated)

        if itemsModel is not None:
            self.setEditTriggers(itemsModel)

        if expandAll:
            self.expandAll()

        if headerView is not None:
            self.setHeader(headerView)

        if model is not None:
            self.setModel(model)

        if style is not None:
            self.setStyle(style)

        return self

    # 重设某处的Item为控件类
    def resetIndexWidget(self, row: int, col: int, widget: QWidget):
        self.setIndexWidget(
            self.model().index(row, col),
            widget
        )

    # 重设某列的Item为全为某类控件不同的实例
    def setIndexesToWidgets(self, rows: Iterable[int], col: int, widget: QWidget):
        for row in rows: self.resetIndexWidget(row, col, widget)


class OptStandardItem(QStandardItem):

    def setWidgets(self,
                   text: Optional[str] = None,
                   icon: str | QIcon | None = None,
                   textModel: Qt.Alignment | int = Qt.AlignLeft,
                   selectable: bool = True,
                   tips: Optional[str] = None,
                   checkable: Optional[bool] = None,
                   checkState: Qt.CheckState = Qt.CheckState.Unchecked,
                   tristate: bool = False,
                   editable: bool = False
                   ):
        self.setTextAlignment(textModel)
        self.setSelectable(selectable)
        self.setEditable(editable)
        if checkable is not None:
            self.setCheckable(checkable)
            self.setCheckState(checkState)
            self.setTristate(tristate)

        if text is not None:
            self.setText(text)

        if isinstance(icon, str):
            self.setIcon(QIcon(icon))
        elif isinstance(icon, QIcon):
            self.setIcon(icon)
        else:
            pass
        if tips is not None:
            self.setToolTip(tips)

        return self

    def setAttributes(self,
                      font: Optional[QFont] = None,
                      foregroundColor: QBrush | QColor | QGradient | None = None,
                      backgroundColor: QBrush | QColor | QGradient | None = None
                      ):
        if foregroundColor is not None:
            self.setForeground(foregroundColor)

        if backgroundColor is not None:
            self.setBackground(backgroundColor)

        if font is not None:
            self.setFont(font)

        return self

    def setUnifiedAndContinuousCells(self,
                                     children: List[QObject],
                                     row: Optional[int] = None,
                                     col: Optional[int] = None,
                                     from_col: Optional[int] = None,
                                     from_row: Optional[int] = None
                                     ):
        # 某行上
        if row is not None and from_col is not None:
            for index, child in enumerate(children):
                self.setChild(row, from_col + index, child)
        elif col is not None and from_row is not None:
            for index, child in enumerate(children):
                self.setChild(from_row + index, col, child)
        else:
            pass
        # 某列上
        return self

    # 创建多行——行的首列是带有可勾选框的Item
    def setUnifiedAndContinuousRowCellsWithFirstCheckableBtn(self,
                                                             children: set | list,
                                                             col: int = 1,
                                                             from_row: int = 0,
                                                             checkState: Qt.CheckState = Qt.CheckState.Unchecked
                                                             ):
        for index, _child in enumerate(children):
            checkedItem = QStandardItem()
            checkedItem.setCheckable(True)
            checkedItem.setCheckState(checkState)
            self.setChild(from_row + index, 0, checkedItem)
            child = QStandardItem()
            child.setText(str(_child))
            child.setCheckState(checkState)
            self.setChild(from_row + index, col, child)
        return self


class OptStandardItemModel(QStandardItemModel):
    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)

    def setWidgets(self,
                   rowItems: Iterable[QStandardItem] | Iterable['OptStandardItem'] | None = None,
                   rowsOneLine: bool = False,
                   colItems: Iterable[QStandardItem] | Iterable['OptStandardItem'] | None = None,
                   horizontalHeaderLabels: Iterable[str] | None = None,
                   verticalHeaderLabels: Iterable[str] = None,
                   ):

        if horizontalHeaderLabels is not None:
            self.setHorizontalHeaderLabels(horizontalHeaderLabels)

        if verticalHeaderLabels is not None:
            self.setVerticalHeaderLabels(verticalHeaderLabels)
        if rowItems is not None:
            if rowsOneLine:
                self.appendRow(rowItems)
            else:
                for r in rowItems:
                    self.appendRow(r)

        if colItems is not None:
            self.appendColumn(colItems)

        return self

    def resetItem(self, *args) -> 'OptStandardItemModel':
        self.setItem(*args)
        return self

class MdiDesigner(QMdiArea, AbstractWidget):
    def setWidgets(self,
                   viewMode : QMdiArea.ViewMode = QMdiArea.TabbedView,
                   option: Optional[QMdiArea.AreaOption] = None,
                   activationOrder : Optional[QMdiArea.WindowOrder] = None,
                   background_color : Union[QBrush, QColor, Qt.GlobalColor, QGradient] = QColor('grey'),
                   tabposition : Optional[QTabWidget.TabPosition] = None,
                   tabshape : Optional[QTabWidget.TabShape] = None,
                   tabmovable : bool = True,
                   tabclosable : bool = True,
                   documentMode : bool = False,
                   **kwargs
                   ):
        self.baseCfg(**kwargs)
        self.setViewMode(viewMode)
        self.setBackground(background_color)

        if option is not None:
            self.setOption(option)

        if activationOrder is not None:
            self.setActivationOrder(activationOrder)

        if self.viewMode() == QMdiArea.TabbedView:
            if tabposition is not None:
                self.setTabPosition(tabposition)
            if tabshape is not None:
                self.setTabShape(tabshape)
            self.setTabsMovable(tabmovable)
            self.setDocumentMode(documentMode)
            self.setTabsClosable(tabclosable)
        return self

class MdiSubWindow(QMdiSubWindow, AbstractWidget):
    def setWidgets(self, widget : QWidget, **kwargs):
        self.setWidget(widget)
        self.baseCfg(**kwargs)
        return self


