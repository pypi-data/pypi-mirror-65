from PyQt5.QtWidgets import QMenuBar,QAction
class TakMenuBar(QMenuBar):
    def __init__(self,mainWindow):
        super().__init__()
        self.mainWindow=mainWindow
        self.initMenuBar()
def takInitMenuBar(window):
    menuBar=window.menuBar()
    file=menuBar.addMenu('文件')
    #向QMenu小控件中添加按钮，子菜单
    file.addAction('New')

    #定义响应小控件按钮，并设置快捷键关联到操作按钮，添加到父菜单下
    save=QAction('Save',file)
    save.setShortcut('Ctrl+S')
    file.addAction(save)

    #创建新的子菜单项，并添加孙菜单
    edit=file.addMenu('Edit')
    edit.addAction('Copy')
    edit.addAction('Paste')

    #添加父菜单下
    quit=QAction('Quit',file)
    file.addAction(quit)

        #单击任何Qmenu对象，都会发射信号，绑定槽函数
        #file.triggered[QAction].connect(self.step)
        