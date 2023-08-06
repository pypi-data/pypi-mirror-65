import numpy as np
import time
from takagiabm.agent import GridAgent,BaseAgent
#from numba import jit
import sys
from itertools import chain

def xLoop(grid,pos):
    if( pos[0]<0):
        pos[0]=grid.width-1
    elif(pos[0]>=grid.width):
        pos[0]=0
    
def yLoop(grid,pos):
    if(pos[1]<0):
        pos[1]=grid.height-1
    elif(pos[1]>=grid.height):
        pos[1]=0
    
def xBlock(grid,pos):
    
    if( pos[0]<0):
        pos[0]=0
    elif(pos[0]>=grid.width):
        pos[0]=grid.width-1
    return pos
    
def yBlock(grid,pos):
    #print(pos)
    if(pos[1]<0):
        pos[1]=0
    elif(pos[1]>=grid.height):
        #print('dd',grid.height)
        pos[1]=grid.height-1 
    return pos
    #print(pos)  
    

class Cell(BaseAgent):
    def __init__(self,pos,grid=None,model=None,color='#ffffff'):
        super().__init__(model=model,pos=pos)
        self.model=model
        self.grid=grid
        self.properties['color']=color# self.properties这个词典继承自Agent基类.
        
    def step(self):
        pass
    def getNeighbors(self,shape=''):
        return self.grid.getNeighbors(self.pos,shape)
    def __repr__(self):
        return str(self.pos)
        

class Grid():
    def __init__(self,model=None,width=0,height=0):# 分别是表格的宽度和高度.
        self.model=model
        self.width=width   # 网格的宽度(列数)
        self.height=height # 网格的高度(行数)
        self.cellList=[[set() for i in range(width)] for j in range(height)]
        
        self.cells=[]*width
##        for i in range(self.height):
##            self.cells.append([None]*width)
##            for j in range(self.width):
##                self.cells[i][j]=Cell(pos=(j,i),grid=self,model=self.model)
##        for i in range(self.height):
##            for j in range(self.width):
##                print('pos',i,j,self.cells[i][j].pos)
        
        self.cells=[[Cell(pos=(i,j),grid=self,model=self.model) for i in range(width)] for j in range(height)]
        print('cells',self.cells)
        self.boundryPolicy={'x':'loop','y':'loop'}# 
        self.xPolicy=xBlock
        self.yPolicy=yBlock
        
        #self.cellUpdateList=[]
    def getCell(self,pos:np.ndarray):
        
        if type(pos)==type((1,2)):
            pos=np.array(pos)
        #pos=np.array(pos)
       # print('2',pos)
        pos=self.getCellPos(pos)
       # print('3fff',pos)
        c=self.cells[pos[1]][pos[0]]
       # print(4,c.pos)
        return c
    def getNeighbors(self,pos:tuple,shape:str)->list:
        #print('neighbors',pos)
        if(str=='+'):# 上,下,左,右
            l= [self.getCell((pos[0],pos[1]+1)),self.getCell((pos[0],pos[1]-1)),
                    self.getCell((pos[0]-1,pos[1])),self.getCell((pos[0]+1,pos[1]))]
        elif(str=='-'):
            l=[]
        elif(str=='x'):# 右上,左上,左下,右下
            l=[self.getCell((pos[0]+1,pos[1]+1)),self.getCell((pos[0]-1,pos[1]+1)),
                    self.getCell((pos[0]-1,pos[1]-1)),self.getCell((pos[0]+1,pos[1]+1))]
        elif(str=='->'):
            l=[]
        else:
            l=[self.getCell((pos[0]+1,pos[1])),self.getCell((pos[0]+1,pos[1]+1)),# 右,右上
               self.getCell((pos[0],pos[1]+1)), self.getCell((pos[0]-1,pos[1]+1)),# 上,左上
               self.getCell((pos[0]-1,pos[1])),self.getCell((pos[0]-1,pos[1]-1)),# 左,左下
               self.getCell((pos[0],pos[1]-1)),self.getCell((pos[0]+1,pos[1]-1))]# 下,右下、
            
        return list(set(l))# 去重
    def getCellPos(self,pos:np.ndarray):
        #print(pos)
        #self.model.startTiming('getCellPos')
        pos=self.xPolicy(self,pos)
        pos=self.yPolicy(self,pos)
        #print('dd',pos)
    
##        if(self.boundryPolicy['x']=='loop'):
##            if( pos[0]<0):
##                pos=(self.width-1,pos[1])
##            elif(pos[0]>=self.width):
##                pos=(0,pos[1])
##        elif self.boundryPolicy['x']=='block':
##            if( pos[0]<0):
##                pos=(self.width-1,pos[1])
##            elif(pos[0]>=self.width):
##                pos=(0,pos[1])
##        elif self.boundryPolicy['x']=='none':
##            if( pos[0]<0)|(pos[0]>=self.width):
##                raise Exception("索引%s位于网格之外.网格宽度为%d,高度为%d"%(
##                str(pos),self.width,self.height))
##            
##        else:
##            raise Exception('x边界策略值%s无效值.有效策略为loop,block以及none三种.'%(self.boundryPolicy['y'])) 
##        
##        if(self.boundryPolicy['y']=='loop'):
##            if(pos[1]<0):
##                pos=(pos[0],self.height-1)
##            elif(pos[1]>=self.height):
##                pos=(pos[0],0) 
##        elif(self.boundryPolicy['y']=='block'):
##            if(pos[1]<0):
##                pos=(pos[0],0)
##            elif(pos[1]>=self.height):
##                pos=(pos[0],self.height-1)
##        elif(self.boundryPolicy['y']=='none'):
##            if( pos[0]<0)|(pos[0]>=self.width):
##                raise Exception("索引%s位于网格之外.网格宽度为%d,高度为%d"%(
##                str(pos),self.width,self.height))
##        else:
##            raise Exception('y边界策略值%s为无效值.有效策略为loop,block以及none三种.'%(self.boundryPolicy['y']))   
        #self.model.endTiming('getCellPos')
        
        return pos
  
    def getAllCellsIter(self):#iterator:
        iterChain=chain.from_iterable(self.cells)#(*self.cells),返回一个迭代器.

        return iterChain
    def getAllCells(self)->list:
        return list(self.getAllCellsIter())
    def getCellColor(self,pos:tuple)->str:
        return self.cells[pos[1]][pos[0]].getColor()
        
    def getCellColorTupleF(self,pos=None)->tuple:# pos或者wh的输入都是tuple
        if(pos!=None):
            value=self.cells[pos[1]][pos[0]].getColor()
        elif(rc!=None):
            value=self.cells[rc[0]][rc[1]].getColor()
        else:
            raise Exception("必须选定以位置pos=(x:int,y:int)之一作为索引。")
        
        digit = list(map(str, range(10))) + list("abcdef")
        value=value.lower()
        a1 = (digit.index(value[1]) * 16 + digit.index(value[2]))/256.0
        a2 = (digit.index(value[3]) * 16 + digit.index(value[4]))/256.0
        a3 = (digit.index(value[5]) * 16 + digit.index(value[6]))/256.0
        return (a1, a2, a3)
        
    def setCellColor(self,pos:tuple,color:str)->None:
        #print(pos)
        cell=self.cells[pos[1]][pos[0]]# 先行后列,逐个定位.
        cell.setColor(color)
        #self.cellUpdateList.append(cell)
        
    def placeAgent(self,agent)->None:
        #self.agentSet.add(agent)
        pos=agent.pos
        agent.grid=self
       
        self.cellList[pos[0]][pos[1]].add(agent)
        
    def moveAgent(self,agent,deltaPos=(0,0)):
        lastPos=agent.pos
        #self.cellList[lastPos[0]][lastPos[1]].remove(agent)
        pos=(deltaPos[0]+lastPos[0],deltaPos[1]+lastPos[1])
        self.moveAgentTo(agent,pos)
        #agent.pos=pos
        #print(pos)
        #self.cellList[pos[0]][pos[1]].add(agent)
        
    
    def moveAgentTo(self,agent,targetPos=(0,0)):
        targetPos=self.getCellPos(targetPos)
##        if ( not 0<=targetPos[0]<self.width) or ( not 0<=targetPos[1]<self.height):
##            if 0:
##                raise Exception("索引%s位于网格之外.网格宽度为%d,高度为%d"%(
##                str(targetPos),self.width,self.height))
##            else:
##                if( targetPos[0]<0):
##                    targetPos=(self.width-1,targetPos[1])
##                elif(targetPos[0]>=self.width):
##                    targetPos=(0,targetPos[1])
##                if(targetPos[1]<0):
##                    targetPos=(targetPos[0],self.height-1)
##                elif(targetPos[1]>=self.height):
##                    targetPos=(targetPos[0],0)                 

        lastPos=agent.pos
        #print('agentPos',agent.pos)
        self.cellList[lastPos[1]][lastPos[0]].remove(agent)# 索引是先行后列，但是位置是先列（x）后行(y)
        agent.pos=targetPos
        self.cellList[targetPos[1]][targetPos[0]].add(agent)
        
    def isCellEmpty(self,pos):
        return self.getAgentNumInCell(pos)==0
        
    def getAgentNumInCell(self,pos):# 输入位置,返回单元格内对象的数目.
        return len(self.cellList[pos[0]][pos[1]])
        
    def getAgentsByPos(self,pos):
        return list(self.cellList[pos[0]][pos[1]])
        
    def removeAgent(self,agent):
        #self.agentSet.remove(agent)
        pos=agent.pos
        self.cellList[pos[0]][pos[1]].remove(agent)
        #print(sys.getrefcount(agent))

if __name__=='__main__':
    g=Grid(width=7,height=7)
    s=g.getCell(np.array((1,2)))
    print('posfffff',s.pos)
    print(s.getNeighbors())
    print(Cell(pos=(2,2)).pos)
    print(g.getCellPos(np.array((1,2))))
##    a=GridA#gent() 
##    g.placeAgent(a,(0,0))
##
##    t0=time.time()
##    for i in range(10000):
##        #pass
##        #g.moveAgentTo(a,(0,1))
##    ##time.sleep(1)
##    ##print(g.cellList)
##        a.moveTo((0,1))
##        a.moveTo((0,0))
##        #g.moveAgentTo(a,(0,0))
##    #g.rmoveAgent(a)
##    print(g.getAgentNumInCell((0,0)))
##    print(g.getAgentsByPos((0,0)))
##    print(time.time()-t0)
    #print(g.cellList)
