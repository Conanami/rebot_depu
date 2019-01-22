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
from Harrington import DontLikeRate
#fisherman，打低级别和鱼专用的
#from Harrington import flopDecision
from Moshman import flopDecision
from Harrington import MyTurn
from beforeFlop import beforeFlopDecision



#返回值第一个是决定，0弃牌，1过牌，2跟注，3加注，对应不同按键
#待整理的函数
def afterFlopDecision(pubnum,nextWinrate,finalWinrate,leftman,rtSit):
    print("potsize:"+str(rtSit.potsize))
    print("blind:"+str(rtSit.bb))
    print("callchip:"+str(rtSit.callchip))
    publist=getPubList(rtSit)
    myhand=getMyHand(rtSit)
    wholehandlist=myhand+rtSit.cardlist
    if(pubnum==0):
        return "before Flop"
    #翻牌前
    #超级大牌要设置陷阱
    if(pubnum>=1 and pubnum<=3):
        print("翻牌不会走这里！！")
        return (0,0)
    if(pubnum==4):
        if(leftman==2):
            #print('测试是不是走到这里')
            if rtSit.callchip==0:
                #特别大一定要过牌骗人
                if finalWinrate>=0.98: return (2,0)
                if rtSit.potsize<=(leftman*3+2)*rtSit.bb:
                    print('翻牌大家都示弱，转牌咋呼')
                    return (3,1) 
                elif(nextWinrate[1]<-0.03 and finalWinrate>0.9): return (3,1)               
                #对手一过牌我就保持进攻，看看效果，看起来不行
                #if MyTurn(rtSit)==2: return (3,1)
                else: return (2,0)
            #如果我还没有下注
            if(rtSit.betlist[rtSit.myseat]<=0):
                
                if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize<15*rtSit.bb):
                    #超级大就是要骗人
                    if(finalWinrate>=0.98): return (2,0)
                    if(finalWinrate>=0.93): return (3,3)
                    if(finalWinrate>=0.90): return (3,2)
                    if(finalWinrate>=0.80): return (2,0)
                    if(IsDrawFlush(wholehandlist)): return (2,0)
                    if(IsDrawStraight(wholehandlist)): return(2,0)
                    if(rtSit.callchip/rtSit.potsize<finalWinrate): return (2,0)
                    return (0,0)
                
                if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize>=15*rtSit.bb):
                    print('转牌下小注，我不走')
                    if(finalWinrate>=0.98):  
                        if(nextWinrate[1]>=-0.01): return (3,3)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.92): return (3,2)
                    if(finalWinrate>=0.80): return (2,0)
                    if(IsDrawFlush(wholehandlist)): return (2,2)
                    if(IsDrawStraight(wholehandlist)): return(2,2)
                    return (0,0)
                if(rtSit.callchip>=rtSit.potsize/leftman):
                    print('转牌，下注好大，啥意思？')
                    if(nextWinrate[1]>0.3): return (3,4)
                    if(nextWinrate[1]>0.15): return (2,0)
                    if(finalWinrate>=0.97):  
                        if(nextWinrate[1]>=-0.01): return (2,0)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.8): 
                        return (2,0)
                    return (0,0)
            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                if(finalWinrate>=0.98): return (3,4)
                if rtSit.potsize/rtSit.callchip>0.08/(finalWinrate-0.92) and finalWinrate>0.92:
                    return (2,0)
                return (0,0)
            #print('0000')
        if(leftman>=3):
            if rtSit.callchip==0 :
                if rtSit.potsize<=(leftman*3+2)*rtSit.bb and getWaitingman(rtSit)==0:
                    print('转牌咋呼,必须是两圈都没有人显示实力')
                    return (3,1)
                elif(nextWinrate[1]<-0.03 and finalWinrate>0.9): return (3,1)                       
                return (2,0)
            #如果我还没有下注
            if(rtSit.betlist[rtSit.myseat]<=0):
                
                if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize<15*rtSit.bb):
                    if(finalWinrate>=0.94):  
                        if(nextWinrate[1]>=-0.01): return (3,3)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.91): return (3,3)
                    if(finalWinrate>=0.87): return (3,2)
                    if(finalWinrate>=0.70): return (2,0)
                    if(IsDrawFlush(wholehandlist)): return (2,0)
                    if(IsDrawStraight(wholehandlist)): return(2,0)
                    if(rtSit.callchip/rtSit.potsize<finalWinrate): return (2,0)
                    return (0,0)
                if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize>=15*rtSit.bb):
                    if(finalWinrate>=0.96):  
                        if(nextWinrate[1]>=-0.01): return (2,0)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.92): return (3,2)
                    if(IsDrawFlush(publist) or len(dealer.SameSuit(publist))>=3): return (2,0)
                    if(IsDrawStraight(publist)): return (2,0)
                    return (0,0)
                if(rtSit.callchip>=rtSit.potsize/leftman):
                    if(nextWinrate[1]>0.3): return (3,4)
                    if(nextWinrate[1]>0.15): return (2,0)
                    if(finalWinrate>=0.97):  
                        if(nextWinrate[1]>=-0.01): return (2,0)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if rtSit.callchip<=80*rtSit.bb:   
                        print('是到这里了吗？')             
                        if(finalWinrate>=0.8): return (2,0)
                    return (0,0)
            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                if(finalWinrate>=0.98): return (3,4)
                if rtSit.potsize/rtSit.callchip>0.08/(finalWinrate-0.92) and finalWinrate>0.92:
                    return (2,0)
                return (0,0)
        return (0,0)
    if(pubnum==5):
        #还剩2个人
        if(leftman==2):
            #没人下注，底池小积极偷，底池大如果牌大就努力争取
            if rtSit.callchip==0:
                if(finalWinrate>=0.98): return (3,4)
                if rtSit.potsize<=8*rtSit.bb and getWaitingman(rtSit)==0:
                    print('河牌咋呼')
                    return (3,3)
                #对手没啥实力，我价值下注，不下注就没钱了
                if finalWinrate>0.94 and rtSit.potsize<50*rtSit.bb: return (3,1)
                if(finalWinrate>0.85) and rtSit.potsize<25*rtSit.bb: return (3,1)
                #否则摊牌比牌
                return (2,0)
            #如果我还没有下注
            if(rtSit.betlist[rtSit.myseat]<=0):
                #对手下了小注
                if(rtSit.callchip>0 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)/3):
                    print('对手河牌下小注')
                    if(finalWinrate>=0.94): return (3,4)
                    #根据最后胜率来决定
                    if rtSit.potsize<=20*rtSit.bb:
                        if(rtSit.potsize/rtSit.callchip>0.6/(finalWinrate-0.4) and finalWinrate>=0.4): 
                            print('20bb小池子，我头就是硬')
                            return (2,0)
                    if(rtSit.potsize<12*rtSit.bb):
                        if(finalWinrate>0.60): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<20*rtSit.bb): 
                        if(finalWinrate>=0.66): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=20*rtSit.bb):
                        if(finalWinrate>=0.94): return (3,4)
                        if(finalWinrate>=0.91): return (3,1)
                        if(finalWinrate>=0.8): return (2,0)
                        return (0,0)
                    return (0,0)
                #对手表现出很强的实力
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)/3 and rtSit.callchip<=(rtSit.potsize-rtSit.callchip)):
                    print("对手下注半个底池，是在偷吗？")
                    if(finalWinrate>=0.96): return (3,4)
                    if(rtSit.potsize<12*rtSit.bb):
                        if(finalWinrate>0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<20*rtSit.bb): 
                        if(finalWinrate>=0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=20*rtSit.bb and rtSit.potsize<30*rtSit.bb):
                        if(finalWinrate>=0.8): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=30*rtSit.bb):
                        if(finalWinrate>=0.9): return (0,0)
                        return (0,0)
                    return (0,0)
                #面对一个超POT大下注
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)):
                    if(finalWinrate>=0.97): return (3,4)
                    if rtSit.callchip<=30*rtSit.bb:                
                        if(finalWinrate>=0.91): return (2,0)
                        return (0,0)
                    return (0,0)
            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                if(finalWinrate>=0.98): return (3,4)
                if rtSit.potsize/rtSit.callchip>0.08/(finalWinrate-0.92) and finalWinrate>0.92:
                    return (2,0)
                return (0,0)
            return (0,0)
        #还剩3个人以上
        if(leftman>=3):
            #没人下注，底池小积极偷，底池大如果牌大就努力争取
            if finalWinrate>=0.94: return (3,4)
            if rtSit.callchip==0:
                if rtSit.potsize<=(leftman*3+2)*rtSit.bb and getWaitingman(rtSit)==0:
                    print('河牌咋呼')
                    return (3,3)
                #大家都没啥实力，我价值下注
                if finalWinrate>0.68 and rtSit.potsize<(leftman*10+2)*rtSit.bb: return (3,1)
                return (2,0)
            #如果我还没有下注
            if(rtSit.betlist[rtSit.myseat]<=0):
                #对手下了小注
                if(rtSit.callchip>0 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)/3):
                    if(finalWinrate>=0.94): return (3,4)
                    if(rtSit.potsize<12*rtSit.bb ):
                        if(finalWinrate>0.6): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                        if(finalWinrate>=0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>20*rtSit.bb and rtSit.potsize<=40*rtSit.bb):
                        if(finalWinrate>=0.94): return (3,4)
                        if(finalWinrate>=0.91): return (3,1)
                        if(finalWinrate>=0.76): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>40*rtSit.bb):
                        if(finalWinrate>=0.94): return (3,4)
                        if(finalWinrate>=0.92): return (2,0)
                        if(finalWinrate>=0.76): return (0,0)
                        return (0,0)
                    return (0,0)
                #对手表现出很强的实力
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)/3 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)):
                    if(finalWinrate>=0.94): return (3,4)
                    if(rtSit.potsize<12*rtSit.bb):
                        if(finalWinrate>0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<=20*rtSit.bb): 
                        if(finalWinrate>=0.91): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>20*rtSit.bb):
                        if(finalWinrate>=0.92): return (2,0)
                        return (0,0)
                    return (0,0)
                #面对一个超POT大下注
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)):
                    if(finalWinrate>=0.97): return (3,4)
                    if rtSit.callchip<=30*rtSit.bb:                
                        if(finalWinrate>=0.92): return (2,0)
                        return (0,0)
                    return (0,0)
                return (0,0)
            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                if(finalWinrate>=0.98): return (3,4)
                if rtSit.potsize/rtSit.callchip>0.08/(finalWinrate-0.92) and finalWinrate>0.92:
                    return (2,0)
                return (0,0)
        return (0,0)
    return (0,-1)


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
        print('翻前决策')
        finalDecision=beforeFlopDecision(rtSit,callchip)
    elif(pubnum==1 or pubnum==2): finalDecision=(2,0)
    #如果是翻牌后
    elif(pubnum==3): 
        finalDecision=flopDecision(rtSit)
    #如果是转牌和河牌
    elif(pubnum>=4):
        #如果没有读到底池大小
        if(rtSit.potsize==0): finalDecision=(-1,-1)
        #计算当前牌的胜率
        myWinrate=calcuWinrate(rtSit)
        nextWinrate=DontLikeRate(rtSit,myWinrate)
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
            if pubnum==4:  #and len(dealer.SameSuit(rtSit.cardlist))<3):
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
        mydecision=afterFlopDecision(pubnum,nextWinrate,finalWinrate,leftman,rtSit)
        finalDecision=mydecision
    
    #实际情况还要结合自己的筹码，才能决定到底点击哪里
    newDecision=getClickDecision(finalDecision,rtSit)
    return newDecision


#根据自己手里的筹码多少，下注一个比例
def getClickDecision(finalDecision,rtSit):
    #返回的决定
    rtDecision=finalDecision
    percent=0
    pubnum=getPubnum(rtSit)
    #如果要加注，要根据自己的筹码和底池的实际情况
    if(finalDecision[0]==3):
        #如果筹码太少,只能点全下
        if(rtSit.chiplist[rtSit.myseat]<0.5*rtSit.potsize):
            rtDecision=(3,4)
        #如果翻后底池比3个盲注还小，那就不能选择3，1和3，2，直接3，3
        if(rtSit.potsize<=3*rtSit.bb and pubnum>0):
            if(finalDecision[1]==1): rtDecision=(3,3)
            if(finalDecision[1]==2): rtDecision=(3,3)
        #如果是选择了3，5,1/3底池薄价值下注,3,6 , 3/4底池的下注，3,7 1.5倍底池的超pot,都需要重新计算
        if(finalDecision[1]==5):
            #如果1/3底池下注，筹码是够的
            if(rtSit.chiplist[rtSit.myseat]>0.33*rtSit.potsize):
                percent=0.33*rtSit.potsize/rtSit.chiplist[rtSit.myseat]
                rtDecision=(4,percent)
            else:   #如果筹码不够
                rtDecision=(3,4)

        #如果选择了3/4底池的下注            
        if(finalDecision[1]==6):
            #如果3/4底池下注，并且筹码是够的
            if(rtSit.chiplist[rtSit.myseat]>0.75*rtSit.potsize):
                percent=0.75*rtSit.potsize/rtSit.chiplist[rtSit.myseat]
                rtDecision=(4,percent)
            else:   #如果筹码不够
                rtDecision=(3,4)
        #如果选择了1.5倍底池的下注
        if(finalDecision[1]==7):
            #如果1.5倍底池的下注，筹码是够的
            if(rtSit.chiplist[rtSit.myseat]>1.5*rtSit.potsize):
                percent=1.5*rtSit.potsize/rtSit.chiplist[rtSit.myseat]
                rtDecision=(4,percent)
            else:   #如果筹码不够
                rtDecision=(3,4)
    #如果对方是全下，那2,0要变3,0
    if IsAllIn(rtSit) and finalDecision[0]==2: rtDecision=(3,0)
    if rtSit.callchip>rtSit.chiplist[rtSit.myseat] and finalDecision[0]==2: rtDecision=(3,0)
    return rtDecision
    

