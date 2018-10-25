#import time
import dealer
import math
import random
#import readpot

from reader import getPubList
from reader import getPubnum
from reader import getSurvivor
from reader import getMyHand
from reader import calcuWinrate
from reader import getWaitingman
from dealer import IsFlush
from reader import IsAllIn
from reader import IsAfter
from Harrington import DontLikeRate
from Moshman import flopDecision
from Harrington import MyTurn



#新写一个翻前决策
#2018-10-22 翻前决策重新写，无比重视紧和位置
def beforeFlopDecision(Sit,callchip):
    myhand=getMyHand(Sit)
    leftman=getSurvivor(Sit)[1]
    pubcnt=getPubnum(Sit)
    print('还剩%s个人' % leftman)
    if(pubcnt==0 and len(myhand)==2):
        #如果前面没有人加注
        if(callchip==Sit.bb and Sit.betlist[Sit.myseat]<=0):
            #如果是UTG
            if (Sit.position-Sit.myseat)%6==3:
                print('UTG')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                if(InStealRange(myhand)):
                    return (0,0)
            #如果是MP
            if (Sit.position-Sit.myseat)%6==2:
                print('MP')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                if(InStealRange(myhand)):
                    return (0,0)
            #如果是CO
            if (Sit.position-Sit.myseat)%6==1:
                print('CO')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                if(InTryRange(myhand)):
                    return (3,2)
            #如果是BTN
            if (Sit.position-Sit.myseat)%6==0:
                print('BTN')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                if(InTryRange(myhand)):
                    return (3,2)
                if QuiteGood(myhand) and leftman==3:
                    return (3,2)
                if leftman==3: return (3,2)
                else: return (0,0)
        if callchip<Sit.bb :
            #如果是小盲
            if callchip==Sit.bb/2:
                if leftman==2 and (Sit.myseat-Sit.position)%6==1:
                    print('小盲单挑大盲')
                    if InSuperRange(myhand): 
                        return (3,2)
                    if InOpenRange(myhand):
                        return (3,2)
                    if InTryRange(myhand):
                        return (3,2)
                    if QuiteGood(myhand):
                        return (3,2)
                    return (0,0)
                if leftman>2 and (Sit.myseat-Sit.position)%6==1:
                    print('小盲可以溜入')
                    if InSuperRange(myhand): 
                        return (3,3)
                    if InOpenRange(myhand):
                        return (3,3)
                    if InTryRange(myhand):
                        return (2,0)
                
                #print('小盲默认要偷')
                #return (3,0)
            #如果是大盲，只剩2个人，不发起攻击，碰运气
            if callchip==0 and leftman==2 and (Sit.myseat-Sit.position)%6==2:
                print('大盲')
                if InSuperRange(myhand):
                    return (3,3)
                if MyTurn(Sit)==2:
                    if InOpenRange(myhand):  
                        return (3,2)
                    if InStealRange(myhand): 
                        return (3,2)
                    if InTryRange(myhand):
                        return (3,2)
                    if QuiteGood(myhand):
                        return (3,2)
                if MyTurn(Sit)==1:
                    if InOpenRange(myhand):  
                        return (2,0)
                    if InTryRange(myhand): 
                        return (2,0)
                
        
        #如果有人加注了，但还不是很大
        if callchip>=Sit.bb and callchip<=6*Sit.bb:
            if (Sit.position-Sit.myseat)%6==3 :
                print('UTG跟加注')
                if InSuperRange(myhand): return (3,3)
                if InOpenRange(myhand): return (0,0)
                #if leftman>=3 and InTryRange(myhand): return (2,0)
                return (0,0)
            if (Sit.position-Sit.myseat)%6==2 :
                print('MP跟加注')
                if leftman>=5:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (3,4)
                    return (0,0)
                if leftman<5 and leftman>2:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (3,4)
                    return (0,0)
                if leftman==2:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (3,4)
                    return (0,0)
            if (Sit.position-Sit.myseat)%6==1:
                print('CO跟加注')
                if leftman>=5:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (3,4)
                    #if InTryRange(myhand): return (2,0)
                    return (0,0)
                if leftman==4:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (3,4)
                    #if InTryRange(myhand): return (2,0)
                    return (0,0)
                if leftman==3:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (3,4)
                    #if InTryRange(myhand): return (2,0)
                    return (0,0)
                if leftman==2:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (3,4)
                    return (0,0)
            #按钮位，跟加注
            if (Sit.position-Sit.myseat)%6==0 and Sit.betlist[Sit.myseat]>0:
                print('btn跟加注')
                if leftman<=6 and leftman>=2:
                    if InSuperRange(myhand): return (3,3)
                    if InOpenRange(myhand): return (2,0)
                    if InStealRange(myhand): return (2,0)
                    if InTryRange(myhand): return (2,0)
                    return (2,0)
            #小盲位跟加注
            if (Sit.myseat-Sit.position)%6==1:
                print('小盲跟加注')
                if InSuperRange(myhand): return (3,4)
                if InOpenRange(myhand): return (3,4)
                
                
            #大盲位跟加注
            if (Sit.myseat-Sit.position)%6==2:
                print('大盲位跟加注')
                if InSuperRange(myhand): return (3,4)
                if InOpenRange(myhand): 
                    if leftman<=2 and MyTurn(Sit)==1: return (3,3)
                    else: return (2,0)
                if leftman==2:
                    if QuiteGood(myhand): 
                        if MyTurn(Sit)==2 and Sit.potsize/Sit.callchip>=3: 
                            print('对抗小盲有位置优势')
                            return (2,0)
                    elif InTryRange(myhand):
                        print('对抗一个玩家，保卫盲注')
                        return (2,0)
                #这个也是测试用的，不一定好
                if InTryRange(myhand) and leftman>=2: 
                    print('底池赔率还行，进去试试')
                    return (0,0)
        if callchip>=6*Sit.bb and callchip<10*Sit.bb:
            if InSuperRange(myhand): return (3,4)
            if leftman==2 and MyTurn(Sit)==2 and InOpenRange(myhand): return (2,0)
            if InOpenRange(myhand) and Sit.potsize/callchip>3: return (2,0) 
            if QuiteGood(myhand) and Sit.potsize/callchip>5: return (2,0)
            #还是要认怂，这么凶的人少见
            #if InOpenRange(myhand) and MyTurn(Sit)==1: return (3,4)
            #if InTryRange(myhand): return (2,0)
            return (0,0)
        #底池赔率可以，怎么都搞
        if callchip>=10*Sit.bb: 
            if InSuperRange(myhand): return (3,4)
            if InOpenRange(myhand) and Sit.potsize/callchip>3: return (2,0)
            if InStealRange(myhand) and Sit.potsize/callchip>5: return (2,0)
            return (0,0)


        if callchip==0 : return (2,0)
        
    return (0,-1)

#最厉害的
def InSuperRange(myhand):
    if myhand[0].num==myhand[1].num and myhand[0].num>=12: return True
    else : return False

#前位可以开局的
def InOpenRange(myhand):
    if myhand[0].num==myhand[1].num and myhand[0].num>=7: return True
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=14 or myhand[1].num>=14) and myhand[0].num+myhand[1].num>=24: return True
    if myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=25 : return True
    if myhand[0].num+myhand[1].num>=27: return True
    return False

#CO位可以开局的
def InTryRange(myhand):
    if myhand[0].num==myhand[1].num: return True
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=14 or myhand[1].num>=14): return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1: return True
    if myhand[0].num+myhand[1].num>=24: return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==2 and myhand[0].num+myhand[1].num==18 : return True
    return False

#BTN位可以开局的
def QuiteGood(myhand):
    if myhand[0].num==myhand[1].num: return True
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=13 or myhand[1].num>=13): return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1: return True
    if myhand[0].num+myhand[1].num>=24: return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==2: return True
    if myhand[0].suit!=myhand[1].suit and abs(myhand[0].num-myhand[1].num)>=3 and myhand[0].num+myhand[1].num<=23: return False
    return False


#偷的范围
def InStealRange(myhand):
    if myhand[0].suit!=myhand[1].suit and abs(myhand[0].num-myhand[1].num)>=3 and myhand[0].num+myhand[1].num<=23: return False
    return True
