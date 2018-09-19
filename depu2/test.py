from read_pokerstar import analysisImg
from read_pokerstar import NeedAnalyse
from reader import getWaitingman
import time
from PIL import Image
import player as p
#import random


def bbb():
    ''' 测试 '''
    start =time.clock()
   
   
    file_name=r'tmp\dz_0918120940.png' 
    wholeimg=Image.open(file_name).convert('L')
    #要解析的图片，和后面一堆样本图片
    print(NeedAnalyse(wholeimg))
    rtSit=analysisImg(wholeimg)
    
    print(rtSit.todict())
    print(getWaitingman(rtSit))
    '''
    print('决策结果%s %s' % (p.makeDecision(rtSit)))
    #print('决策结果%s %s' % (p.makeTmpDecision(rtSit)))
    #for i in range(15):
    #    print(random.random())
    #计算运行时间
    '''
    end = time.clock()
    print('Running time: %s Seconds'%(end-start)) 

bbb()