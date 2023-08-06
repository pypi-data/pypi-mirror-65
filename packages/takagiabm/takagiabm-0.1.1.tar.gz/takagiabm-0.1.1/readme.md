# Python的基于主体建模的仿真库——TakagiABM ！


## 简介：
由于Netlogo的语法本人有点不太喜欢，所以为完成网络仿真的作业，本人便重新编写了一个ABD仿真的代码，参考了Netlogo的架构以及一些类似Python 仿真库的API写法。

### 安装方式：
```bash
 pip install takagiabm
```
如果有类似报错：
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
ERROR: Could not find a version that satisfies the requirement takagiabm (from versions: none)
ERROR: No matching distribution found for takagiabm

说明国内源可能还没有完成同步。不过，这个库只有几十kb大小，暂时换用官方源也无妨：
尝试：
```bash
pip install takagiabm -i https://pypi.org/simple
```
当然它依赖的numpy,pyqt5之类的几十MB的大包，还是先用国内源安装好吧。
### 版本及依赖包：
python3及以上版本，且确保支持以下库：
#### 仅仿真逻辑：
numpy
#### 需要界面可视化时：
numpy  
pyopengl  
pyqt5  
pyqtgraph  

注意，当启动图形界面时，不支持PyPy，盖因PyPy不支持PyQt、PyOpenGL。

可以直接将全项目以zip下载下来，或是克隆下来之后直接运行根目录下的simu.py文件。

### 示例及使用方式介绍

安装依赖包以后，在下载的TakagiABM解压出的TakagiABM文件夹根目录下运行命令：
```bash
python LantonAnt.py
```

界面启动以后，就可以看到一个兰顿蚂蚁模型,红点是蚂蚁，白色就是白色的方格，如图所示：

![ant](src/兰顿蚂蚁.png)
界面左侧显示的是当前所有在界面上移动的代理人的各种信息，比如位置等。对于这个实验，只有一个代理人，就是这只小蚂蚁；和下方的文本栏目暂时无效果。
#### 开始仿真
点击左上角“开始”，拖动滑块即可调整仿真速度。点击以后此按钮文字变为”暂停“. 
点击“重启”，重置仿真。此时仿真文件中的设置项将被重新加载。如果在重启之前修改代码，那么下一次仿真就可以按照此次的设置执行。也就是说，**代码文件支持动态修改**，对于小修小改，无需重新启动图形界面。但是推荐将仿真的相关内容都写在同一个文件里面。
点击“暂停“，可以暂停仿真。此时”暂停“的文字变为”继续“。点击”继续“的时候，仿真继续执行。  
点击”单步“，可以进行单步仿真。  

同样可以进行其他仿真，比如下面的生命游戏（GameOfLife.py中）

![src](src/生命游戏.png)

#### 各项指标的含义
当前步代表当前仿真进行的步数；  

设定步速是滑动条控制的步速；  

实际帧率是显示刷新的实际频率；  

实际步速是模型仿真每秒走过的步数。   

由于模型可以仿真多步刷新一次，所以当设定步速高于最大刷新率（根据网格的大小而定，对于34*34的网格，最大刷新速率大约为55fps）时，模型步速将高于实际帧率。


## 简易教程：
打开兰顿蚂蚁的代码，发现以下内容：
```python
from takagiabm.agent import GridAgent
from takagiabm.model import GridModel
import random
from takagiabm.visualize.mainwindow import simStart
from takagiabm.variable import Var
def agentSetup(model):
    global xspeed
    for i in range(1):
        a=GridAgent((45,45))#放置于单元格x=45,y=45
        a.speed[0]=1# 初始化速度，vx=1,vy=0。
        a.speed[1]=0
        model.addAgent(a)

def agentLoop(agent):# 代理人(也就是蚂蚁)执行的函数。每轮每个agent都要被访问到。
    global xspeed
    color=agent.getCellColor()
    print(color)
    if(color=='#ffffff'):
        agent.setCellColor('#000000')
        agent.turn('RIGHT')
    else:       
        agent.setCellColor('#ffffff')
        agent.turn('LEFT')
    agent.move()

GridAgent.step=agentLoop 

GridModel.initAgent=agentSetup   
if __name__=="__main__":
    GridModel.width=70  # 设置网格宽度
    GridModel.height=70 # 设置网格高度
    simStart(__file__,GridModel)  # 这个方法同时启动了图形界面。

```
仿真的控制是由仿真模型对象GridModel来完成的。它每走一步，称为仿真前进一步。仿真每前进一步，所有的agent都会被激活一次，也就是调用一下step。

## API&接口教程
### 简介
TakagiABM库参考了NetLogo，主体一共有agent（代理人）、cell（网格单元）、observer(观察者)三类，分别对应于NetLogo的turtle、patch和observer。

三者都继承自BaseAgent这一类。下面请看接口API:

### Agent
#### BaseAgent()
基类.
##### 属性：
###### self.pos:tuple
为当前的x,y坐标。目前要求为两个整数。
###### self.properties：dict
用于保存自身属性的变量,这是一个词典。但是不推荐直接使用索引的方式取得其中的元素，因为这样就会绕过代码中的类型检查，容易出现越界等情况。

BaseAgent有一个'color'键是默认初始化的，初始化时默认为白色，类型为字符串。形如"#ffffff"。     
例如“#ff0000”代表正红色，“#00ff00”代表正绿色，“#0000ff”代表正蓝色

##### def setColor(self,color:str)->None:
将自身的颜色设置为此字符串类型。
#####     def getColor(self)->str:
返回一个十六进制颜色字符串形如“#aaaaaa”
##### setProperty(self,propertyName:str,property:object)->None:
设置自身的属性，立即生效。用法在self.getProperty中一并示出。
##### setPropertyLater(self,propertyName,property:object)->None:
也是设置自身的属性，入口参数同self.setProperty。在仿真过程中调用这个函数时，在整个仿真程序的当前步中，当所有代理人各自刷新时，若调用此函数设置属性，此BaseAgent的属性将暂时不变，等到模型此步调用完所有的代理人以后，再更新属性。

这个方法的用处不妨举例说明：对于生命游戏等等场合的仿真，如果每个代理人在被调用时都立即更新自己是否存活，那么其周围尚未更新的代理人，相邻的生命数量都会被改变，造成仿真结果完全错误。如果在模型该步调用好所有代理人之后再更新属性，就能避免这个错误的发生。

不妨在生命游戏例程GameOfLife中尝试一下将这个函数(或者是setTraitLater)换成setProperty/setTrait，以体会其差别。

##### getProperty(self,propertyName:str)->object:
获取自身的属性。
：(略去了BaseAgent初始化时的输入参数)：
```python
baseAgent=BaseAgent()
baseAgent.setProperty('alive',123)
print(baseAgent.getProperty('alive'))
# 运行结果：123
```
##### setTrait(self,traitName:str,trait:object)->None:
与setProperty的用法相同。之所以封装一下，是因为trait差不多是有“属性”这个意思的单词中最简短易拼写的，能少打一半字母（尽管从英语角度来看不太严谨。）
##### getTrait(self,traitName:str)->object:
同getProperty。

##### setTraitLater(self,traitName:str,trait:object)
同setPropertyLater.


#### GridAgent(BaseAgent)

这是用于网格上的Agent类。目前只有这一类可以使用（当然了，NetLogo最多的用途也是在网格上）。
##### 属性：

###### self.speed:numpy.ndarray([x:int,y:int])
是此Agent的速度。分别是x方向和y方向的分量。由于需要旋转操作，需要计算矩阵乘法，所以使用numpy.ndarray来加快运算速度。
注：numpy.ndarray这个叫法可能比较陌生，但它就是大名鼎鼎的np.array()、np.zeros()之类的函数所返回的numpy矩阵类型。
###### self.pos:tuple (x:int,y:int)
是此Agent当前的位置。
##### __init__(self,pos=(x：int,y:int))
初始化一个Agent，设定其位于x,y。必须输入整数，否则报错。
#####  getCellHatchColor（self）->str:
获取当前所在单元格的颜色。返回一个十六进制颜色字符串
#####  setCellHatchColor（self,color:str）->None
设置当前所在单元格的颜色。

##### move(self，deltaPos:(x:int,y:int))->None:
移动相对位置横向x格，纵向y格。如果出界，则会从网格对侧再次进入。
##### moveTo(self，pos:(x:int,y:int))->None:
移动到网格上的绝对位置：横向第x-1格，索引为x，纵向第y-1格，索引为y（因为索引是从0开始的！）。如果出界，则会从网格对侧再次进入。
##### stop(self)->None:
将速度置为0
##### step(self)->None:
此Agent的动作函数。每一个周期内，所有的Agent都会被激活一次。
##### getAgents(self)->[Agent(),Agent(),...]
获取此Agent当前单元格的其他Agent（），返回Agent的列表，<u>注意：此列表包括当前的Agent.</u>
##### getAgentsByPos(self,pos:(x,y))->[Agent(),Agent(),...]
返回pos位置的单元格中全部Agent的列表。<u>注意：此列表与getAgents的返回值类似，也包括当前的Agent</u>。
### Cell
#### class Cell（BaseAgent):
##### 属性：
与其继承的BaseAgent相比，暂时无新的属性。请参阅BaseAgent。
##### def getNeighbors(self,shape=""):
获取此单元格邻近的所有cell。shape可以输入不同参数，列举如下：
1、shape='+' ,返回上下左右四个单元格。
2、shape='x' (是一个小写的第24个英文字母x，不是乘号)，返回对角的四个单元格，亦即左上、左下、右上、右下。
3、什么参数都不输入，或者输入其他字符串：获取邻接的八个单元格。在生命游戏中用到的就是这个。

### Observer
等待添加……








