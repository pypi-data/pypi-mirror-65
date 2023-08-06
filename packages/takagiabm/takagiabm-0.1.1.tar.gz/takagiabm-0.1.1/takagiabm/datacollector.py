import time
class DataCollector():
    def __init__(self,model):
        self.model=model
##        if(type(attr)!=type('')):
##            raise TypeError('采集的属性必须以字符串表示！')
##        self.attrToCollect=attr
        pass
    def defaultCollect(self):
        return
    def collectAttr(self,agentList:list,attr=None)->dict:
##        agentList=list(agentSet)
        propertyDic={}
        
        for agent in agentList:
            #print(attr)
            a=getattr(agent,attr)
            if a in propertyDic.keys():
                propertyDic[a]+=1
            else:
                propertyDic[a]=1
            
        return propertyDic
    def collectProperty(self,agentList:list,property:str)->dict:
        t=time.time()
        propertyDic={}
        
        for agent in agentList:
            #print(attr)
            a=agent.getProperty(property)#getattr(agent,attr)
            if a in propertyDic.keys():
                propertyDic[a]+=1
            else:
                propertyDic[a]=1
        print('aaaa',time.time()-t)
        return propertyDic