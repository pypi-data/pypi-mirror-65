from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel,QPushButton,QToolBar,QAction,QComboBox,QScrollBar
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import Qt
class TakControlBar(QToolBar):
    mainWindow=None
    def __init__(self,mainWindow):
        super().__init__()
        self.mainWindow=mainWindow
        self.initBarWidgets()
    
    def singleStep(self):
        self.mainWindow.singleStep()
        self.pauseToolButton.setText("继续")
        
    def resetModel(self):
        self.mainWindow.resetModel()
        self.pauseToolButton.setText("开始")
        
    def setSpeed(self):
        self.mainWindow.setSpeed( self.speedControl.value())
        
    def pause(self):
        self.mainWindow.pause()# 主窗口停止或者继续
        if(self.mainWindow.running==True):
            self.pauseToolButton.setText("暂停")
        else:
            self.pauseToolButton.setText("继续")
        
    def showSpeed(self,currentStep,speedDic):
        '''
         当前步数(int)，速度（dict）
        '''
        speedText="当前步：%d, 设定步速：%.2f/s,实际帧率：%.2f/s,实际步速：%.2f/s"%(
            currentStep,
            speedDic['given'],speedDic['frames/s'],speedDic['steps/s'])
        self.showSpeedLabel.setText(speedText)
        
    def initBarWidgets(self):# 初始化类、
        if(self.mainWindow==None):
            raise Exception("takagiwidgets.contolbar.ControlBar初始化时需要传入一QMainWindow作为参数。")
        self.stepToolButton=QAction("单步",self)
        self.addAction(self.stepToolButton)
        self.stepToolButton.triggered.connect(self.singleStep)
        
        self.restartToolButton=QAction(QIcon(QPixmap("./image/wifi.png")),"重启",self)
        self.addAction(self.restartToolButton)
        self.restartToolButton.triggered.connect(self.resetModel)
        
        self.pauseToolButton=QAction(QIcon(QPixmap("./image/wifi.png")),"开始",self)
        self.addAction(self.pauseToolButton)
        self.pauseToolButton.triggered.connect(self.pause)
        
        self.box = QComboBox()
        self.box.insertItem(0,'hahahah')

        self.speedControl=QScrollBar(Qt.Horizontal)
        self.speedControl.setMaximum(2000)
        self.speedControl.setMinimum(1)
        self.speedControl.valueChanged.connect(self.setSpeed)
        
        
        self.speedControl.setMinimumWidth(250)
        
        self.addWidget(self.speedControl)
        self.showSpeedLabel=QLabel("")
        self.addWidget(self.showSpeedLabel)

        
        self.speedControl.setValue(20)
        