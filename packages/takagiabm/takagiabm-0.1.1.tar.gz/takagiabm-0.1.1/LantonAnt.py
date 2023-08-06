from takagiabm.agent import GridAgent
from takagiabm.model import GridModel
import random
from takagiabm.visualize.mainwindow import simStart
from takagiabm.variable import Var
def agentSetup(model):
    global xspeed
    for i in range(1):
        a=GridAgent((45+i,45))
        a.speed[0]=1# 初始化速度.
        a.speed[1]=0
        model.addAgent(a)

def agentLoop(agent):# 代理人(也就是蚂蚁)执行的函数
    global xspeed
    color=agent.getCellColor()
#    print(color)
    if(color=='#ffffff'):
        agent.setCellColor('#000000')
        agent.turn('RIGHT')
    else:       
        agent.setCellColor('#ffffff')
        agent.turn('LEFT')
    agent.move()

GridAgent.step=agentLoop 
#每轮每个agent都要被访问到。
GridModel.initAgent=agentSetup   
if __name__=="__main__":
    GridModel.width=70  # 设置网格宽度
    GridModel.height=70 # 设置网格高度
    simStart(__file__,GridModel)  # 这个方法同时启动了图形界面。
