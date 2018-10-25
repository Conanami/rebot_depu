import dealer
import math
import random
from dealer import IsDrawFlush
from dealer import IsDrawStraight
from reader import getPubList
from reader import getPubnum
from read_pokerstar import getCallchip
from reader import getSurvivor
from reader import getMyHand
from reader import calcuWinrate
from reader import calcuNumRate
from dealer import SameSuit
from dealer import LikeStraight
from dealer import IsFlush
from reader import getWaitingman
from dealer import IsGunshotStraight
from dealer import cardtypeOf

#得到我是第几个行动的人
def MyTurn(Sit):
    cnt=1
    for i in range(Sit.position+1,Sit.position+6):
        tmpi=i%6
        if tmpi==Sit.myseat: return cnt
        else:
            if Sit.chiplist[tmpi]>=0 or Sit.betlist[tmpi]>=0:
                cnt=cnt+1
    return cnt

def afterFlopDecision(Sit):
    pubnum=getPubnum(Sit)
    if pubnum==3:
        return flopDecision(Sit)
    if pubnum==4:
        return turnDecision(Sit)
    if pubnum==5:
        return riverDecision(Sit)
    return (0,0)

def turnDecision(Sit):
    return (0,0)
def riverDecision(Sit):
    return (0,0)

def flopDecision(Sit):
    leftman=getSurvivor(Sit)[1]
    #得到自己的手牌，加上公共牌
    myhand=getMyHand(Sit)
    myhand=myhand+Sit.cardlist
    winrate=calcuWinrate(Sit)
    print('胜率判断：%s',winrate)
    print("potsize:"+str(Sit.potsize))
    print('原来底池:'+str(Sit.oldpot))
    print('还剩几人:'+str(leftman))
    print('我的位置:'+str(MyTurn(Sit)))

    if leftman==2:
        #我在后位
        if MyTurn(Sit)==leftman:
            if Sit.callchip==0:
                return (3,3)
            elif Sit.callchip<Sit.oldpot/1.8:
                if winrate>0.92: return (3,3)
                if winrate>0.8: return (3,3)
                if winrate>0.7: return (3,3)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                return (0,0)
            elif Sit.callchip>=Sit.oldpot/1.8 and Sit.callchip<=Sit.oldpot:
                if winrate>0.92: return (3,4)
                if winrate>0.9: return (3,3)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                return (0,0)
            elif Sit.callchip>Sit.oldpot:
                if winrate>0.92: return (3,4)
                if Sit.potsize/Sit.callchip>3 and (IsDrawFlush(myhand) or IsDrawStraight(myhand)): return (2,0)
                return (0,0)
        #我在前位
        elif MyTurn(Sit)==1:
            if Sit.callchip==0:
                if winrate>0.56: return (3,3)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (3,3)
                if cardtypeOf(Sit.cardlist)==3: return (3,3)
                return (3,1)
            elif Sit.callchip<Sit.oldpot/1.8:
                if winrate>0.9: return (3,3)
                if winrate>0.8: return (3,3)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                return (0,0)
            elif Sit.callchip>=Sit.oldpot/1.8 and Sit.callchip<=Sit.oldpot:
                print('我在前位，最后一个CBET了，我中对以上招架一下')
                if winrate>0.92: return (3,4)
                if winrate>0.83: return (3,3)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                return (0,0)
            elif Sit.callchip>Sit.oldpot:
                #顶对顶踢脚，我谁都不怕
                if winrate>0.92: return (3,4)
                if Sit.potsize/Sit.callchip>3 and (IsDrawFlush(myhand) or IsDrawStraight(myhand)): return (2,0)
                return (0,0)
        
    elif leftman>2:
        #我在后位没人下注，多人需要两次确认
        if Sit.callchip==0:
            #多人底池还是需要主动一点
            if winrate>0.83: return (3,3)
            if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (3,3)
            return (2,0)
        elif Sit.callchip<Sit.oldpot/1.8:
            if winrate>0.95: return (3,4)
            if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (3,3)
            if winrate>0.8: return (2,0)
            return (0,0)
        elif Sit.callchip>=Sit.oldpot/1.8 and Sit.callchip<=Sit.oldpot:
            if winrate>0.95: return (3,3)
            if winrate>0.9: return (2,0)
            if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
        elif Sit.callchip>Sit.oldpot:
            if winrate>0.97: return (3,4)
            if Sit.potsize/Sit.callchip>3 and (IsDrawFlush(myhand) or IsDrawStraight(myhand)): return (2,0)
            return (0,0)
    return (0,0)
        
            
            
            