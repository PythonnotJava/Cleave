from typing import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class ColorType:
    def __init__(self, r : int, g : int, b : int, a : int = 255):
        self.__rgba : List[int] = [r, g, b, a]

    def __add__(self, other : "ColorType"):
        for index in range(4):
            self.__rgba[index] += other.__rgba[index]
        return self

    @overload
    def __mul__(self, mul : Optional[float] = None): ...

    @overload
    def __mul__(self, muls : Tuple[float] = None): ...

    def __mul__(self, mul : Optional[float] = None, muls : Tuple[float] = None):
        if mul is not None:
            for index in range(4):
                self.__rgba[index] = int(mul * self.__rgba[index])
            return self
        else:
            for index, mul in enumerate(muls):
                self.__rgba[index] = mul * self.__rgba[index]
            return self

    def toQColor(self) -> QColor: return QColor(*self.__rgba)

    @property
    def RGBA(self) -> list:
        rgba = []
        for e in self.__rgba:
            if 0 <= e <= 255:
                pass
            elif e < 0:
                e = 0
            else:
                e = 255
            rgba.append(e)
        return rgba

    @RGBA.setter
    def RGBA(self, value : List[int]) -> None:
        self.__rgba.clear()
        self.__rgba.extend(value)

    @staticmethod
    def fromQColor(qc : QColor) -> "ColorType": return ColorType(qc.red(), qc.green(), qc.blue(), qc.alpha())

class QssSetter:
    def __init__(self,
                 color: QColor = Qt.black,
                 background_color: QColor = Qt.white,
                 border_color: QColor = Qt.white,
                 border_radius: int = 0,
                 border_width: int = 0,
                 border_style: str = 'solid',
                 target_with_actions: Optional[str] = None  # 例如 ： target_with_actions='QToolButton:clicked'
                 ):

        self._color = color
        self._background_color = background_color
        self._border_color = border_color
        self._border_radius = border_radius
        self._border_width = border_width
        self._border_style = border_style
        self.target_with_actions = target_with_actions

    @property
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, value: QColor):
        self._color = value

    @property
    def background_color(self) -> QColor:
        return self._background_color

    @background_color.setter
    def background_color(self, value: QColor):
        self._background_color = value

    @property
    def border_color(self) -> QColor:
        return self._border_color

    @border_color.setter
    def border_color(self, value: QColor):
        self._border_color = value

    @property
    def border_radius(self) -> int:
        return self._border_radius

    @border_radius.setter
    def border_radius(self, value: int):
        self._border_radius = value

    @property
    def border_width(self) -> int:
        return self._border_width

    @border_width.setter
    def border_width(self, value: int):
        self._border_width = value

    @property
    def border_style(self) -> str:
        return self._border_style

    @border_style.setter
    def border_style(self, value: str):
        self._border_style = value

    @property
    def qss(self) -> str:
        if self.target_with_actions is None:
            return (f"color : {self.color.name()};"
                    f"background-color : {self.background_color.name()};"
                    f"border-color : {self.border_color.name()};"
                    f"border-radius : {self.border_radius}px;"
                    f"border-style : {self.border_style};"
                    f"border-width : {self.border_width}px;"
                    )
        else:
            return """
            %s{
                color : %s;
                background-color : %s;
                border : %s;
                border-radius: %dpx;
                border-style : %s;
                border-width : %dpx;
            }
            """ % (
                self.target_with_actions, self.color.name(), self.background_color.name(),
                self.border_color.name(), self.border_radius, self.border_style, self.border_width
            )

    def __str__(self):
        return self.qss

class WidgetOrLayoutDict(TypedDict):
    align: Optional[Qt.Alignment]
    dtype: int
    obj: QObject | QWidget

class TabWidgetDict(TypedDict):
    widget: Optional[QWidget]
    text: Optional[str]
    icon: Optional[Union[str, QIcon]]
    enabled: Optional[bool]
    tips: Optional[str]

Red = ColorType(255, 0, 0, 255)
Green = ColorType(0, 255, 0, 255)
Blue = ColorType(0, 0, 255, 255)