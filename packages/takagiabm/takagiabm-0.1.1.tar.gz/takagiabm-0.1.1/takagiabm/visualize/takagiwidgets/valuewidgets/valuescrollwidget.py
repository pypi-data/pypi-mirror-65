'''
这个控件可以通过滑动来改变数值，进而改变行为模型参数。
'''
import sys
from PyQt5.QtWidgets import QScrollBar,QWidget,QLabel,QHBoxLayout\
,QApplication
from PyQt5.QtCore import Qt
class TakValueScrollWidget(QWidget):
    min=0
    max=1
    step=0
    name=''
    accuracy=2
    times=0
    variable=None
    def __init__(self,name='unnamed',min=0,max=100,value=20,step=1,var=None):
        super().__init__()
        self.name=name
        self.max=max
        self.min=min
        self.step=step
        self.initWidget()
        self.setValue(value)
        self.variable=var
    def setVariable(self,var):
        self.variable=var
    def reset(self,name='unnamed',min=0,max=100,value=20,step=1,var=None):
        self.name=name
        self.max=max
        self.min=min
        self.step=step
        self.setupWidgets()
        self.setValue(value)
        self.variable=var
    def setName(self,name:str)->None:
        if(type(name)==type('')):
            self.name=name
            self.nameLabel.setText(self.name)
        else:
            raise Exception("setName 方法必须输入字符串作为参数！ Method \"setName\" requires a string param.")
    def setupWidgets(self):
        self.scrollBar.setMaximum(int((self.max-self.min)/self.step))
        self.scrollBar.setMinimum(0)
        self.scrollBar.setMinimumWidth(100)
        self.nameLabel.setText(self.name)
        self.nameLabel.setMaximumWidth(100)
        self.valueLabel.setMaximumWidth(80)
        self.minShowLabel.setMaximumWidth(50)
        self.maxShowLabel.setMaximumWidth(50)
        self.minShowLabel.setText(str(self.min))
        self.maxShowLabel.setText(str(self.max))
        self.scrollBar.valueChanged.connect(self.updateValue) 
    def initWidget(self):
        layout=QHBoxLayout()
        self.scrollBar=QScrollBar(Qt.Horizontal)
        paramTmp=1/self.step

        self.nameLabel=QLabel(self.name)
        self.valueLabel=QLabel()
        self.minShowLabel=QLabel()
        self.maxShowLabel=QLabel(str(self.max))

        layout.addWidget(self.nameLabel)
        layout.addWidget(self.minShowLabel)
        layout.addWidget(self.scrollBar)
        layout.addWidget(self.maxShowLabel)
        layout.addWidget(self.valueLabel)
        
        self.setupWidgets()
        self.setLayout(layout) 
         
         
    def updateValue(self):
        v=self.scrollBar.value()
        val=v*self.step+self.min
        self.valueLabel.setText("%f"%(val))
##        print()
        if(self.variable!=None):
            self.variable.value=val
        
    def getValue(self):
        v=self.scrollBar.value()
        
        return v*self.step+self.min
    def setValue(self,value):
        self.scrollBar.setValue(int((value-self.min)/self.step))
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = TakValueScrollWidget("当前速度是",0,1001,407.1,0.3)
    ex.show()
    sys.exit(app.exec_())