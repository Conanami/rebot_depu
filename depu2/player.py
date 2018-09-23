#import time
import dealer
import math
import random
#import readpot
from dealer import IsDrawFlush
from dealer import IsDrawStraight
from reader import getPubList
from reader import getPubnum
from reader import getSurvivor
from reader import getMyHand
from reader import calcuWinrate
from reader import getWaitingman
from dealer import IsFlush
from reader import IsAllIn
from reader import IsAfter
  
#fisherman，打低级别和鱼专用的

#返回值第一个是决定，0弃牌，1过牌，2跟注，3加注，对应不同按键
#待整理的函数
def afterFlopDecision(pubnum,singleWinrate,finalWinrate,leftman,rtSit):
    print("potsize:"+str(rtSit.potsize))
    #print("blind:"+str(rtSit.bb))
    #print("callchip:"+str(rtSit.callchip))
    publist=getPubList(rtSit)
    myhand=getMyHand(rtSit)
    myhand=myhand+rtSit.cardlist
    #翻牌前
    if(pubnum==0):
        return "before Flop"
    #超级大牌要设置陷阱
    #翻后
    if(pubnum>=1 and pubnum<=3):
        if(leftman==2):
            if(rtSit.callchip==0):
                if(finalWinrate>0.99): return (2,0)
                if(finalWinrate>0.9): return(3,3)
                if(random.random()>0.2): return (3,1)
                if(IsDrawFlush(myhand)): return (3,2)
                if(IsDrawStraight(myhand)): return(3,2)
                return (2,0)
            #对手表现出最强的实力,我强力下注后加注
            if rtSit.betlist[rtSit.myseat]>=(rtSit.potsize-max(rtSit.betlist))/(leftman+1) and rtSit.callchip>0:
                if finalWinrate>=0.985: return (2,0)
                if finalWinrate>=0.94: return (3,4)
                if rtSit.potsize/rtSit.callchip>=3.9 and finalWinrate>=0.85 : return (2,0)
                else: return (0,0)
            if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize<15*rtSit.bb):
                if(finalWinrate>=0.99): return (2,0)
                if(finalWinrate>=0.95): return (3,4)
                if(finalWinrate>=0.92): return (3,3)
                if(finalWinrate>=0.88): return (3,2)
                if(finalWinrate>=0.7): return (3,2)
                if(IsDrawFlush(myhand)): return (3,2)
                if(IsDrawStraight(myhand)): return(3,2)
                return (0,0)
            if(rtSit.callchip<rtSit.potsize/leftman):
                #翻后底池不大，可以头铁一点
                if rtSit.potsize>=15*rtSit.bb and rtSit.potsize<30*rtSit.bb:
                    if(finalWinrate>=0.95): return (3,4)
                    if(finalWinrate>=0.8): return (2,0)
                    if(IsDrawFlush(myhand)): return (2,2)
                    if(IsDrawStraight(myhand)): return(2,2)
                #翻后底池比较大，就弱一点吧
                if rtSit.potsize>=30*rtSit.bb and rtSit.potsize<=60*rtSit.bb:
                    if(finalWinrate>=0.95): return (3,4)
                    if(finalWinrate>=0.85): return (2,0)
                    if(IsDrawFlush(myhand)): return (2,2)
                    if(IsDrawStraight(myhand)): return(2,2)
                return (0,0)
            if(rtSit.callchip>=rtSit.potsize/leftman):
                #if(finalWinrate>=0.99): return (2,0)
                if(finalWinrate>=0.97): return (3,4)
                #如果碰到全下要小心
                if(finalWinrate>=0.92): 
                    if(rtSit.callchip<=80*rtSit.bb): return (2,0)
                if(rtSit.potsize<15*rtSit.bb and finalWinrate>0.7): return (2,0)
                #if (finalWinrate>=0.89 and rtSit.potsize<=60*rtSit.bb): return (2,0)
                return (0,0)
        if(leftman>=3):
            if(rtSit.callchip==0):
                if(finalWinrate>0.95): return (3,1)
                if(finalWinrate>0.8): return(3,3)
                if(random.random()>0.5 and leftman<=3 and getWaitingman(rtSit)<=1): return (3,1)
                if(IsDrawFlush(myhand)): return (2,0)
                if(IsDrawStraight(myhand)): return(2,0)
                return (2,0)
            #对手表现出最强的实力,在我强力下注后加注
            if rtSit.betlist[rtSit.myseat]>=(rtSit.potsize-max(rtSit.betlist))/(leftman+1) and rtSit.callchip>0:
                if(finalWinrate>=0.92): return (2,0)
                else: return (0,0)
            if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize<15*rtSit.bb):
                if(finalWinrate>=0.95): return (3,4)
                elif(finalWinrate>=0.9): return (3,3)
                elif(finalWinrate>=0.7): 
                    if(getWaitingman(rtSit)<=1): return (3,1)
                    else: return (2,0)
                elif(finalWinrate>=0.5): return (2,0)
                if(IsDrawFlush(myhand)): return (2,0)
                if(IsDrawStraight(myhand)): return(2,0)
                return (0,0)
            if(rtSit.callchip<rtSit.potsize/leftman):
                #翻后底池不大，可以头铁一点
                if rtSit.potsize>=15*rtSit.bb and rtSit.potsize<30*rtSit.bb:
                    if(finalWinrate>=0.95): return (3,4)
                    if(finalWinrate>=0.68): return (2,0)
                    if(IsDrawFlush(myhand)): return (2,2)
                    if(IsDrawStraight(myhand)): return(2,2)
                #翻后底池比较大，就弱一点吧
                if rtSit.potsize>=30*rtSit.bb and rtSit.potsize<=60*rtSit.bb:
                    if(finalWinrate>=0.95): return (3,4)
                    if(finalWinrate>=0.75): return (2,0)
                    if(IsDrawFlush(myhand)): return (2,2)
                    if(IsDrawStraight(myhand)): return(2,2)
                return (0,0)
            if(rtSit.callchip>=rtSit.potsize/leftman):
                if(finalWinrate>=0.92): return (3,4)
                #如果碰到全下什么的，要小心
                if(finalWinrate>=0.8): 
                    if rtSit.callchip<=80*rtSit.bb: return (2,0)
                if(rtSit.potsize<15*rtSit.bb and finalWinrate>0.7): return (2,0)
                return (0,0)
        return (0,-1)
    #转牌阶段，4张公共牌
    if(pubnum==4):
        if(leftman==2):
            if(rtSit.callchip==0):
                if(finalWinrate>0.99): return (2,0)
                if(finalWinrate>0.9): return(3,3)
                if(random.random()>0.3 and rtSit.potsize<15*rtSit.bb and getWaitingman(rtSit)==0): return (3,1)
                #if(rtSit.potsize<15*rtSit.bb):
                if(random.random()>0.5): return (3,1)
                if(IsDrawFlush(myhand)): return (2,0)
                if(IsDrawStraight(myhand)): return(2,0)
                return (2,0)
            #对手表现出最强的实力,我强力下注后加注
            if rtSit.betlist[rtSit.myseat]>=(rtSit.potsize-max(rtSit.betlist))/(leftman+1) and rtSit.callchip>0:
                if(finalWinrate>=0.985): return (2,0)
                #套池了就只能跟到底
                if rtSit.potsize/rtSit.callchip>leftman+3 and finalWinrate>0.91: return (2,0) 
                else: return (0,0)
            if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize<15*rtSit.bb):
                if(finalWinrate>=0.95): return (3,4)
                if(finalWinrate>=0.92): return (3,3)
                if(finalWinrate>=0.88): return (2,0)
                if(finalWinrate>=0.7): return (2,0)
                if(IsDrawFlush(myhand)): return (2,0)
                if(IsDrawStraight(myhand)): return(2,0)
                if(rtSit.callchip/rtSit.potsize<finalWinrate): return (2,0)
                return (0,0)
            if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize>=15*rtSit.bb):
                if(finalWinrate>=0.95): return (3,4)
                #咨询一下对手到底是不是咋呼
                if(finalWinrate>=0.9): return (3,2)
                if(IsDrawFlush(myhand)): return (2,2)
                if(IsDrawStraight(myhand)): return(2,2)
                #小注头铁
                if((rtSit.callchip/rtSit.potsize)<(finalWinrate/(leftman+1))): return (2,0)
                return (0,0)
            if(rtSit.callchip>=rtSit.potsize/leftman):
                if(finalWinrate>=0.98): return (3,4)
                if(finalWinrate>=0.92 and rtSit.callchip<=80*rtSit.bb): return (2,0)
                if(rtSit.potsize<15*rtSit.bb and finalWinrate>0.7): return (2,0)
                return (0,0)
            #print('0000')
        if(leftman>=3):
            if(rtSit.callchip==0):
                #print("到这里了吗?")
                #print("我的单挑胜率:"+str(finalWinrate))
                if(finalWinrate>0.98): return (2,0)
                if(finalWinrate>0.8): return(3,3)
                #只有在有位置的时候才偷
                if random.random()>0.7 and rtSit.myseat==rtSit.position : return (3,1)
                if(IsDrawFlush(myhand)): 
                    if(getWaitingman(rtSit)<=1): return (3,1)
                    else: return (2,0)
                if(IsDrawStraight(myhand)):
                    if(getWaitingman(rtSit)<=1): return (3,1)
                    else: return (2,0)
                return (2,0)
            #对手表现出最强的实力,我强力下注后加注
            if rtSit.betlist[rtSit.myseat]>=(rtSit.potsize-max(rtSit.betlist))/(leftman+1) and rtSit.callchip>0:
                if(finalWinrate>=0.985): return (2,0)
                #套池了就只能跟到底
                if rtSit.potsize/rtSit.callchip>leftman+3 and finalWinrate>0.91: return (2,0) 
                else: return (0,0)
            #对手下了小注
            if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize<15*rtSit.bb):
                if(finalWinrate>=0.95): return (3,4)
                if(finalWinrate>=0.92): return (3,3)
                if(finalWinrate>=0.85): return (2,0)
                #if(finalWinrate>=0.5): return (2,0)
                if(IsDrawFlush(myhand)): return (2,0)
                if(IsDrawStraight(myhand)): return(2,0)
                if(rtSit.callchip/rtSit.potsize<finalWinrate): return (2,0)
                return (0,0)
            if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize>=15*rtSit.bb):
                if(finalWinrate>=0.95): return (3,4)
                if(finalWinrate>=0.8): return (3,2)
                if((rtSit.callchip/rtSit.potsize)<(finalWinrate/(leftman+1))): return (2,0)
                if(IsDrawFlush(publist) or len(dealer.SameSuit(publist))>=3): return (0,0)
                if(IsDrawStraight(publist)): return (0,0)
                return (0,0)
            if(rtSit.callchip>=rtSit.potsize/leftman):
                if(finalWinrate>=0.96): return (3,4)
                if(finalWinrate>=0.9 and rtSit.callchip<=80*rtSit.bb): return (2,0)
                if(rtSit.potsize<15*rtSit.bb and finalWinrate>0.7): return (2,0)
                return (0,0)
        return (0,-1)
    #河牌阶段，5张公共牌
    if(pubnum==5):
        #还剩2个人
        if(leftman==2):
            #没人下注，底池小积极偷，底池大如果牌大就努力争取
            if(rtSit.callchip==0):
                if(finalWinrate>=0.95): return (3,4)
                if(rtSit.potsize<12*rtSit.bb and random.random()>0.3): return (3,2)
                if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                    if(random.random()>0.5): return (3,1)
                    else: return (2,0)
                if(rtSit.potsize>20*rtSit.bb):
                    if(finalWinrate>=0.95): return (3,4)
                    if(finalWinrate>=0.9 and finalWinrate<0.95): return (3,1)
                    return (2,0)
                else:
                    return (2,0)
            #对手表现出最强的实力,我强力下注后加注
            if rtSit.betlist[rtSit.myseat]>=(rtSit.potsize-max(rtSit.betlist))/(leftman+1) and rtSit.callchip>0:
                if(finalWinrate>=0.985): return (2,0)
                #套池就跟到底了，没有选择了
                if rtSit.potsize/rtSit.callchip>leftman+3 and finalWinrate>0.91: return (2,0) 
                else: return (0,0)
            #对手下了小注
            if(rtSit.callchip>0 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)/3):
                if(finalWinrate>=0.95): return (3,4)
                if(rtSit.potsize<12*rtSit.bb and finalWinrate>0.75): return (2,0)
                if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                    if(finalWinrate>0.9): return (2,0)
                    return (2,0)
                if(rtSit.potsize>20*rtSit.bb):
                    if(finalWinrate>=0.96): return (3,4)
                    if(finalWinrate>=0.9 and finalWinrate<0.95): return (3,1)
                    #小注小池头铁
                    if rtSit.potsize/rtSit.callchip>=3 and rtSit.potsize<=25*rtSit.bb and finalWinrate>0.7: return (2,0) 
                    #小注头铁
                    if((rtSit.callchip/rtSit.potsize)<(finalWinrate/(leftman+1))): return (2,0)
                    
                return (0,0)
            #对手表现出很强的实力
            if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)/3 and rtSit.callchip<=(rtSit.potsize-rtSit.callchip)):
                if(finalWinrate>=0.95): return (3,4)
                if(rtSit.potsize<12*rtSit.bb and finalWinrate>0.8): return (2,0)
                if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                    if(finalWinrate>0.9): return (2,0)
                    return (2,0)
                if(rtSit.potsize>20*rtSit.bb):
                    if(finalWinrate>=0.94): return (2,0)
                    if(finalWinrate>=0.92 and finalWinrate<0.95): return (2,0)
                    #小注小池头铁
                    if rtSit.potsize/rtSit.callchip>=2.9 and rtSit.potsize<=25*rtSit.bb and finalWinrate>0.7: return (2,0) 
                    return (0,0)
                return (0,0)
           
            #面对一个超POT大下注
            if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)):
                if(finalWinrate>=0.97): return (3,4)
                if(finalWinrate>=0.94): return (2,0)
                if(rtSit.potsize<20*rtSit.bb and finalWinrate>0.7): return (2,0)
                return (0,0)
            
        #还剩3个人以上
        if(leftman>=3):
            #没人下注，底池小积极偷，底池大如果牌大就努力争取
            if(rtSit.callchip==0):
                if(finalWinrate>=0.93): return (3,4)
                if(rtSit.potsize<12*rtSit.bb and random.random()>0.3): return (3,2)
                if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                    if(random.random()>0.5): return (3,0)
                    return (2,0)
                if(rtSit.potsize>20*rtSit.bb):
                    if(finalWinrate>=0.93): return (3,4)
                    if(finalWinrate>=0.90 and finalWinrate<0.93): return (3,1)
                    #小注头铁
                    if((rtSit.callchip/rtSit.potsize)<(finalWinrate/(leftman+1))): return (2,0)
                    return (2,0)
                return (2,0)
            #对手表现出最强的实力,我强力下注后加注
            if rtSit.betlist[rtSit.myseat]>=(rtSit.potsize-max(rtSit.betlist))/(leftman+1) and rtSit.callchip>0:
                if(finalWinrate>=0.985): return (2,0)
                #套池就跟到底了，没有选择了
                if rtSit.potsize/rtSit.callchip>leftman+3 and finalWinrate>0.91: return (2,0) 
                else: return (0,0)
            #对手下了小注
            if(rtSit.callchip>0 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)/3):
                if(finalWinrate>=0.93): return (3,4)
                if(rtSit.potsize<12*rtSit.bb and finalWinrate>0.75): return (2,0)
                if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                    if(finalWinrate>0.9): return (2,0)
                    return (2,0)
                if(rtSit.potsize>20*rtSit.bb):
                    if(finalWinrate>=0.96): return (3,4)
                    if(finalWinrate>=0.92 and finalWinrate<0.95): return (3,1)
                    #小注头铁
                    if((rtSit.callchip/rtSit.potsize)<(finalWinrate/(leftman+1))): return (2,0)
                    return (0,0)
                return (0,0)
            #对手表现出一定的实力
            if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)/3 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)):
                if(finalWinrate>=0.94): return (3,4)
                if(rtSit.potsize<12*rtSit.bb and finalWinrate>0.8): return (2,0)
                if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                    if(finalWinrate>0.9): return (2,0)
                    return (2,0)
                if(rtSit.potsize>20*rtSit.bb):
                    if(finalWinrate>=0.94): return (2,0)
                    if(finalWinrate>=0.90 and finalWinrate<0.94): return (2,0)
                    #小注小池头铁
                    if rtSit.potsize/rtSit.callchip>=3 and rtSit.potsize<=25*rtSit.bb and finalWinrate>0.7: return (2,0) 
                    return (0,0)
                return (0,0)
            #面对一个超POT大下注
            if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)):
                if(finalWinrate>=0.98): return (3,4)
                if(rtSit.potsize<20*rtSit.bb and finalWinrate>0.7): return (2,0)
                return (0,0)
            
        return (0,0)
    return (0,-1)

#翻前决策
def beforeFlopDecision(Sit,callchip):
    print("翻前决策")
    myhand=getMyHand(Sit)
    pubcnt=getPubnum(Sit)
    leftman=getSurvivor(Sit)[1]
  
    #如果中间有牌，或者两张牌没有读出来，则返回弃牌
    if(pubcnt==0 and len(myhand)==2):
        
        if(InSuperRange(myhand)):
            if(callchip==0): return (3,3)
            if(callchip>0 and callchip<Sit.bb*3): 
                if Sit.betlist[Sit.myseat]>=2*Sit.bb: return (3,4)
                else: return (3,3)
            if(callchip>=Sit.bb*3): return (3,4)
            
        
        #好牌可以加注入局
        if(InOpenRange(myhand) and callchip<=Sit.bb and getWaitingman(Sit)<=5): return (3,random.randint(1,2))
        #投机牌如果没有人入局，我有好位置，也可以入局
        if InTryRange(myhand) and callchip<=Sit.bb and Sit.position==Sit.myseat :
            return (2,1)
        #如果是开局牌，则可以跟别人open，但不能跟别人的4bet
        if InOpenRange(myhand) and callchip>Sit.bb and callchip<=Sit.bb*6 and Sit.betlist[Sit.myseat]<=Sit.bb: 
            if(callchip==Sit.bb): return (2,1)
            else: return (2,callchip)
        #底池赔率合适，啥牌都可以玩
        if callchip/Sit.potsize<1/(leftman+2) and (InTryRange(myhand) or InOpenRange(myhand)) and callchip<=5*Sit.bb: 
            return (2,callchip)
        #小盲单挑大盲可以玩
        if(callchip/Sit.potsize<0.5 and callchip<=Sit.bb and callchip>0 and leftman==2): 
            if(InTryRange(myhand)): return (3,1)
            elif (random.random()>0.5): return (3,1)
            else: return (0,0)
        #大盲单挑小盲
        if(callchip==0 and leftman==2):
            if(InTryRange(myhand)): return (3,1)
            elif (random.random()>0.5): return (3,1)
            else: return (2,0)

        #两个人单挑，很少情况接ALLIN玩玩
        if(leftman==2 and callchip>=5*Sit.bb):
            return (0,0)
        #如果是大盲白看牌
        if(callchip==0): 
            if(random.random()>0.5): return (3,1)
            return (2,0)
        return (0,0)
    else:
        return (0,-1)

#入局玩的牌，紧是硬道理
def InOpenRange(myhand):
    #print(str(myhand[0].suit)+","+str(myhand[0].num)+"|"+str(myhand[1].suit)+","+str(myhand[1].num))
    if(InSuperRange(myhand)): return False
    #有张A
    #if((myhand[0].num >= 14 and myhand[1].num < 14) or (myhand[0].num < 14 and myhand[1].num >= 14)): return True
    
    #两张高牌
    if(myhand[0].num+myhand[1].num>=26): return True

    #两张同花高牌
    if(myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=24 ): return True

    #中口袋对
    if(myhand[0].num==myhand[1].num and myhand[0].num>=7): return True
    
    
    return False

#入局投机牌
def InTryRange(myhand):
    #不是超强牌
    if(InSuperRange(myhand)): return False
    #也不是进池牌
    if(InOpenRange(myhand)): return False
    #有张A
    if((myhand[0].num >= 14 ) or (myhand[0].num < 14 and myhand[1].num >= 14)): return True
    #带AK的同花
    if(myhand[0].suit==myhand[1].suit and (myhand[0].num>=13 or myhand[1].num>=13)): return True
    #所有口袋对
    if(myhand[0].num==myhand[1].num): return True
    #大的连牌和中的口袋对
    if(abs(myhand[0].num-myhand[1].num)<=2 and myhand[0].num>=8 and myhand[1].num>=8): return True
    #同花连牌
    if(abs(myhand[0].num-myhand[1].num)<=2 and myhand[0].suit==myhand[1].suit and (myhand[0].num>=6 or myhand[1].num>=6)): 
        return True
    return False

#只有AA,KK,QQ跟人推
def InSuperRange(myhand):
    if(myhand[0].num==myhand[1].num and myhand[0].num>=12): return True
    #if(myhand[0].num+myhand[1].num>=26): return True
    else: return False

#做出决定，该函数对外
def makeDecision(rtSit):
    #得到要跟注多少筹码
    #callchip=getCallchip(rtSit)
    #rtSit.callchip=max(callchip,rtSit.callchip)
    callchip=rtSit.callchip
    #得到当前公共牌的数量
    pubnum=getPubnum(rtSit)
    
    #得到自己的手牌，加上公共牌
    myhand=getMyHand(rtSit)
    myhand=myhand+rtSit.cardlist

    print("callchip:"+str(callchip))
    print("pubnum:"+str(pubnum))
    
    #如果是翻牌前
    if(pubnum==0):
        finalDecision=beforeFlopDecision(rtSit,callchip)
    elif(pubnum==1 or pubnum==2): finalDecision=(2,0)
    #如果是翻牌后
    elif(pubnum>=3):
        #如果没有读到底池大小
        if(rtSit.potsize==0): finalDecision=(-1,-1)
        #计算当前牌的胜率
        myWinrate=calcuWinrate(rtSit)
        #得到当前还剩几个人在底池中
        leftman=getSurvivor(rtSit)[1]
        #胜率与人数的关系，人数越多，胜率越小
        print('我的胜率%.4f' % myWinrate)
        print('剩余人数%d ' % leftman)
        finalWinrate=math.pow(myWinrate,leftman-1)
        if IsDrawFlush(myhand):
            if(pubnum==3):
                if(myhand[0].suit==myhand[1].suit):
                    if(finalWinrate<0.5):
                        print('同花听牌，胜率增加%.4f' % 0.3)
                        finalWinrate=finalWinrate+0.3
                if(len(dealer.SameSuit(rtSit.cardlist))==3):
                    if(IsFlush(myhand)==False):
                        print('公面三同花,胜率减少%.4f' % 0.1)
                        finalWinrate=finalWinrate-0.1
            if(pubnum==4 and len(dealer.SameSuit(rtSit.cardlist))<3):
                if(finalWinrate<0.6):
                    print('同花听牌,胜率增加%.4f' % 0.15)
                    finalWinrate=finalWinrate+0.15
        if IsDrawStraight(myhand):
            if pubnum==3:
                if(finalWinrate<0.5):
                    print('顺子听牌，胜率增加%.4f' % 0.3)
                    finalWinrate=finalWinrate+0.3
            if pubnum==4 and IsDrawStraight(rtSit.cardlist)==False :
                if(finalWinrate<0.6):
                    print('顺子听牌，胜率增加%.4f' % 0.15)
                    finalWinrate=finalWinrate+0.15
        
        print('最后胜率%.4f' % finalWinrate)
        #翻牌后的决策
        mydecision=afterFlopDecision(pubnum,myWinrate,finalWinrate,leftman,rtSit)
        finalDecision=mydecision

    #如果要加注，要根据自己的筹码和底池的实际情况
    if(finalDecision[0]==3):
        #如果翻前，要跟注的量已经大于3个盲注了，则3，1，3，2都变成3，3
        if(rtSit.callchip>3*rtSit.bb and (finalDecision[1]==1 or finalDecision[1]==2)):
            finalDecision=(3,3)
        #如果翻前，底池大小小于4个盲注，则一个底池下注是灰色
        if(rtSit.potsize<=4*rtSit.bb and pubnum==0):
            if(finalDecision[1]==3): 
                finalDecision=(3,2)
        #如果所有筹码小于要跟注的数量，那么直接allin
        if(rtSit.chiplist[rtSit.myseat]<rtSit.callchip): finalDecision=(3,0)
        #如果筹码大于需要跟注的数量
        if(rtSit.chiplist[rtSit.myseat]>=rtSit.callchip):
            #如果比2/3底池多，但是不到一个底池，则3，3变3，2
            if(finalDecision[1]==3 and rtSit.chiplist[rtSit.myseat]>=0.66*rtSit.potsize and rtSit.chiplist[rtSit.myseat]<rtSit.potsize):
                finalDecision=(3,2)
            #如果比1/2底池多，但是不到2/3个底池，则3，2变3，1
            if(finalDecision[1]==2 and rtSit.chiplist[rtSit.myseat]>=0.5*rtSit.potsize and rtSit.chiplist[rtSit.myseat]<0.66*rtSit.potsize):
                finalDecision=(3,1)
            #如果比1/2底池小，则只能选全下
            if(finalDecision[1]==1 and rtSit.chiplist[rtSit.myseat]<0.5*rtSit.potsize):
                finalDecision=(3,4)
        #如果翻后底池比3个盲注还小，那就不能选择3，1和3，2，直接3，3
        if(rtSit.potsize<=3*rtSit.bb and pubnum>0):
            if(finalDecision[1]==1): finalDecision=(3,3)
            if(finalDecision[1]==2): finalDecision=(3,3)
    #如果对方是全下，那2,0要变3,0
    if IsAllIn(rtSit) and finalDecision[0]==2: finalDecision=(3,0)
    return finalDecision
