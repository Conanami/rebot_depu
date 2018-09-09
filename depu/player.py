#import time
import dealer
import math
import random
#import readpot
from dealer import IsDrawFlush
from dealer import IsDrawStraight

#得到目前的公共牌数量
def getPubnum(rtSit):
    mycardlist=[]
    opplist=[]
    for tmpcard in rtSit.cardlist:
        mycardlist.append(tmpcard)
    for i in range(2,len(mycardlist)):
        opplist.append(mycardlist[i])
    return len(opplist)

#得到一对一时候牌的胜率,得到目前状态
def calcuWinrate(rtSit):
    mycardlist=[]
    opplist=[]
    for tmpcard in rtSit.cardlist:
        mycardlist.append(tmpcard)
    for i in range(2,len(mycardlist)):
        opplist.append(mycardlist[i])
   
    # dealer.printCard(mycardlist)
    # dealer.printCard(opplist)
    return dealer.winRate(mycardlist)

#得到还剩几个人
def getSurvivor(rtSit):
    quitCnt=0
    survivorCnt=0
    for i in range(6):
        #去掉弃牌和位子是空的人
        if(rtSit.statuslist[i]==0 or (rtSit.statuslist[i] is None and rtSit.chiplist[i]<=0 and rtSit.betlist[i]<=0)):
            quitCnt=quitCnt+1
        else:
            survivorCnt=survivorCnt+1
    return quitCnt,survivorCnt

#得到需要跟注的筹码量
def getCallchip(rtSit):
    mybet=0
    if(rtSit.betlist[0]>0): mybet=rtSit.betlist[0]
    rtchip= max(rtSit.betlist)-mybet
    if(rtchip<0): return 0
    else: return rtchip

#返回值第一个是决定，0弃牌，1过牌，2跟注，3加注，第二个是准备放入的筹码量，只有在2，3的时候有值，
#待整理的函数
def afterFlopDecision(pubnum,singleWinrate,finalWinrate,leftman,rtSit):
    print("potsize:"+str(rtSit.potsize))
    print("blind:"+str(rtSit.bb))
    print("callchip:"+str(rtSit.callchip))
    if(pubnum==0):
        return "before Flop"
    elif(pubnum>=1 and pubnum<=3):
        #钓到大鱼
        if(finalWinrate>=0.98 and rtSit.callchip>=rtSit.potsize/2): return (3,4)
        #胜率比较高
        if(finalWinrate>0.95 and rtSit.callchip<(rtSit.potsize-rtSit.callchip) and rtSit.potsize<=20*rtSit.bb): return (3,3)
        #比较大
        #如果遭遇对手大额反加注，还是要弃牌的
        if(rtSit.betlist[0]>5*rtSit.bb and max(rtSit.betlist)>3*rtSit.betlist[0] and singleWinrate<0.94): return (0,0)
        if(finalWinrate>=0.7 and rtSit.callchip<rtSit.potsize/3 and rtSit.potsize<=20*rtSit.bb): return (3,2)
        #有一定的胜率不轻易弃牌，伪装自己
        if(singleWinrate>=0.92):
            if(rtSit.callchip==0):
                if(leftman>2): return (3,1)
                else:return (2,0)
            elif(rtSit.callchip<rtSit.potsize-rtSit.callchip): return (2,0)
        
        
        #偶尔下注半个底池偷
        if(leftman<=3 and rtSit.callchip==0 and rtSit.potsize/rtSit.bb<15 and random.random()>0.7): return (3,1) 
        #底池赔率合适，坚决跟
        if(rtSit.callchip/(rtSit.potsize+rtSit.callchip)<finalWinrate and rtSit.potsize<20*rtSit.bb): return (2,rtSit.callchip)      
        #底池赔率不合适
        if(rtSit.callchip/(rtSit.potsize+rtSit.callchip)>finalWinrate): return (0,0) 
        #过牌看牌
        if(rtSit.callchip==0): return (2,0)
        return (0,0)
    elif(pubnum==4):
        #超大牌则陷阱
        if(singleWinrate>=0.97): return (2,0)
        #比较大则下一个底池
        if(finalWinrate>=0.9 and rtSit.potsize<=20*rtSit.bb): return (3,3)
        #下注遭遇强烈反加注
        if(rtSit.betlist[0]>5*rtSit.bb and max(rtSit.betlist)>3*rtSit.betlist[0]):
            if(finalWinrate<0.93): return (0,0)
            else: return (3,4)
        if(rtSit.betlist[0]>5*rtSit.bb and max(rtSit.betlist)>3*rtSit.betlist[0] and singleWinrate<0.94): return (0,0)
        if(finalWinrate>=0.9 and rtSit.callchip<=rtSit.potsize/2): return (2,0)
        if(finalWinrate>=0.75 and rtSit.callchip<=rtSit.potsize/3): return (2,0)
        if(finalWinrate>=0.6 and rtSit.callchip==0 and random.random()>0.2 and rtSit.potsize<=20*rtSit.bb): return (3,1)
        #偶尔下注半个底池偷
        if(rtSit.callchip==0 and leftman<=3 and rtSit.potsize/rtSit.bb<=15 and random.random()>0.5): return (3,1)
        
        #胜率还占优
        if(rtSit.callchip/(rtSit.potsize+rtSit.callchip)<finalWinrate and rtSit.callchip<=rtSit.potsize/3 and rtSit.potsize<=20*rtSit.bb): 
            return (2,rtSit.callchip)
               
        #转牌弱一点了
        if(rtSit.callchip/rtSit.potsize>finalWinrate and rtSit.callchip/rtSit.bb>20): return (0,0)
        
        #过牌看牌
        if(rtSit.callchip==0): return (2,0)
        return (0,0)
    elif(pubnum==5):
        if(finalWinrate>=0.98): return (3,4)
        if(finalWinrate>=0.75 and rtSit.callchip==0 and random.random()>0.2 and rtSit.potsize<=20*rtSit.bb): return (3,1)
        #下注遭遇强烈反加注
        if(rtSit.betlist[0]>5*rtSit.bb and max(rtSit.betlist)>3*rtSit.betlist[0]):
            if(finalWinrate<0.93): return (0,0)
            else: return (3,4)
        #偶尔下注半个底池偷
        if(rtSit.callchip==0 and leftman==2 and rtSit.potsize/rtSit.bb<=20 and random.random()>0.6): return (3,1)
        #被反加注就不用硬扛了，最后不支付
        if(rtSit.callchip/rtSit.potsize<finalWinrate and finalWinrate>0.7 and rtSit.potsize<=20*rtSit.bb): return (2,rtSit.callchip)
        if(rtSit.callchip/rtSit.potsize>finalWinrate and rtSit.callchip>30*rtSit.bb): return (0,0)
        
        #过牌看牌
        if(rtSit.callchip==0): return (2,0)
        return (0,0)
    return (0,-1)

#翻前决策
def beforeFlopDecision(Sit,callchip):
    myhand=[]
    pubcnt=0
    leftman=getSurvivor(Sit)
    for i in range(len(Sit.cardlist)):
        if(i<2):
            myhand.append(Sit.cardlist[i])
        elif(i>=2):
            pubcnt=pubcnt+1
    #如果中间有牌，或者两张牌没有读出来，则返回弃牌
    if(pubcnt==0 and len(myhand)==2):
        
        if(InSuperRange(myhand)):
            if(callchip==0): return (3,4)
            if(callchip>0 and callchip<Sit.bb*3): return (3,4)
            if(callchip>=Sit.bb*3): return (3,4)
        
        if(InOpenRange(myhand) and callchip==0): return (2,random.randint(1,2))
        #如果是开局牌，则可以跟别人
        if(InOpenRange(myhand) and callchip>0 and callchip<=Sit.bb*3): 
            if(callchip==Sit.bb): return (2,1)
            else: return (2,callchip)
        #底池赔率合适，啥牌都可以玩
        if(callchip/Sit.potsize<0.15 and callchip<=3*Sit.bb): return (2,callchip)
        #小盲单挑大盲可以玩
        if(callchip/Sit.potsize<0.5 and callchip<=Sit.bb and leftman[1]<=2): 
            if(random.random()>0.5): return (3,1)
            else: return (2,callchip)
        #两个人单挑
        if(leftman[1]==2 and callchip>=3*Sit.bb):
            if(random.random()>0.96): return (2,1)
            else: return (0,0)
        #如果是大盲白看牌
        if(callchip==0): return (2,0)
        return (0,0)
    else:
        return (0,-1)

#入局玩的牌
def InOpenRange(myhand):
    #print(str(myhand[0].suit)+","+str(myhand[0].num)+"|"+str(myhand[1].suit)+","+str(myhand[1].num))
    if(InSuperRange(myhand)): return False
    #两张高牌
    if(myhand[0].num+myhand[1].num>=22): return True
    #带AK的同花
    if(myhand[0].suit==myhand[1].suit and (myhand[0].num>=13 or myhand[1].num>=13)): return True
    #口袋对
    if(myhand[0].num==myhand[1].num): return True
    #大的连牌和中的口袋对
    if(abs(myhand[0].num-myhand[1].num)<=2 and myhand[0].num>=8 and myhand[1].num>=8): return True
    #同花连牌
    if(abs(myhand[0].num-myhand[1].num)<=3 and myhand[0].suit==myhand[1].suit and (myhand[0].num>=9 or myhand[1].num>=9)): 
        return True
    return False

#只有AA,KK,QQ,JJ,TT跟人推
def InSuperRange(myhand):
    if(myhand[0].num==myhand[1].num and myhand[0].num>=10): return True
    else: return False

#做出决定
def makeDecision(rtSit):
    #得到要跟注多少筹码
    callchip=getCallchip(rtSit)
    if(callchip==0): callchip=rtSit.callchip
    #得到当前公共牌的数量
    pubnum=getPubnum(rtSit)
    finalDecision=(0,-1)
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
        print('我的胜率%.2f' % myWinrate)
        print('剩余人数%d ' % leftman)
        finalWinrate=math.pow(myWinrate,leftman-1)
        if(IsDrawFlush(rtSit.cardlist) and pubnum==3):
            print('同花听牌，胜率增加%.2f' % 0.18)
            finalWinrate=finalWinrate+0.18
        if(IsDrawStraight(rtSit.cardlist) and pubnum==3): 
            print('顺子听牌，胜率增加%.2f' % 0.16)
            finalWinrate=finalWinrate+0.16
        
        print('最后胜率%.2f' % finalWinrate)
        #翻牌后的决策
        mydecision=afterFlopDecision(pubnum,myWinrate,finalWinrate,leftman,rtSit)
        finalDecision=mydecision
    #如果要加注，要根据自己的筹码和底池的实际情况
    if(finalDecision[0]==3):
        #如果翻前，底池大小小于4个盲注，则一个底池下注是灰色
        if(rtSit.potsize<=4*rtSit.bb and pubnum==0):
            if(finalDecision[1]==3): 
                finalDecision=(3,2)
        #如果所有筹码小于要跟注的数量，那么直接allin
        if(rtSit.chiplist[0]<rtSit.callchip): finalDecision=(2,0)
        #如果筹码大于需要跟注的数量
        if(rtSit.chiplist[0]>=rtSit.callchip):
            #如果比2/3底池多，但是不到一个底池，则3，3变3，2
            if(finalDecision[1]==3 and rtSit.chiplist[0]>=0.66*rtSit.potsize and rtSit.chiplist[0]<rtSit.potsize):
                finalDecision=(3,2)
            #如果比1/2底池多，但是不到2/3个底池，则3，2变3，1
            if(finalDecision[1]==2 and rtSit.chiplist[0]>=0.5*rtSit.potsize and rtSit.chiplist[0]<0.66*rtSit.potsize):
                finalDecision=(3,1)
            #如果比1/2底池小，则只能选全下
            if(finalDecision[1]==1 and rtSit.chiplist[0]<0.5*rtSit.potsize):
                finalDecision=(3,4)
        #如果翻后底池比3个盲注还小，那就不能选择3，1和3，2，直接3，3
        if(rtSit.potsize<=3*rtSit.bb and pubnum>0):
            if(finalDecision[1]==1): finalDecision=(3,3)
            if(finalDecision[1]==2): finalDecision=(3,3)
    return finalDecision
