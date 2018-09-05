#import time
import dealer
import math
import random
#import readpot

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
    rtchip= rtSit.betlist[rtSit.betlist.index(max(rtSit.betlist))]-mybet
    if(rtchip<0): return 0
    else: return rtchip

#返回值第一个是决定，0弃牌，1过牌，2跟注，3加注，第二个是准备放入的筹码量，只有在2，3的时候有值，
def afterFlopDecision(pubnum,finalWinrate,callchip,potsize,leftman,mychip,bigblind):
    if(pubnum==0):
        return "before Flop"
    elif(pubnum==3):
        #胜率比较高
        if(finalWinrate>0.95 and callchip<(potsize-callchip)): return (3,3)
        #钓到大鱼
        if(finalWinrate>=0.98 and callchip>=potsize/2): return (3,4)
        if(callchip/potsize>finalWinrate): return (0,0)  
        #底池赔率合适，坚决跟
        if(callchip/potsize<finalWinrate): return (2,callchip)      
        #偶尔下注半个底池偷
        if(leftman<=3 and callchip==0 and potsize/bigblind<15 and random.random()>0.5): return (3,1)
        #过牌看牌
        if(callchip==0): return (2,0)
    elif(pubnum==4):
        if(finalWinrate>=0.98): return (3,4)
        if(callchip/potsize<finalWinrate and callchip<=potsize/4): return (2,callchip)
        if(callchip/potsize>finalWinrate and callchip/bigblind>20): return (0,0)
        #偶尔下注半个底池偷
        if(callchip==0 and leftman==2 and potsize/bigblind<=15 and random.random()>0.5): return (3,1)
        #过牌看牌
        if(callchip==0): return (2,0)
    elif(pubnum==5):
        if(finalWinrate>=0.98): return (3,4)
        if(callchip/potsize<finalWinrate and callchip<=potsize/4): return (2,callchip)
        if(callchip/potsize>finalWinrate): return (0,0)
        #偶尔下注半个底池偷
        if(callchip==0 and leftman==2 and potsize/bigblind<=15 and random.random()>0.5): return (3,1)
        #过牌看牌
        if(callchip==0): return (2,0)
        return (0,0)
    return (0,-1)

#翻前决策
def beforeFlopDecision(Sit,callchip):
    myhand=[]
    pubcnt=0
    for i in range(len(Sit.cardlist)):
        if(i<2):
            myhand.append(Sit.cardlist[i])
        elif(i>=2):
            pubcnt=pubcnt+1
    #如果中间有牌，或者两张牌没有读出来，则返回弃牌
    if(pubcnt==0 and len(myhand)==2):
        if(InOpenRange(myhand) and callchip==0): return (3,random.randint(1,3))
        if(InOpenRange(myhand) and callchip>0 and callchip<=4*Sit.bb): 
            return (2,callchip)
        #底池赔率合适，啥牌都可以玩
        if(callchip/Sit.potsize<0.13 and callchip<=3*Sit.bb and callchip>0): return (2,callchip)
        if(InSuperRange(myhand)):
            if(callchip==0): return (3,1)
            if(callchip>0 and callchip<Sit.bb*3): return (3,3)
            if(callchip>=Sit.bb*3): return (3,4)
        #如果是大盲白看牌
        if(callchip==0): return (1,0)
        return (0,0)
    else:
        return (0,-1)

#入局玩的牌
def InOpenRange(myhand):
    #print(str(myhand[0].suit)+","+str(myhand[0].num)+"|"+str(myhand[1].suit)+","+str(myhand[1].num))
    if(InSuperRange(myhand)): return False
    #两张高牌
    if(myhand[0].num+myhand[1].num>=22 and myhand[0].num>=10 and myhand[1].num>=10): return True
    #带A的同花
    if(myhand[0].suit==myhand[1].suit and (myhand[0].num==14 or myhand[1].num==14)): return True
    #大的连牌和中的口袋对
    if(abs(myhand[0].num-myhand[1].num)<=1 and myhand[0].num>=6): return True
    return False

#只有AA,KK,QQ跟人推
def InSuperRange(myhand):
    if(myhand[0].num==myhand[1].num and myhand[0].num>=12): return True
    else: return False

#做出决定
def makeDecision(rtSit):
    #得到要跟注多少筹码
    callchip=getCallchip(rtSit)
    if(callchip==0): callchip=rtSit.callchip
    #得到当前公共牌的数量
    pubnum=getPubnum(rtSit)
    #如果是翻牌前
    if(pubnum==0):
        return beforeFlopDecision(rtSit,callchip)
    elif(pubnum>=3):
        #计算当前牌的胜率
        myWinrate=calcuWinrate(rtSit)
        #得到当前还剩几个人在底池中
        leftman=getSurvivor(rtSit)[1]
        #胜率与人数的关系，人数越多，胜率越小
        print('我的胜率%.2f' % myWinrate)
        print('剩余人数%d ' % leftman)
        finalWinrate=math.pow(myWinrate,leftman-1)
        print('最后胜率%.2f' % finalWinrate)
        #翻牌后的决策
        mydecision=afterFlopDecision(pubnum,finalWinrate,callchip,rtSit.potsize,leftman,rtSit.chiplist[0],rtSit.bb)
        return mydecision
    return (0,-1)
