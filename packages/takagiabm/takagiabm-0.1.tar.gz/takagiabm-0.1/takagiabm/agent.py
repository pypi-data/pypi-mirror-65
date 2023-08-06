import numpy as np
rotMat=np.array([[0,-1],[1,0]])



class BaseAgent():
    pos=np.array([0,0])
    model=None
    def __init__(self,pos,model=None):
        self.pos=self.initPos(pos)
        self.marker='o'
        self.master=None
        self.model=model
        #self.color="#ffff00"
        self.properties={'color':'#000000'}
        #self.stat=False
    def step(self)->None:
        #self.stat=True
        pass
    def setColor(self,color:str)->None:
        
        self.properties['color']=color
    def getColor(self)->str:
        return self.properties['color']  
        
    def setProperty(self,propertyName:str,property):
        if(type(propertyName)!=type('')):
            raise Exception(\
                '警告:agent或者cell的属性只能以字符串命名.你输入的是%s'%(repr(prop)))
        self.properties[propertyName]=property
    def setTraitLater(self,propertyName:str,property):
##        print('hahahah')
        self.setPropertyLater(propertyName,property)
    def setPropertyLater(self,propertyName:str,property):# 待到下次访问的时候再设置.
##        if(property==True):
##            print('haaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
##        print('a')
        self.model.agentUpdateList.append((self,propertyName,property))
        #self.properties[propertyName]=property
    def setTrait(self,traitName,trait):
        self.setProperty(traitName,trait)
    def getProperty(self,propertyName:str):# ->返回一个任何类型.
        return self.properties[propertyName]
    def getTrait(self,traitName:str):# ->返回一个任何类型.
        return self.getProperty(traitName)
    def initPos(self,pos):
        return np.array([pos[0],pos[1]])
    def setPos(self,pos):
        self.pos[0]=pos[0]
        self.pos[1]=pos[1]
    #    print('init',self.pos)
    
class GridAgent(BaseAgent):
    '''
    在Grid上运动的Agent
    '''
    def __init__(self,pos:tuple,model=None,color='#ffffff'):
        super().__init__(model=model,pos=pos)
##        self.pos=self.setPos(pos)
        self.grid=None
        self.stat=0
        self.properties['color']=color
        self.markerDic={}
        self.speed=np.array([0,0])

    def getCellColor(self)->str:
        return self.grid.getCellColor(self.pos)
    def turn(self,dir:str):
        global rotMat
        if(dir=='LEFT'):
            self.speed=np.dot(rotMat,self.speed.T).T
        elif(dir=='RIGHT'):
            self.speed=-np.dot(rotMat,self.speed.T).T
    def setCellColor(self,color:str)->None:
        '''
        设置当前Agent所在的单元格的颜色.
        '''
        self.grid.setCellColor(self.pos,color)
        pass
    def setMarker(self,status,marker)->None:
        self.markerDic[status]=marker
    def setMarkers(self,markerDic:dict)->None:
        self.markerDic=markerDic
    def getMarkerDic(self)->dict:
        return self.markerDic
    def getMarker(self,status):
        if(status not in self.markerDic.keys()):
            raise KeyError('状态%s在属性字典中不存在.'%status)
        return self.markerDic[status]
    def stop(self)->None:
        '''
        主要作用是将此个体的速度置零。
        '''
        self.move((0,0))
    def move(self,deltaPos=None)->None:
        '''
        将Agent移动一个相对位置deltaPos.比如等于(1,-1)的时候为向右平移1格,下平移1格.
        并且会将速度改写为np.ndarray([1,1]).
        当没有参数输入时,将使得Agent按照其speed移动.
        
        '''
        
        
        if(deltaPos!=None):
            self.grid.moveAgent(self,deltaPos)
            self.speed[0]=deltaPos[0]
            self.speed[1]=deltaPos[1]
        else:
            self.grid.moveAgent(self,(self.speed[0],self.speed[1]))
            
    def moveTo(self,pos:tuple)->None:
        '''
        将Agent移动到某个单元格,以tuple表示.
        '''
        self.speed[0]=pos[0]-self.pos[0]
        self.speed[1]=pos[1]-self.pos[1]
        self.grid.moveAgentTo(self,pos)
    def getAgents(self)->list:
        '''
        返回此Agent所在的单元格中所有Agent的列表.
        '''
        if(self.grid==None):
            raise Exception('当前Agent对象不属于任何Grid网格对象！')
        self.getAgentsByPos(self.pos)
    def getAgentsByPos(self,pos:tuple)->BaseAgent:
        return self.grid.getAgentsByPos(pos)
    def setGrid(self,grid)->None:
        self.grid=grid
    def getGrid(self,grid):
        '''
        返回一个Grid对象
        '''
        return self.grid
    def step(self):
        self.stat+=1
    def __iter__(self):
        
        return iter([self.pos,self.color])
    def __repr__(self):
        return "cor:%s,v:%s,color:%s"%(str(self.pos),str(self.speed),self.getColor())
        
        
    
        
def main():
    a=GridAgent((0,0))
    a.speed[0]=1
    a.speed[1]=-1
    a.turn('RIGHT')
    #print(a.speed)
    pass

if __name__ == "__main__":
    main()
