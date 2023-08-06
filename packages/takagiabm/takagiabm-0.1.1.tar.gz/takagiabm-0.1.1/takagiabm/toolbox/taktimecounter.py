import time

class TakTimeCount():
    def __init__(self,name:str):
        self.name=name
        self.lastTime=0
        self.updateTimes=0# 更新的次数
        self.timeCount=0
        self.running=False
    def start(self):
        
        self.lastTime=time.time()
        self.running=True
    def end(self,time):
##        if(self.running==False):
##            raise Exception('错误:定时器%s未启动'%(self.name))
        self.timeCount+=time-self.lastTime
        self.updateTimes+=1
        self.running=False
       # self.lastTime=time.time()
    def clear(self):
        self.updateTimes=0
        self.timeCount=0
##        self.running=False
        
    def __repr__(self):
        return '计时器名:%s调用:%d次,总共用时%.8f'%(self.name,self.updateTimes,self.timeCount)
    

class TakTimeCounter():# 计时器
    def __init__(self,model):
        self.functions={}
        self.timers={}
        self.model=None
    def timeIt(self,name,func,*args,**kw):
        t0=time.time()
        result=func(*args,**kw)   
        t1=time.time()
        if(name in self.functions.keys()):
            self.functions[name]+=t1-t0
        else:
            self.functions[name]=t1-t0
        return result
    def startTiming(self,timerName):
        if timerName in self.timers.keys():
            self.timers[timerName].start()
        else:
            self.timers[timerName]=TakTimeCount(timerName)
            self.timers[timerName].start()
    def endTiming(self,timerName,time):
##        if not timerName in self.timers.keys():
##            raise Exception('警告:endTiming之前未使用startTiming来启动计时器！')
        self.timers[timerName].end(time)
    def getTiming(self):
        return self.functions
    def flush(self):
        print('flushTimer:',self.timers)
        
        for k in self.timers.keys():
            self.timers[k].clear()
    def startTimer(self):
        pass
def hahahah(a,b,c):
    print(a,b,c)
    return 'das'
if __name__=="__main__":
    tc=TakTimeCounter()
    s=tc.timeIt(hahahah,1,2,3)
    print(hahahah)