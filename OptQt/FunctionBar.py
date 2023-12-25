# 组合类控件的实现
from os.path import join, expanduser, exists
from qtawesome import icon as qticon
from OptQt.OptTableWidget import *
from OptQt.OptimizeQt import OptAppication
from Sources import ImageType, CursorType, MusicType

class FunctionsBar(AbstractWidget):

    __slots__ = ('SearchCellLabel', 'SearchCellEdit', 'FunctionsRecordsCombox', 'Hbox')

    def __init__(self):
        super().__init__()

        self.SearchCellBtn = OptPushButton()
        self.SearchCellEdit = OptLineEdit()
        self.FunctionsRecordsCombox = OptComBox()
        self.Hbox = OptHBox()
        self.setUI()

    def setUI(self):
        self.setLayout(self.Hbox)

    def setWidgets(self,
                   jump_function : Callable = lambda : ...,
                   **kwargs
                   ) -> 'FunctionsBar':
        super().baseCfg(**kwargs)

        self.Hbox.setWidgets(
            widgets=[
                self.SearchCellEdit, self.SearchCellBtn, self.FunctionsRecordsCombox
            ],
            aligns=[Qt.AlignLeft, Qt.AlignLeft, Qt.AlignLeft]
        )

        self.SearchCellBtn.setWidgets(
            icon_model=False,
            text_model=True,
            text='跳转',
            objectName='F-SearchCellBtn',
            cursor=CursorType.Link,
            maxh=40,
            minw=50,
            function=jump_function
        )

        self.SearchCellEdit.setWidgets(
            enable=True,
            objectName='F-SearchCellEdit',
            cursor=CursorType.Text,
            minw=200,
            maxw=400,
            maxh=40
        )

        self.FunctionsRecordsCombox.setWidgets(
            items=[],
            objectName='F-FunctionsRecordsCombox',
            cursor=CursorType.Link,
            minw=400,
            maxh=40
        )

        return self

if __name__ == '__main__':
    app = OptAppication([])
    app.setWidgets(
        display_name='FunctionsBar',
        icon=QIcon(ImageType.APP_LOGO)
    )
    ui = FunctionsBar()
    ui.setWidgets()
    ui.show()
    app.exec()