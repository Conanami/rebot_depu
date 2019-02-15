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
from dealer import getHighCard

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
    #计算胜率
    winrate=calcuWinrate(Sit)
    print('胜率判断：',winrate)
    print("potsize:"+str(Sit.potsize))
    print('原来底池:'+str(Sit.oldpot))
    print('还剩几人:'+str(leftman))
    print('我的位置:'+str(MyTurn(Sit)))

    if leftman==2:
        #我在后位
        if MyTurn(Sit)==leftman:
            #我没有下过注
            if Sit.betlist[Sit.myseat]<=Sit.oldpot/2.1 :
                print('我在后位，并没有认真下注过')
                if Sit.callchip==0:
                    #除了超大牌外
                    if winrate>0.98: return (2,0)
                    #所有牌正常CBET
                    return (3,1)
                elif Sit.callchip<Sit.oldpot/1.8:
                    if winrate>0.95: return (3,4)
                    if winrate>0.8: return (2,0)
                    if winrate>0.7: return (2,0)
                    if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                    return (0,0)
                elif Sit.callchip>=Sit.oldpot/1.8 and Sit.callchip<=Sit.oldpot:
                    if winrate>0.95: return (3,4)
                    if winrate>0.75: 
                        print('中对，面对CBET不能太弱')
                        return (2,0)
                    if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                    return (0,0)
                elif Sit.callchip>Sit.oldpot:
                    if winrate>0.95: return (3,4)
                    if Sit.potsize/Sit.callchip>3 and (IsDrawFlush(myhand) or IsDrawStraight(myhand)): return (2,0)
                    return (0,0)
            #我已经做了半池下注，对手仍然加注我
            if Sit.betlist[Sit.myseat]>Sit.oldpot/2.1  and Sit.betlist[Sit.myseat]<Sit.oldpot*1.5 :
                if winrate>0.98: 
                    print('总归打光了')
                    return (3,4)
                if winrate>0.95: 
                    print('勉强跟注吧')
                    return (2,0)
                if Sit.callchip/Sit.potsize<0.3 and winrate>0.9:
                    print('对手只是不相信我的CBET，还是要继续战斗的')
                    return (2,0)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0) 
                else: return (0,0)
            
            if Sit.betlist[Sit.myseat]>=Sit.oldpot*1.5 :
                print('对方下注，我加注，对方还能再加')
                if Sit.callchip/Sit.potsize<0.1: 
                    print('反正打光了')
                    return (2,0)
                if winrate>0.985: 
                    print('只能打光了，大牌撞大牌')
                    return (3,4)
                if winrate>0.95 and Sit.callchip/Sit.potsize<0.3:
                    print('套池只能勉强打')
                    return (2,0)
                if (IsDrawFlush(myhand) or IsDrawStraight(myhand)) and Sit.callchip/Sit.potsize<0.3:
                    print('底池赔率还行，只能拼命了')
                    return (2,0) 
                else: return (0,0)
        #我在前位
        elif MyTurn(Sit)==1:
            if Sit.callchip==0:
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (3,3)
                if cardtypeOf(Sit.cardlist)==3: return (3,3)
                if winrate>0.98:
                    print('超大牌必须迷惑对手') 
                    return (2,0)
                if winrate>0.84: 
                    print('必要的价值下注')
                    return (3,3)
                if unconnectFlop(Sit) and (Sit.myseat-Sit.position)%6>2: 
                    print('看起来翻牌不大像我的范围')
                    return (2,0)
                return (3,0)
            #我已经做了半池下注，对手仍然加注我
            if Sit.betlist[Sit.myseat]>Sit.oldpot/2.1 :
                print('虽然落后也要拼命')
                if Sit.callchip<Sit.oldpot/2:
                    print('对手仍然加注我')
                    if winrate>0.98: return (3,4)
                    if winrate>0.91: return (2,0)
                    if Sit.callchip/Sit.potsize<0.14 and winrate>0.7: 
                        print('赔率太好，不用想了，当他诈唬')
                        return (2,0)
                    if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                    return (0,0)
                if Sit.callchip>=Sit.oldpot/2 and Sit.callchip<=Sit.oldpot*1.1:
                    print('我在前位半池下注，后位加注我，我顶对或超对可以跟注一下')
                    if winrate>0.98: return (3,4)
                    if winrate>0.89: return (2,0)
                    if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                    return (0,0)
                if Sit.callchip>Sit.oldpot*1.1:
                    #顶对顶踢脚，我谁都不怕
                    print('超POT下注，只有超大牌才打光算了')
                    if winrate>0.98: return (3,4)
                    if winrate>0.9: return (2,0)
                    if Sit.potsize/Sit.callchip>2.9 and (IsDrawFlush(myhand) or IsDrawStraight(myhand)): return (2,0)
                    return (0,0)
            #我没有做下注，或者我下注很小，对手下注我
            elif Sit.betlist[Sit.myseat]<=Sit.oldpot/2.1 :
                print('我没有做下注，或者我下注很小，对手下注我')
                if Sit.callchip<Sit.oldpot/2:
                    if winrate>0.98: 
                        print('真正的大牌跟注就行')
                        return (2,0)
                    if winrate>0.9: return (3,3)
                    if winrate>0.8: 
                        print('顶对以上跟一下吧，没必要这么大的底池')
                        return (2,0)
                    if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                    return (0,0)
                if Sit.callchip>=Sit.oldpot/2 and Sit.callchip<=Sit.oldpot:
                    print('我在前位，最后一个CBET了，我中对以上招架一下')
                    if winrate>0.98: 
                        print('真正的大牌跟注就行')
                        return (2,0)
                    if winrate>0.9: return (3,3)
                    if winrate>0.8: return (3,3)
                    if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
                    return (0,0)
                if Sit.callchip>Sit.oldpot:
                    #顶对顶踢脚，我谁都不怕
                    if winrate>0.98: 
                        print('真正的大牌跟注就行')
                        return (2,0)
                    if winrate>0.92: return (3,3)
                    if Sit.potsize/Sit.callchip>3 and (IsDrawFlush(myhand) or IsDrawStraight(myhand)): return (2,0)
                    return (0,0)
        
    elif leftman>2:
        #我在后位没人下注，多人需要两次确认
        if Sit.callchip==0:
            if MyTurn(Sit)<leftman:
                #多人底池前位还是需要主动一点，
                # 0206 顶对大踢脚才主动，小踢脚还是保守一点
                if winrate>0.88: return (3,3)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (2,0)
            if MyTurn(Sit)==leftman:
                #多人底池后位还是需要主动一点，
                # 0206 多人底池后位可以凶一点点
                if winrate>0.85: return (3,3)
                if IsDrawFlush(myhand) or IsDrawStraight(myhand): return (3,3)
            return (2,0)
        elif Sit.callchip<Sit.oldpot/1.8:
            if winrate>0.95: return (3,3)
            if IsDrawFlush(myhand) or IsDrawStraight(myhand): 
                print('多人底池听牌不宜太凶，因为对手全部弃牌概率不高，而CBET是纯诈唬的概率也不高')
                return (2,0)
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
        
#如果翻牌中牌的可能性小
def unconnectFlop(Sit):
    pubcardlist=getPubList(Sit)
    #三张都小于8，而且是彩虹面
    if getHighCard(pubcardlist)<=8 and len(SameSuit(pubcardlist))<2:
        return True
    return False
            