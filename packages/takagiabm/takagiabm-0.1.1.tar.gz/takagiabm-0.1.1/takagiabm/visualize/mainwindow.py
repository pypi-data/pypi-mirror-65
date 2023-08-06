from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,QToolBar,QScrollBar,QWidget,\
QDesktopWidget,QAction,QComboBox,QLabel,QSplitter,QVBoxLayout,QTextEdit
from PyQt5.QtCore import Qt
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtOpenGL import QGLWidget
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pyqtgraph as pg
import time
import numpy as np
import math
from takagiabm.visualize.takagiwidgets.controlbar import TakControlBar
from takagiabm.visualize.takagiwidgets.menubar import TakMenuBar,takInitMenuBar
from takagiabm.visualize.takagiwidgets.valuewidgets.valuewidgetfactory import createValueWidget# .valuescrollwidget import TakValueScrollWidget
class TakBaseWindow(QMainWindow):
    """docstring for Mainwindow"""
    speed={'frames/s':0,'given':5,'steps/s':0,'maxfps':0}
    openGLWidget=None
    timeToUpdate=0
    timeToThisStep=0
    sourceFile=0
    def __init__(self, sourceFile='',parent = None,modelClass=None,varList=[],collectorList=[]):
        super(TakBaseWindow,self).__init__(parent)
        self.basic()
        self.varList=varList
        self.modelClass=modelClass
        self.model=modelClass()
        self.sourceFile=sourceFile
        
        self.controlBar=TakControlBar(self)
        
        self.addToolBar(self.controlBar)
        
        takInitMenuBar(self)# menuBar没有办法通过构造对象的方式获取，就只能这样弄了。    
        self.running=False
        

        
        
        #self.s = OpenGLWidget()
        self.stepsPerFrame=1
        self.stepToNextFrame=self.stepsPerFrame
        self.splitter_main = self.split_()
        self.setCentralWidget(self.splitter_main)
        self.s.setModel(self.model)
        
        self.refreshTimer = QtCore.QTimer()
        self.refreshTimer.timeout.connect(self.step)
        self.refreshTimer.start(1) 
        
        self.UITimer = QtCore.QTimer()
        self.UITimer.timeout.connect(self.updateUI)
        
        self.UITimer.start(1000) 
        
    
    def updateUI(self):
        self.showSpeed()
        self.agentViewer.setData(list(self.model.agentSet))

    def getRealSpeed(self):
        if(self.openGLWidget!=None):
            interval=self.openGLWidget.updateInterval 
            avgRefresh=self.openGLWidget.averageRefreshingTime
#            print("interval",interval)
            if(interval!=0)&(avgRefresh!=0): # 防止除以0
                self.speed['frames/s']=1.0/interval
                self.speed['maxfps']=1.0/avgRefresh
            deltaStep=self.model.currentStep-self.model.lastStep
            self.model.lastStep=self.model.currentStep
            self.speed['steps/s']=deltaStep
            
        
    def showSpeed(self):
        self.getRealSpeed()
        self.controlBar.showSpeed(self.model.currentStep,speedDic=self.speed)
        self.adjustSpeed()
        
    def adjustSpeed(self):
        '''
            根据当前刷新帧率以及输入的仿真速度，自动计算每次刷新对应的步数，并更新步数。
        '''
        if(self.speed['frames/s']>0):
            self.stepsPerFrame=round(1.0*self.speed['given']/self.speed['maxfps'])
            #print(self.stepsPerFrame)
        
    def setSpeed(self,speed):
    
        self.speed['given']=speed

        
    def resetModel(self):
        import sys
        from imp import reload# 要求：重新导入。        
        (self.sourcePath,sourceFileName) = os.path.split(self.sourceFile)
        (moduleName,ext) = os.path.splitext(sourceFileName)
        sys.path.append(self.sourcePath)   
        
        __import__(moduleName)   
        if(moduleName in sys.modules.keys()):
            
            del sys.modules[moduleName]     
            __import__(moduleName)
        else:
            __import__(moduleName)

        self.model=self.modelClass()
        self.openGLWidget.setModel(self.model)
        self.initControlPanel()
        self.running=False
        self.visualize()

    def pause(self):
        if self.running:
            
            self.running=False
        else:
            self.running=True
            

    
        
    def basic(self):
        #设置标题，大小，图标
        self.setWindowTitle("GT")
        self.setWindowIcon(QIcon("./image/Gt.png"))
        #居中显示
        screen = QDesktopWidget().geometry()
        self_size = self.geometry()
        self.move((screen.width() - self_size.width())/2,(screen.height() - self_size.height())/2)
    
    def initControlPanel(self):
        import sip
        print('count',self.controlLayout.count())
        for i in range(self.controlLayout.count()-1,0-1,-1):# 删除。 
            print(i)            
            print(i,self.controlLayout.itemAt(i).widget())
            w=self.controlLayout.itemAt(i).widget()
            #w.delete()
            sip.delete(w)
            del w
        for var in self.model.varList:
            if type(var)==type([]):
                pass
            else:            
                print(var)
                tvsw=createValueWidget(var)#TakValueScrollWidget(name=var.name)
    #             var.setValueWidget(tvsw)
                self.controlLayout.addWidget(tvsw)
    def split_(self):
        splitter = QSplitter(Qt.Vertical)
        #s = self.s #将opengl例子嵌入GUI
        
        self.base=OpenGLBaseWidget()
        self.s=self.base.openGLWidget
        self.openGLWidget=self.s
        l=QVBoxLayout()
        l.addWidget(self.s)
        self.base.setLayout(l)
        
        self_size = self.base.geometry()
        print(self_size)

        splitter.addWidget(self.base)
        testedit = QTextEdit()
        self.controlPanel=QWidget()
        self.controlLayout=QVBoxLayout()
        self.controlPanel.setLayout(self.controlLayout)
        self.initControlPanel()
        splitter.addWidget(self.controlPanel)
        splitter.addWidget(testedit)
        splitter.setStretchFactor(0,10)
        splitter.setStretchFactor(1,1)
        
        screen = QDesktopWidget().geometry()
        
        splitter_main = QSplitter(Qt.Horizontal)
        textedit_main = pg.DataTreeWidget(data=None)
        splitter_main.addWidget(textedit_main)
        self.agentViewer=textedit_main

        splitter_main.addWidget(splitter)

        splitter_main.setStretchFactor(0,1)
        splitter_main.setStretchFactor(1,3)
        
        return splitter_main
    def visualize(self):
        self.openGLWidget.update()# 刷新，生成网格。
        
    def singleStep(self):
        
        self.running=False
        
        
        self.model.step()
        self.visualize()
        print(self.model.currentStep)
    def step(self):
        
        if not self.running:
            return
        t=time.time()
        if(t<=self.timeToThisStep):
            #print("ret!")
            return
        self.model.step()
        if(self.stepToNextFrame<=1):
            self.visualize()
            self.stepToNextFrame=self.stepsPerFrame
        else:
            self.stepToNextFrame-=1
       # print(self.model.currentStep)
        self.timeToThisStep=t+1.0/self.speed['given']
        #print('timetothisstep',self.timeToThisStep,t)
        
class OpenGLBaseWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.openGLWidget=OpenGLWidget()
    def resizeEvent(self,event):
        
        size=self.size()
        
        s=min([size.width(),size.height()])
        self.openGLWidget.resize(s,s) 
        


class OpenGLWidget(QGLWidget):
    model=None
    refreshingTimeList=[]
    refreshingTimeListLen=10
    averageRefreshingTime=0# 刷新的平均时间
    lastUpdateTime=0
    updateInterval=0# 两次刷新之间的时间间隔
    def __init__(self):
        self.gridScale=[1,1]
        
        super().__init__()
        
    def setModel(self,model):
        self.model=model 
    def initializeGL(self):
        self.times=0
        glutInit([])
        glClearColor(0,0,0,1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def mouse(self,*k):
        print(k)
    def mousePressEvent(self,event):
        print(event.localPos(),event.x(),event.y(),event.windowPos(),event.globalX()
              ,event.globalY())
   

    def paintAgents(self):
       # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        for agent in list(self.model.agentSet):
            glBegin(GL_POLYGON)
            x=agent.pos[0]
            y=agent.pos[1]
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(x, y, 0)
            #glColor3f(0.0, 1.0, 0.0)
            glVertex3f( x+1, y, 0)
            #glColor3f(0.0, 0.0, 1.0)
            glVertex3f( x+1,  y+1, 0)
            glVertex3f( x,  y+1, 0)
            glEnd()
    def update(self):
        
        super().update()
        
    def calcRefreshTime(self,t1,t0):
        self.refreshingTimeList.append(t1-t0)
        if(len(self.refreshingTimeList)>=self.refreshingTimeListLen):
            self.refreshingTimeList.pop(0)
        self.averageRefreshingTime=sum(self.refreshingTimeList)/len(self.refreshingTimeList)*1.0
        
        self.updateInterval=t1-self.lastUpdateTime
        self.lastUpdateTime=t1
            
    
    def paintCellHatch(self):
        width=self.model.grid.width
        height=self.model.grid.height
        w=self.gridScale[0]
        h=self.gridScale[1]
        for x in range(width):
            
            for y in range(height):

                
                color=self.model.grid.getCellColorTupleF(pos=(x,y))
                glBegin(GL_POLYGON)
                glColor3f(color[0],color[1],color[2])   
                
                glVertex3f(x, y, 0)
                #glColor3f(0.0, 1.0, 0.0)
                glVertex3f( x+w, y, 0)
                #glColor3f(0.0, 0.0, 1.0)
                glVertex3f( x+w,  y+h, 0)
                glVertex3f( x,  y+h, 0)
                glEnd()
                #glRectf(x*w, y*h, (x+1)*w,(y+1)*h)      #画矩形 
        

                
    def resizeGL(self,w,h):
       # self.resize2(w,h)
        glViewport(0, 0, w, h);
        glLoadIdentity();
        
        glOrtho(0, self.model.grid.width*self.gridScale[0], 0.0, self.model.grid.height*self.gridScale[1]
                , 1.0, -1.0)
    def resize2(self,w,h):
        glViewport(0, 0, w, h);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(80.0, w /h, 0.1, 10000.0);
      
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        gluLookAt(100.0, -100.0, 200.0, 100.0, 300.0, 0.0, 0.0, 1, 0.0);
    
        
    def paintGL(self):
       
        #清除之前画面
        t0=time.time()
        
        glClear(GL_COLOR_BUFFER_BIT| GL_DEPTH_BUFFER_BIT)
        self.paintAgents()
        self.paintCellHatch()
       # self.paintAgents()
        glFinish()
        self.adjustSize()
  
        self.calcRefreshTime(time.time(),t0)
        print(time.time()-t0)#,time.time()-t2,t2-t1,t1-t0)


    def ChangeSize(w,h):
        global windowWidth,windowHeight
        if(h == 0):     #防止除数为0
            h = 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if (w <= h): 
            windowHeight = 250.0
            windowWidth = 250.0
        else: 
            windowWidth = 250.0
            windowHeight = 250.0
            
        # 设置修剪窗口
        glOrtho(0.0, windowWidth, 0.0, windowHeight, 1.0, -1.0)
     
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();


def simStart(sourceFile,modelClass,varList=[]):
    #timer = pg.QtCore.QTimer()
    modelClass.varList=varList
    app = pg.mkQApp()
    #modelClass.# 模型的源代码路径
    win=TakBaseWindow(sourceFile=sourceFile,modelClass=modelClass,varList=varList)

    win.show()

    app.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    print('hahaha')
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
