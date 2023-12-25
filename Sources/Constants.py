from pathlib import Path
from random import randint
from PyQt5.QtGui import QColor

path = Path(__file__).parent

# html
class PageType:
    Dracula = str(path / "html" / "mainSurface_dracula.html")
    Skyblue = str(path / "html" / "mainSurface_skyblue.html")
    Cyan = str(path / "html" / "mainSurface_cyan.html")
    Snow = str(path / "html" / "mainSurface_snow.html")

# image
class ImageType:
    APP_LOGO = str(path / "image" / "logo.ico")
    PKG_LOGO = str(path / "image" / "app.ico")
    Loading = str(path / "image" / "loading.gif")
    Fail = str(path / "image" / "fail.png")
    Splash = str(path / "image" / "splash.jpg")
    DefaultBackground = str(path / 'image' / 'bg.jpg')
    Dracula = str(path / 'image' / 'dracula.png')
    Drag = str(path / 'image' / 'drag.png')
    White240 = str(path / 'image' / 'white240.png')

    # some icons for debug or default-using、plugins
    Coper_error_Icon = str(path / ".." / "Plugins" / "default" / "icons" / "cope_error.ico")
    Analysis_Icon = str(path / ".." / "Plugins" / "default" / "icons" / "analysis.ico")
    Calc_Icon = str(path / ".." / "Plugins" / "default" / "icons" / "calc.ico")
    Help_Icon = str(path / ".." / "Plugins" / "default" / "icons" / "help.ico")
    Shift_Icon = str(path / ".." / "Plugins" / "default" / "icons" / "shift.ico")
    Notebook_Icon = str(path / ".." / "Plugins" / "default" / "icons" / "note.ico")
    Trick_Icon = str(path / ".." / "Plugins" / "default" / "icons" / "trick.ico")

    # some menu or actions'icons
    MA_Functions = str(path / "image" / "icons" / "functions.svg")
    MA_Load = str(path / "image" / "icons" / "load.svg")
    MA_Copy = str(path / "image" / "icons" / "copy.svg")
    MA_Matrix = str(path / "image" / "icons" / "matrix.svg")
    MA_Expand_Tool = str(path / "image" / "icons" / "expand_tools.svg")
    MA_Lock = str(path / "image" / "icons" / "lock.svg")
    MA_Search = str(path / "image" / "icons" / "search.svg")
    MA_Open = str(path / "image" / "icons" / "open.svg")
    MA_Save = str(path / "image" / "icons" / "save.svg")
    MA_Save_As = str(path / "image" / "icons" / "save_as.svg")
    MA_Help = str(path / "image" / "icons" / "help.svg")
    MA_Align_Justify = str(path / "image" / "icons" / "align_justify.svg")
    MA_Close = str(path / "image" / "icons" / "close.svg")
    MA_Cubes = str(path / "image" / "icons" / "cubes.svg")
    MA_Home = str(path / "image" / "icons" / "home.svg")
    MA_Analysis = str(path / "image" / "icons" / "analysis.svg")
    MA_Setting = str(path / "image" / "icons" / "setting.svg")
    MA_Datasets = str(path / "image" / "icons" / "datasets.svg")
    MA_Datafix = str(path / "image" / "icons" / "datafix.svg")
    MA_Newcol = str(path / "image" / "icons" / "newcol.svg")
    MA_Up = str(path / "image" / "icons" / "up.svg")
    MA_Down = str(path / "image" / "icons" / "down.svg")
    MA_Exchangedata = str(path / "image" / "icons" / "exchangedata.svg")
    MA_Delcol = str(path / "image" / "icons" / "delcol.svg")
    MA_Delrow = str(path / "image" / "icons" / "delrow.svg")
    MA_Newrow = str(path / "image" / "icons" / "newrow.svg")
    MA_Advanced_Tools = str(path / "image" / "icons" / "advancedtools.svg")
    MA_Link = str(path / "image" / "icons" / "link.svg")
    MA_Marked = str(path / "image" / "icons" / "marked.svg")
    MA_Thaw = str(path / "image" / "icons" / "thaw.svg")
    MA_Cross = str(path / "image" / "icons" / "cross.svg")
    MA_Rename = str(path / "image" / "icons" / "rename.svg")
    MA_Tips = str(path / "image" / "icons" / "tips.svg")

    # icons for analysis
    Surface3d = str(path / "image" / "icons" / "surfacechart.svg")
    Scatter3d = str(path / "image" / "icons" / "scatter3dchart.svg")
    Bar3d = str(path / "image" / "icons" / "bar3dchart.svg")
    Scatter = str(path / "image" / "icons" / "scatterchart.svg")
    Polar = str(path / "image" / "icons" / "polarchart.svg")
    Pie = str(path / "image" / "icons" / "piechart.svg")
    Line = str(path / "image" / "icons" / "linechart.svg")
    Cotton = str(path / "image" / "icons" / "cottonchart.svg")
    Mixin = str(path / "image" / "icons" / "chartmixed.svg")
    Box = str(path / "image" / "icons" / "boxchart.svg")
    Bar = str(path / "image" / "icons" / "barchart.svg")

# Cursor
class CursorType:
    Busy = str(path / "mouseCursor" / "busy.cur")
    Help = str(path / "mouseCursor" / "help.cur")
    Move = str(path / "mouseCursor" / "move.cur")
    Link = str(path / "mouseCursor" / "link.cur")
    Text = str(path / "mouseCursor" / "text.cur")
    Table = str(path / "mouseCursor" / "table.cur")
    Working = str(path / "mouseCursor" / "working.cur")
    Normal = str(path / "mouseCursor" / "normal.cur")
    Vertical = str(path / "mouseCursor" / "vertical.cur")
    Precision = str(path / "mouseCursor" / "precision.cur")
    Alternate = str(path / "mouseCursor" / "alternate.cur")
    Diagonal1 = str(path / "mouseCursor" / "diagonal1.cur")
    Diagonal2 = str(path / "mouseCursor" / "diagonal2.cur")
    Horizontal = str(path / "mouseCursor" / "horizontal.cur")
    Unavailable = str(path / "mouseCursor" / "unavailable.cur")
    Handwriting = str(path / "mouseCursor" / "handwriting.cur")

# global-Theme
class ThemeType:
    Dracula = str(path / "theme" / "dracula.qss")
    Skyblue = str(path / "theme" / "skyblue.qss")
    Cyan = str(path / "theme" / "cyan.qss")
    Snow = str(path / "theme" / 'snow.qss')

# music
class MusicType:
    Success = str(path / "music" / "success.mp3")
    Error = str(path / "music" / "error.mp3")
    Tip = str(path / "music" / 'tip.mp3')

# global-font
GLOBAL_FONT = {
    'size' : 12,
    'family' : '微软雅黑'
}

# start-cfg
CFG_FILE = str(path / "cfg" / "config.json")

# plugins-file
PLUGINS_FILE = str(path / "../" / "Plugins" / "plugins.json")

# BACK_UP_EXCEL
BACK_UP_EXCEL = str(path / "logs" / "backup.xlsx")

def __generate_random_colors(num_colors):
    colors = list()
    while len(colors) < num_colors:
        # 生成随机颜色
        color = QColor(
                randint(0, 255),
                randint(0, 255),
                randint(0, 255)
        )
        colors.append(color)
    return colors

# 生成50个不同的QColor
RandomColorLists = __generate_random_colors(50)