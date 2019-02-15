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
from reader import LastManAfterFlop

#新的翻前决策函数
# def beforeFlopDecision2(Sit,callchip):
#     myhand=getMyHand(Sit)
#     #如果是所有人弃牌到我，我使用openrange
#     if IsFirst(Sit) and IsOpenRange(Sit):
#         return (3,2)
    
#     #如果前面有1个人加注，我使用callrange来call,使用3betRange来3bet
#     if getRaiseman(Sit)>=1:
#         if isCallRange(myhand,Sit.myseat): return (3,2)
#         if is3betRange(myhand,Sit.myseat): return (3,3)
#         return (0,0)

#     #如果前面有人3bet，我使用4betRange来4bet
#     if get3Betman(Sit)>=1:
#         if is4betRange(myhand,Sit.myseat): return (3,4)
#         return (0,0)
#     return (0,0)








#新写一个翻前决策，把疯狂的全下都去掉先
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
                print('UTG是否开局')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                #0214如果钱多可以打得松一点，钱少就只能紧
                if Sit.chiplist[Sit.myseat]>150*Sit.bb:
                    if(InTryRange(myhand)):
                        #筹码比较多，有钱偷
                        return (3,2)
                    if(QuiteGood(myhand)):
                        #UTG做一个经常加注的实验
                        return (0,0)
                    
            #如果是MP
            if (Sit.position-Sit.myseat)%6==2:
                print('MP是否开局')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                #0214如果钱多可以打得松一点，钱少就只能紧
                if Sit.chiplist[Sit.myseat]>150*Sit.bb:
                    if(InTryRange(myhand)):
                        return (3,2)
                if(QuiteGood(myhand)):
                #MP做一个经常加注的实验
                    return (0,0)
                if(InTryRange(myhand)):
                    return (0,0)
                if(InStealRange(myhand)):
                    return (0,0)
            #如果是CO
            if (Sit.position-Sit.myseat)%6==1:
                print('CO是否开局')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                #0214如果钱多可以打得松一点，钱少就只能紧
                if Sit.chiplist[Sit.myseat]>150*Sit.bb:
                    if(InTryRange(myhand)):
                        #print(InTryRange(myhand))
                        return (3,2)
                    #0204,CO放宽范围的实验，CO位还是不能太松
                    if QuiteGood(myhand) and leftman==4: 
                        return (0,0)
            #如果是BTN
            if (Sit.position-Sit.myseat)%6==0:
                print('BTN无人入池')
                if(InSuperRange(myhand)): 
                    return (3,2)
                if(InOpenRange(myhand)):
                    return (3,2)
                #0214，如果钱多可以打得松一点
                if Sit.chiplist[Sit.myseat]>150*Sit.bb:
                    if InBtnOpen(myhand):
                        print('按钮位OPEN的牌')
                        return (3,2)
                    if(InTryRange(myhand)):
                        return (3,2)
                    if QuiteGood(myhand): 
                        #print('执行到这里了吗？')
                        return (0,0)
                if leftman==3: return (0,0)
                return (0,0)
        if callchip<Sit.bb :
            #如果是小盲
            if callchip==Sit.bb/2:
                if leftman==2 and (Sit.myseat-Sit.position)%6==1:
                    print('小盲单挑大盲')
                    if InSuperRange(myhand): 
                        return (3,2)
                    if InOpenRange(myhand):
                        return (3,2)
                    #0204做一个永远加注的实验
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
                        return (2,0)
                    if InTryRange(myhand):
                        return (0,0)
                
                #print('小盲默认要偷')
                #return (3,0)
            #如果是大盲，只剩2个人，不发起攻击，碰运气
            if callchip==0 and leftman==2 and (Sit.myseat-Sit.position)%6==2:
                print('大盲,只剩2人，无人加注')
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
                return (2,0)
                
        
        #如果有人加注了，但还不是很大
        if callchip>=Sit.bb and callchip<=6*Sit.bb and Sit.betlist[Sit.myseat]<2*Sit.bb:
            #print('测试到了这里')
            print('跟第一次加注的情况')
            if (Sit.position-Sit.myseat)%6==3 :
                print('UTG跟加注')
                if InSuperRange(myhand): return (3,3)
                return (0,0)
            if (Sit.position-Sit.myseat)%6==2 :
                print('MP跟加注')
                if InSuperRange(myhand): return (3,3)
                if InMPCallOpen(myhand): return (2,0)
                return (0,0)
            if (Sit.position-Sit.myseat)%6==1:
                print('CO跟加注')
                if InSuperRange(myhand): return (3,3)
                if InCoCallOpen(myhand): return (2,0)
                return (0,0)
            #按钮位，跟加注
            if (Sit.position-Sit.myseat)%6==0:
                if Sit.betlist[Sit.myseat]>0:
                    print('btn跟别人再加注')
                    if leftman==2:
                        if InSuperRange(myhand): return (3,3)
                        #AK在BTN位3BET对手，表示我也会3BET
                        if InBB3Bet(myhand): return (3,3)
                        #0205，BTN也不能太弱，被大盲小盲一3BET就走
                        if InBtnCall3Bet(myhand): return (2,0)
                        return (0,0)
                else:
                    #0205，这里是个BUG
                    print('btn跟多人的起始加注')
                    
                    if leftman>4:
                        if InSuperRange(myhand): return (3,3)
                        if InCoCallOpen(myhand): return (2,0)
                        if InBtnCall3Bet(myhand): return (2,0)
                        return (0,0)
            #小盲位跟加注
            if (Sit.myseat-Sit.position)%6==1:
                print('小盲跟加注')
                if InSuperRange(myhand): return (3,3)
                if InBB3Bet(myhand): 
                    print('小盲位置不利只能加注')
                    return (3,3)
                if sbCallRange(myhand): return (0,0)
                      
            #大盲位跟加注
            if (Sit.myseat-Sit.position)%6==2:
                print('大盲位跟加注')
                if InSuperRange(myhand): return (3,3)
                if InBB3Bet(myhand) and MyTurn(Sit)<leftman: 
                    print('大盲位置不利只能3BET')
                    return (3,3)
                if InOpenRange(myhand): 
                    if leftman<=2 and MyTurn(Sit)==1: return (2,0)
                    else: return (2,0)
                if leftman==2:
                    print('这里位置有错误？',MyTurn(Sit))
                    if MyTurn(Sit)==2: 
                        print('对抗小盲有位置优势')
                        if InBBvsSb(myhand):  return (2,0)
                    elif InTryRange(myhand):
                        print('对抗一个玩家，保卫盲注')
                        return (0,0)
                #这个也是测试用的，不一定好
                if InTryRange(myhand) and leftman>2: 
                    print('底池赔率还行，进去试试')
                    return (0,0)
        if callchip>=5*Sit.bb and Sit.betlist[Sit.myseat]<=4*Sit.bb:
            print('我被3BET了')
            if CallRange(myhand): return (3,3)
            if leftman==2 and MyTurn(Sit)==2 and Sit.myseat==Sit.position: return (0,0)
            if leftman==2 and MyTurn(Sit)==2 and InTryRange(myhand): return (0,0)
            if leftman==2 and InOpenRange(myhand) and MyTurn(Sit)==2: return (0,0)
            if InOpenRange(myhand) and Sit.potsize/callchip>3: return (0,0) 
            if QuiteGood(myhand) and Sit.potsize/callchip>5: return (0,0)
            #还是要认怂，这么凶的人少见
            #if InOpenRange(myhand) and MyTurn(Sit)==1: return (3,4)
            #if InTryRange(myhand): return (2,0)
            return (0,0)
        #底池赔率可以，怎么都搞
        if callchip>=10*Sit.bb and Sit.betlist[Sit.myseat]<8*Sit.bb: 
            if InSuperRange(myhand): return (3,3)
            if InOpenRange(myhand) and Sit.potsize/callchip>5: return (2,0)
            if InStealRange(myhand) and Sit.potsize/callchip>7: return (2,0)
            return (0,0)
        if callchip>6*Sit.bb and Sit.betlist[Sit.myseat]>=8*Sit.bb:
            print('我3BET后被4BET')
            if OnlyAAKK(myhand): return (3,4)
            #AK不能怂
            if InBB3Bet(myhand): return (3,4)
            if callchip/Sit.potsize<0.3 and InSuperRange(myhand) : return (2,0)
            return (0,0)
        #0214补一下，3人底池怎么会走不到这里了
        #如果底池赔率已经小于0.16了，怎么都跟到底了，别想了
        if callchip/Sit.potsize<0.16: 
            print('反正套池了，全部打光，啥也别想了')
            return (2,0)
        
        if callchip==0 : return (2,0)
        
    return (0,-1)

#大盲需要3BET威胁对手的牌
def InBB3Bet(myhand):
    #AK位置不利可以直接3BET
    if myhand[0].num+myhand[1].num==27 : return True

#大盲对抗小盲的，保卫大盲的牌
def InBBvsSb(myhand):
    #口袋对
    if myhand[0].num==myhand[1].num: return True
    #带AKQ的同花
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=12 or myhand[1].num>=12): return True
    #同花连牌，54以上
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1 and myhand[0].num+myhand[1].num>=9: return True 
    #两张高牌
    if myhand[0].num+myhand[1].num>=24: return True
    #隔一张同花连牌，68以上
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==2 and myhand[0].num+myhand[1].num>=14 : return True
    #不同花的两张连牌，67以上
    if abs(myhand[0].num-myhand[1].num)==1 and myhand[0].num+myhand[1].num>=13: return True
    #带A的牌
    if (myhand[0].num>=14 or myhand[1].num>=14) : return True
    #带K的牌
    if (myhand[0].num>=13 or myhand[1].num>=13) and myhand[0].num+myhand[1].num>=19 : return True
    return False

#BTN位OPEN的牌
def InBtnOpen(myhand):
    #口袋对
    if myhand[0].num==myhand[1].num: return True
    #带AK的同花
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=13 or myhand[1].num>=13): return True
    #同花连牌，67以上
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1 and myhand[0].num+myhand[1].num>=13: return True 
    #两张同花高牌
    if myhand[0].num+myhand[1].num>=23 and abs(myhand[0].num-myhand[1].num)<=2 and myhand[0].suit==myhand[1].suit: return True
    #正常两张大牌
    if myhand[0].num+myhand[1].num>=25: return True
    #隔一张同花连牌，8T以上，不能太松
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==2 and myhand[0].num+myhand[1].num>=18 : return True
    #做一个按钮永远偷的实验
    return False

def InBtnCall3Bet(myhand):
    #口袋对
    if myhand[0].num==myhand[1].num: return True
    #同花连牌，67以上
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1 and myhand[0].num+myhand[1].num>=13: return True 
    #AK可以call
    if myhand[0].num+myhand[1].num==27: return True
    return False


#超级厉害
def OnlyAAKK(myhand):
    if myhand[0].num==myhand[1].num and myhand[0].num>=13: 
        print ('AAKK跟人推光')
        return True
    return False

#厉害的
def InSuperRange(myhand):
    
    if myhand[0].num==myhand[1].num and myhand[0].num>=12: 
        print ('是超级大牌')
        return True
    #AK也当超级大牌打
    #if myhand[0].num+myhand[1].num>=27: return True
    #else : return False
    return False

#小盲可以跟注的牌
def sbCallRange(myhand):
    print ('判断是否小盲可以跟注的牌')
    if myhand[0].num==myhand[1].num: return True
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=14 or myhand[1].num>=14): return True
    if myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=17 and  abs(myhand[0].num-myhand[1].num)==1: return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1 : return False
    if myhand[0].num+myhand[1].num>=25 and (myhand[0].num>=14 or myhand[1].num>=14): return True
    return False

#可以在CO跟加注的牌
def InCoCallOpen(myhand):
    #口袋对
    if myhand[0].num==myhand[1].num: return True
    #AK,AQ
    if myhand[0].num+myhand[1].num>=26: return True
    #同花连张结构牌
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1: return True

#可以在MP位跟加注的牌
def InMPCallOpen(myhand):
    #口袋对
    if myhand[0].num==myhand[1].num: return True
    #AK,AQ
    if myhand[0].num+myhand[1].num>=26: return True
    #同花连张结构牌
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1 and myhand[0].num+myhand[1].num>=21: return True
    return False

#前位可以开局的
def InOpenRange(myhand):
    #print ('判断是否前位开局牌')
    if myhand[0].num==myhand[1].num and myhand[0].num>6: return True
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=14 or myhand[1].num>=14) and myhand[0].num+myhand[1].num>=24: return True
    #KQ,KJs，别的不玩
    if myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=24 : return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1 : return False
    #KQ，AJ可以前位开局，但要小心
    if myhand[0].num+myhand[1].num>=25: return True
     
    return False

#CO位可以开局的
def InTryRange(myhand):
    #print('判断是否CO位开局')
    #口袋对
    if myhand[0].num==myhand[1].num: return True
    #带AK的同花
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=13 or myhand[1].num>=13): return True
    #同花连牌，78以上
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1 and myhand[0].num+myhand[1].num>=15: return True 
    #两张高牌
    if myhand[0].num+myhand[1].num>=24: return True
    #隔一张同花连牌，8T以上
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==2 and myhand[0].num+myhand[1].num>=18 : return False
    return False

#前40%的牌，任何两张能打配合的牌
def QuiteGood(myhand):
    #print('判断是否BTN位可以开局的牌')
    if myhand[0].num==myhand[1].num: return True
    if myhand[0].suit==myhand[1].suit and (myhand[0].num>=13 or myhand[1].num>=13): return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1: return True
    #if myhand[0].num+myhand[1].num>=24: return True
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==2: return True
    if myhand[0].num+myhand[1].num>=23: return True
    #带A带K的牌
    if (myhand[0].num>=13 or myhand[1].num>=13): return True
    #两张大牌连张
    if abs(myhand[0].num-myhand[1].num)==1 and myhand[0].num+myhand[1].num>=17: return True
    if myhand[0].suit!=myhand[1].suit and abs(myhand[0].num-myhand[1].num)>=3 and myhand[0].num+myhand[1].num<23: return False
    
    return False


#偷的范围
def InStealRange(myhand):
    if myhand[0].suit!=myhand[1].suit and abs(myhand[0].num-myhand[1].num)>=3 and myhand[0].num+myhand[1].num<=23: return False
    return True

#可以跟注的范围
def CallRange(myhand):
    if myhand[0].num==myhand[1].num and myhand[0].num>=12: return True
    return False
