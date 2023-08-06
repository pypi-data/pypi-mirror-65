import random
import time
import numpy as np
class Activator():
    def __init__(self,model):
        self.agentSet=model.agentSet
        
    def casualActivation(self,agentList):
        '''
        随意地激活,不是随机的.意思是将所有元素简单的按照哈希表的顺序激活.
        '''
##        agentList=list(self.agentList)
        
        for agent in agentList:
            agent.step()

    def randomActivation(self,agentList:list,activatePortion=1)->None:#activatePortion是指激活的agent所占的比例.
        t0=time.time()
        if(activatePortion<0-1e-9)|(activatePortion>1+1e-9):
            raise Exception("Invalid activatePortion.激活比例须在[0,1]闭区间以内.")
##        agentList=list(self.agentSet)
        agentNum=len(agentList)
        agentNumToActivate=int(agentNum*activatePortion)#选择要激活的个体数目.相当于是不放回的抽样.
        
        
        agentIndexArray=np.arange(agentNumToActivate)
        t1=time.time()
        np.random.shuffle(agentIndexArray)# 生成乱序数组
        t2=time.time()
        #print(agentIndexArray)
        for index in agentIndexArray:
##            l=len(agentList)# 求一下长度.
##
##            index=int(random.randint(0,l-1))
            agentList[index].step()
##            agentList.pop(index)
        t3=time.time()
##        for i in range(agentNumToActivate):
##            l=len(agentList)
##            index=int(random.randint(0,l-1))
##            agentList[index].step()
##            agentList.pop(index)
        print('ttt',time.time()-t0)

##agentSet=set()
##for i in range(100000):
##    agentSet.add(Agent.Agent())
##
##t0=time.time()
##randomActivation(agentSet,1)
##t1=time.time()
###casualActivation(agentSet)
##t2=time.time()
##l=list(agentSet)
##print(t1-t0,t2-t1)  
##
##count=0
##for item in l:
##    #print(item.stat)
##    if(item.stat!=True):
##        count+=1
##        #print("exc!!!")
##        
##print(count)        
    
    
