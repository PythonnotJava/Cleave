from os.path import expanduser, join, exists
from pandas import read_csv, read_excel, DataFrame
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from OptQt.OptComponent import ReWriteAnyWidgetDialog, LoadingDialog
from OptQt.OptimizeQt import *
from OptQt.ColorPalette import ColorPaletter
from Sources import *
from Util.tablewidget_functions import WhenGetTableWidgetDatas

# @self : ExcelKernel

# 标记一个线程执行完成并释放
def __handleThreadFinished(thread):
    print("Thread finished.")
    thread.wait()
    thread.deleteLater()

# 调整滑块
def WhenSetSliderToCells(self) -> None:
    value = self.StatusWidget.ExcelSizeSlider.value()
    self.StatusWidget.showMessage(f'比例 : {value}%', 1000)
    for row in range(self.TableWidget.rowCount()):
        self.TableWidget.setRowHeight(row, value // 2)
    for col in range(self.TableWidget.columnCount()):
        self.TableWidget.setColumnWidth(col, value)


# 调整位置
def WhenSetAdjustAlignment(self, align: Qt.Alignment() = Qt.AlignCenter) -> None:
    for row in range(self.TableWidget.rowCount()):
        for col in range(self.TableWidget.columnCount()):
            item = self.TableWidget.item(row, col)
            if item is not None:
                item.setTextAlignment(align)
    self.TableWidget.CommonTextModel = align
    self.OprBar.StartTab.AlignLeftBtn.setEnabled(not align == (Qt.AlignLeft | Qt.AlignVCenter))
    self.OprBar.StartTab.AlignCenterBtn.setEnabled(not align == Qt.AlignCenter)
    self.OprBar.StartTab.AlignRightBtn.setEnabled(not align == (Qt.AlignRight | Qt.AlignVCenter))


# 调整字
def WhenSetAdjustFont(self, family_or_size: str = 'f'):
    match family_or_size:
        case 'f':
            f = self.OprBar.StartTab.FontFamilyBox.currentText()
            self.TableWidget.CommonFont.setFamily(f)
        case 's':
            s = int(self.OprBar.StartTab.FontSizeBox.currentText())
            self.TableWidget.CommonFont.setPointSize(s)
        case '':
            ...
    self.TableWidget.setFont(self.TableWidget.CommonFont)


# -----------------------------------------------------导入方面-------------------------------------------------------
# 仅仅导入文件，支持excel和csv
def WhenJustLoadFilesToTable(self, cancel_msg: str = 'Cancel Load...') -> Optional[Tuple[DataFrame, str]]:
    filePath, _ = QFileDialog.getOpenFileName(
        parent=self,
        caption='选择文件',
        directory=join(expanduser('~'), "Desktop"),
        filter="选择类型 建议xlsx(*.xlsx)\n xls(*.xls)\n csv(*.csv)"
    )
    filePath: Optional[str]
    dataF: DataFrame
    if filePath is not None and filePath != '':
        if filePath.endswith('.xls') or filePath.endswith('.xlsx'):
            dataF = read_excel(filePath, sheet_name=0)
            return dataF, filePath
        elif filePath.endswith('.csv'):
            dataF = read_csv(filePath)
            return dataF, filePath
        else:
            # @Msg_Error
            MusicPlayer.play(MusicType.Error, lasting=2)
            raise Exception("不支持的文件类型")
    else:
        print(cancel_msg)
        return


# 导入文件需要做的额外功能——核心功能之一，需要做到多重同步
def WhenSetItemsByFileLoader(self) -> None:
    def core() -> None:
        self.OprBar.StartTab.OpenBtn.setEnabled(False)
        data_filePath: Optional[Tuple[DataFrame, str]] = (
            WhenJustLoadFilesToTable(self, cancel_msg='Cancel Load...'))
        if data_filePath is not None:
            data: DataFrame = data_filePath[0]
            self.TableWidget.setHorizontalHeaderLabels([str(x) for x in data.columns])
            self.TableWidget.setRowCount(data.shape[0])
            self.TableWidget.setColumnCount(data.shape[1])

            for row in range(self.TableWidget.rowCount()):
                for col in range(self.TableWidget.columnCount()):
                    self.TableWidget.setItem(
                        row,
                        col,
                        OptTableItem().setWidgets(
                            text=str(data.iat[row, col]) if str(data.iat[row, col]) != 'nan' else '',
                            textModel=self.TableWidget.CommonTextModel
                        ).setAttributes(
                            backgroundColor=self.TableWidget.CommonCellBackgroundColor,
                            foregroundColor=self.TableWidget.CommonCellForegroundColor
                        )
                    )
            self.OprBar.StartTab.OpenEdit.setText(data_filePath[1])
            self.StatusWidget.showMessage("已经完全加载", 3000)
        self.OprBar.StartTab.OpenBtn.setEnabled(True)
        # @发射信号
        self.TableWidget.HeaderChangedSignal.emit()

    LoadingDialog(core).setWidgets().setUnStopped().exec_(self.mapToGlobal(self.TableWidget.getSelfCenterPos()))

# -----------------------------------------------------保存方面-------------------------------------------------------
# 保存到某个目录
def WhenJustSave(self, filePath: str) -> None:
    self.OprBar.StartTab.SaveAsBtn.setEnabled(False)
    self.OprBar.StartTab.JustSaveBtn.setEnabled(False)
    _datas: DataFrame = WhenGetTableWidgetDatas(self.TableWidget)
    try:
        if filePath.endswith('.xlsx'):
            _datas.to_excel(filePath, index=False)
            MusicPlayer.play(filePath=MusicType.Success, volume=50, lasting=2)
        elif filePath.endswith('.csv'):
            _datas.to_excel(filePath, index=False)
            MusicPlayer.play(filePath=MusicType.Success, volume=50, lasting=2)
        else:
            # @Msg_Error
            print("Unsupport FileType!")
            MusicPlayer.play(
                filePath=MusicType.Error,
                lasting=2
            )
    except PermissionError:
        # @Msg_Error
        print("File is openning in another Process!")
        MusicPlayer.play(filePath=MusicType.Error, lasting=2)
    self.OprBar.StartTab.SaveAsBtn.setEnabled(True)
    self.OprBar.StartTab.JustSaveBtn.setEnabled(True)


# 保存数据，仅支持csv格式和xlsx格式
def WhenSetSaveModel(self, justSave: bool = True) -> None:
    if justSave:
        filePath = self.OprBar.StartTab.OpenEdit.text()
        if exists(filePath):
            self.JustSaveThread = OptThread(lambda: WhenJustSave(self, filePath))
            self.JustSaveThread.signal.connect(lambda: print("Call Successfully!"))
            self.JustSaveThread.started.connect(lambda: print("A thread is running!"))
            self.JustSaveThread.finished.connect(lambda: __handleThreadFinished(self.JustSaveThread))
            self.JustSaveThread.start()
        else:
            MusicPlayer.play(filePath=MusicType.Error, lasting=2)
    else:
        filePath, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='保存文件',
            directory=join(expanduser('~'), "Desktop"),
            filter="保存类型 建议xlsx(*.xlsx)\n csv(*.csv)"
        )
        if filePath is not None and filePath != '':
            self.SaveAsThread = OptThread(lambda: WhenJustSave(self, filePath))
            self.SaveAsThread.signal.connect(lambda: print("Call Successfully!"))
            self.SaveAsThread.started.connect(lambda: print("A thread is running!"))
            self.SaveAsThread.finished.connect(lambda: __handleThreadFinished(self.SaveAsThread))
            self.SaveAsThread.start()
        else:
            print('Cancel Save...')


# ---------------------------------------------------匹配---------------------------------------------------
# 跳转
def WhenSetCurrentCellByJump(self):
    _text = self.OprBar.FunctionsBar.SearchCellEdit.text()
    if _text != '' and not _text.isspace() and _text is not None:
        try:
            colName, _row = _text.split(':')
            row = int(_row) - 1
            col = self.TableWidget.HeaderLabels.index(colName)
            self.TableWidget.setCurrentCell(row, col)
            MusicPlayer.play(filePath=MusicType.Tip, lasting=1.5)
        except ValueError:
            MusicPlayer.play(filePath=MusicType.Error, lasting=2)
        except AttributeError:
            MusicPlayer.play(filePath=MusicType.Error, lasting=2)


# 搜索匹配项背景颜色
def WhenSetMatchCellsBackgroundColor(self) -> None:
    colorPaletter = ColorPaletter()

    def __func():
        self.TableWidget.CommonCellHightlightColor = colorPaletter.Color
        self.SearchBar.SearchHighlight.setStyleSheet(f'background-color : {colorPaletter.name()}')
        colorPaletter.close()

    colorPaletter.setWidgets(
        initial=self.TableWidget.CommonCellHightlightColor,
        icon=ImageType.APP_LOGO,
        confirm_function=__func
    )
    colorPaletter.exec()


# 展示搜索匹配项目
def WhenSetMatchCellsShown(self) -> None:
    manners = {
        0: Qt.MatchContains,
        1: Qt.MatchExactly,
        2: Qt.MatchStartsWith,
        3: Qt.MatchEndsWith,
        4: Qt.MatchRegExp
    }

    # 首先清除之前的高亮单元格（如果有）
    hlitems: list = self.TableWidget.SpecificSignedCells['Hightlighted']
    if len(hlitems) != 0:
        for item in hlitems:
            try:
                item.setData(Qt.BackgroundRole, self.TableWidget.CommonCellBackgroundColor)
            except RuntimeError:
                pass
    _text = self.SearchBar.SearchEdit.text()
    if _text is not None and _text != '':
        hlitems.clear()
        hlitems.extend(self.TableWidget.findItems(_text, manners[self.SearchBar.SearchModel.currentIndex()]))
        for item in self.TableWidget.SpecificSignedCells['Hightlighted']:
            item.setData(Qt.BackgroundRole, self.TableWidget.CommonCellHightlightColor)
    self.SearchBar.setVisible(not self.SearchBar.isVisible())


# 撤销并恢复所有被高亮搜索选中的单元格
def WhenSetMatchCellsRecover(self) -> None:
    hlitems: list = self.TableWidget.SpecificSignedCells['Hightlighted']
    if len(hlitems) != 0:
        for item in hlitems:
            try:
                item.setData(Qt.BackgroundRole, self.TableWidget.CommonCellBackgroundColor)
            except RuntimeError:
                pass
        hlitems.clear()
    else:
        print("No cell requires beening recovered!")


# 格式按钮菜单栏
def __whenSetFormatActionFuncs(self, n: int) -> None:
    match n:
        case 0:
            __dialog = ReWriteAnyWidgetDialog()

            def __func(height: int):
                for row in range(self.TableWidget.rowCount()):
                    self.TableWidget.setRowHeight(row, height)
                __dialog.close()

            spin = QSpinBox()
            spin.setRange(30, 300)
            spin.setValue(self.TableWidget.rowHeight(0))
            __dialog.setWidgets(
                labelText='当前高度',
                title='修改行高',
                modal=True,
                fixSize=(300, 120),
                okBtn_text='确定',
                okBtn_function=lambda: __func(spin.value()),
                widget=spin
            )
            __dialog.exec_()
        case 1:
            __dialog = ReWriteAnyWidgetDialog()
            spin = QSpinBox()
            spin.setRange(30, 300)
            spin.setValue(self.TableWidget.columnWidth(0))

            def __func(width: int):
                for col in range(self.TableWidget.columnCount()):
                    self.TableWidget.setColumnWidth(col, width)
                __dialog.close()

            __dialog.setWidgets(
                labelText='当前宽度',
                title='修改列宽',
                modal=True,
                fixSize=(300, 120),
                okBtn_text='确定',
                okBtn_function=lambda: __func(spin.value()),
                widget=spin
            )
            __dialog.exec_()
        case 2:
            self.OpenADTools(1)


# 格式菜单栏
def WhenSetFormatMenu(self) -> None:
    menu = OptMenu(self)
    _subMenu = OptMenu(menu)
    menu.setWidgets(
        objectName='FormatMenu',
        qss='QMenu::item:selected{color:#1aa3ff;}',
        widgets={
            OptAction().setWidgets(
                parent=menu,
                text='修改行高',
                function=lambda: __whenSetFormatActionFuncs(self, 0)
            ): 1,
            OptAction().setWidgets(
                parent=menu,
                text='修改列宽',
                function=lambda: __whenSetFormatActionFuncs(self, 1)
            ): 1,
            OptSeparator(): 2,
            _subMenu.setWidgets(
                title='单元格属性',
                widgets={
                    OptAction().setWidgets(
                        parent=_subMenu,
                        text='样式(&Ctrl+&Shift+&T)',
                        function=lambda: __whenSetFormatActionFuncs(self, 2)
                    ): 1
                }
            ): 0
        }
    )
    menu.exec_(
        self.OprBar.StartTab.FormatBoxBtn.mapToGlobal(self.OprBar.StartTab.FormatBoxBtn.rect().bottomLeft())
    )
