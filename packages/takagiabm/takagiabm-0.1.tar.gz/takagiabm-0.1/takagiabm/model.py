from takagiabm.grid import Grid
from takagiabm.datacollector import DataCollector
from takagiabm.agent import GridAgent
from takagiabm.activation import Activator
import time
from takagiabm import TakTimeCounter
class BaseModel():
    def __init__(self):
        self.agentSet=set()
        self.currentStep=0
        self.agentUpdateList=[]# 这是用来在执行结束之后再刷新的列表.
        self.dataCollector=DataCollector(self)
        self.activator=Activator(self)
        self.timeCounter=TakTimeCounter(self)
    def startTiming(self,timerName):
        
        self.timeCounter.startTiming(timerName)
    def endTiming(self,timerName):
        
        self.timeCounter.endTiming(timerName,time.time())
    def addAgent(self,agent):
        self.agentSet.add(agent)
    def removeAgent(self,agent):
        self.agentSet.remove(agent)
    def stepRoutine(func):
        '''
        每一次step发生时都要发生一遍的事情,作为装饰器.
        '''
        def wrapper(self,*args,**kwargs):
            self.currentStep+=1
            return func(self,*args,**kwargs)
        return wrapper
        
    @stepRoutine
    def step(self):
        pass
  


class GridModel(BaseModel):
    stepRoutine=BaseModel.stepRoutine# 先把step的时候的数据记录下来再说.
    width=0
    height=0
    lastStep=0# 用于测速的变量，记录上一次的速度。
    def __init__(self):
        super().__init__()
        self.currentStep=0
        
        self.grid=Grid(model=self,width=self.width,height=self.height)

        self.initAgent()
        
    def timeIt(self,func,*args,**kwargs):
        return self.timeCounter.timeIt(func,*args,**kwargs)

        
    def setProperties(self):
        pass
    def initAgents(self):
        pass
    def getAllAgentAsPGScatters(self):    
        import pyqtgraph as pg
        '''
        获取全部的散点的位置坐标和形状.
        '''
        agentList=list(self.agentSet)
        l=len(agentList)
        spots = [{'pos': agentList[i].pos, 'data': 1, 'brush':pg.intColor(i, l), 
                  'symbol': 's', 'size':10 } for i in range(l)]
        return spots
    def agentsUpdateProperties(self):# 清理UpdateLater生成的列表
        print('***'*30,len(self.agentUpdateList))
        for agent,propertyName,property in self.agentUpdateList:
            agent.properties[propertyName]=property
            #print(propertyName,property)
        
        self.agentUpdateList=[]
    def collectData(self,property:str)->None:
        pass
    def addAgent(self,agent):
        self.agentSet.add(agent)
        self.grid.placeAgent(agent)
        
    def removeAgent(self,agent):
        self.agentSet.remove(agent)
        self.grid.removeAgent()
        
    @stepRoutine
    def step(self):
        
        self.activator.randomActivation(list(self.agentSet),1)
        t0=time.time()
        l=list(self.grid.getAllCells())
        t1=time.time()
        self.activator.randomActivation(l)# 可否使用迭代器？
        t2=time.time()
        print('time.time',t2-t0,t2-t1)
        self.agentsUpdateProperties()
        #self.dataCollector.collect('stat')
        d=self.dataCollector.collectProperty(self.grid.getAllCellsIter(),'color')
        print(d)
        
        self.timeCounter.flush()
        
##        for i in self.grid.cells:
##            for j in i:
##                print(j.properties['alive'],end=' ')
##            print('\n')
##        pass

