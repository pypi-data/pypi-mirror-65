# task_master.py

import random, time, queue
from multiprocessing.managers import BaseManager
import pyqtgraph as pg
import numpy as np
import threading
# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('localhost', 5000), authkey=b'abc')
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()
# 放几个任务进去:


execStat=True

def getResult():
    global execStat
    while(1):
        print('ddd',execStat)
        try:
            
            r = result.get(timeout=5)
        except Exception as e:
            execStat=False
            print(e)
            
th=threading.Thread(target=getResult)
th.setDaemon(True)
th.start()

while(1):
##    n = random.randint(0, 10000)
##    print('Put task %d...' % n)
    n=3000
    pos = np.random.normal(size=(2,n), scale=1)
    spots = [{'pos': pos[:,i], 'data': 1,
           'brush':pg.intColor(i, n), 'symbol': i%5, 'size': 5} for i in range(n)]
    
    size=task.qsize()
    if(size>=10):
        time.sleep(0.0001)
    else:
        task.put(spots)
    print(execStat)
    if(execStat==False):
        break
# 从result队列读取结果:##print('Try get results...')
##for i in range(10):
##    r = result.get(timeout=10)
##    print('Result: %s' % r)
### 关闭:
##manager.shutdown()
##print('master exit.')
