from read_pokerstar import analysisImg
from read_pokerstar import NeedAnalyse
from reader import getWaitingman
from reader import calcuWinrate
from reader import calcuWinrateNoWeight
from reader import calcuNumRate
import time
from PIL import Image
import player as p
#import random
from Harrington import IsSameHand
from Harrington import DontLikeRate
from Harrington import MyTurn
from reader import LastManAfterFlop
from preFlop import IsOpenRange
from preFlop import IsFirst

def bbb():
    ''' 测试 '''
    start =time.clock()
   
   
    file_name=r'tmp\dz_0203003309.png' 
    wholeimg=Image.open(file_name).convert('L')
    #要解析的图片，和后面一堆样本图片
    #print(NeedAnalyse(wholeimg))
    rtSit=analysisImg(wholeimg,0.02)
    
    #入库
    print(rtSit.todict())
    
    #判断在我之前的人是否都弃牌
    print(IsFirst(rtSit))
    print(IsOpenRange(rtSit))
    #print(MyTurn(rtSit))
    
    #winrate=calcuWinrateNoWeight(rtSit)
    
    #print('胜率'+str(winrate[0])+','+str(winrate[1]))
    #print('不喜欢率%s , %s' % DontLikeRate(rtSit,winrate))
    #print('翻后最后一个行动的人的位置:'+str(LastManAfterFlop(rtSit)))
    print('决策结果%s %s' % (p.makeDecision(rtSit)))
    '''
    file_name=r'tmp\dz_0924103508.png' 
    wholeimg=Image.open(file_name).convert('L')
    #要解析的图片，和后面一堆样本图片
    #print(NeedAnalyse(wholeimg))
    rtSit2=analysisImg(wholeimg,0.02)
    
    print(rtSit2.todict())
    #print(getWaitingman(rtSit))
    print(IsSameHand(rtSit,rtSit2))
    
    #
    #print('决策结果%s %s' % (p.makeTmpDecision(rtSit)))
    #for i in range(15):
    #    print(random.random())
    #计算运行时间
    '''
    end = time.clock()
    print('Running time: %s Seconds'%(end-start)) 

bbb()