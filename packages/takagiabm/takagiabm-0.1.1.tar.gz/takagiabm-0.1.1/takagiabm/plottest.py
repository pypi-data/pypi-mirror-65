# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         1
# Description:  
# Author:       Administrator
# Date:         2018/5/28
#-------------------------------------------------------------------------------

import numpy as np
import pyqtgraph as pg
import threading
import time
app = pg.mkQApp()
from pyqtgraph.Qt import QtGui,QtCore
win = QtGui.QMainWindow()#GraphicsWindow()
##win.setWindowTitle(u'pyqtgraph plot demo')
win.resize(600, 400)

##p = win.addPlot()
##p.showGrid(x=True, y=True)
##p.setLabel(axis='left', text=u'Amplitude / V')
##p.setLabel(axis='bottom', text=u't / s')
##p.setTitle('y1=sin(x)  y2=cos(x)')
##p.addLegend()
##
##layer1 = p.plot(name='y1',pen='r')
##layer2 = p.plot( name='y2',pen='g')#,symbol='star')
##
##Fs = 1024.0 #采样频率
##N = 1024    #采样点数
##f0 = 5.0    #信号频率
##pha = 0     #初始相位
##t = np.arange(N) / Fs   #时间向量

view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
win.setCentralWidget(view)
win.show()
w2 = view.addViewBox()
s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen('w'),pxMode=True)
w2.addItem(s2)
def plotData():
    n=30
    
    
    pos = np.random.normal(size=(2,n), scale=1e-5)
    t0=time.time()
    f=open('/home/hzy/Documents/Development/python/calcs_noval/pyqtgraphtest/simu.py')
    co=f.read()
    f.close()
    
    loc=exec(co)
    print(loc)
    #spots = [{'pos': pos[:,i], 'data': 1, 'brush':pg.intColor(i, n), 'symbol': i%5, 'size': 5} for i in range(n)]
    print(time.time()-t0)
    s2.setData(locals()['spots'])
    

##    s2.sigClicked.connect(clicked)
t0=0
fps=0
def continousRefresh():
    global t0,fps

    plotData()
    fps+=1
    if(time.time()-t0>=1):
        
        t0=time.time()
#        print(fps)
        fps=0
##th=threading.Thread(target=continousRefresh)
##th.setDaemon(True)
##th.start()
timer = pg.QtCore.QTimer()
timer.timeout.connect(continousRefresh)
timer.start(0)

app.exec_()