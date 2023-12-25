from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from typing import *
from qtawesome import icon as qticon

class TextEditorSelf(QTextEdit):
    def __init__(self):
        super().__init__()


class TextBrowserSelf(QTextBrowser):
    def __init__(self):
        super().__init__()


class MDEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.MidSplitter = QSplitter()
        self.DirSplitter = QSplitter()
        self.ToolSplitter = QSplitter()
        self.TextEdit = TextEditorSelf()
        self.TextShow = TextBrowserSelf()
        self.DirTree = QTableView()
        self.MenuBar = QMenuBar()
        self.StatusBar = QStatusBar()
        self.ToolsWidget = QWidget()

        self.setUI()

    def setUI(self):
        self.setCentralWidget(self.ToolSplitter)
        self.setStatusBar(self.StatusBar)
        self.setMenuBar(self.MenuBar)

    def setWidgets(self) -> 'MDEditor':
        self.DirSplitter.addWidget(self.DirTree)
        self.DirSplitter.addWidget(self.MidSplitter)

        model = QFileSystemModel()
        model.setRootPath("")
        self.DirTree.setModel(model)

        self.MidSplitter.addWidget(self.TextEdit)
        self.MidSplitter.addWidget(self.TextShow)
        self.TextEdit.textChanged.connect(
            lambda: self.TextShow.setMarkdown(self.TextEdit.toPlainText())
        )

        self.ToolSplitter.addWidget(self.DirSplitter)
        self.ToolSplitter.addWidget(self.ToolsWidget)

        self.DirTree.setStyleSheet('background-color : pink')
        self.TextEdit.setStyleSheet('background-color : tan')
        self.TextShow.setStyleSheet('background-color : lightskyblue')
        self.ToolsWidget.setStyleSheet('background-color : yellow')

        self.MenuBar.addMenu(QMenu('Menu', self.MenuBar))

        return self

def main(widget: '',
         icon=qticon('ri.markdown-fill', color='darkblue'),
         text='MD编辑器',
         tips='内置的Markdown编辑器',
         ) -> dict:
    return dict(
        widget=MDEditor().setWidgets(),
        icon=icon,
        text=text,
        tips=tips
    )

if __name__ == '__main__':
    app = QApplication([])
    ui = MDEditor()
    ui.setWidgets()
    ui.show()
    app.exec()

__all__ = ['main']
