'''reader.py主要是对识别到的信息进行二次加工'''

import read_pokerstar
import dealer
import copy
from dealer import printCard
from dealer import card
from dealer import getLeftNumCardCnt


#得到目前的公共牌数量，对外
def getPubnum(rtSit):
    #print("公共牌张数:"+str(len(rtSit.cardlist)))
    return len(rtSit.cardlist)

#得到一对一时候牌的胜率,得到目前状态，对外
def calcuWinrate(rtSit):
    mycardlist=getMyHand(rtSit)
    mycardlist=mycardlist+rtSit.cardlist
   
    return dealer.winRate(mycardlist)

#得到后面一张牌的胜率
def calcuNumRate(wholecardlist,suit=0):
    cnt=0
    winRate=0
    for i in range(2,15):
        tmpCardList=copy.copy(wholecardlist)
        tmpCardList.append(card(suit,i))
        tmpWinRate=dealer.winRate(tmpCardList)
        leftCardCnt=getLeftNumCardCnt(i,wholecardlist)
        winRate=winRate+tmpWinRate*leftCardCnt
        cnt=cnt+leftCardCnt
    return winRate/cnt


        


#得到手牌，对外
def getMyHand(rtSit):
    myhand=[]
    myhand.append(rtSit.handlist[rtSit.myseat][0])
    myhand.append(rtSit.handlist[rtSit.myseat][1])
    #printCard(myhand)
    return myhand
    

#得到还剩几个人，对外
def getSurvivor(rtSit):
    quitCnt=0
    survivorCnt=0
    for i in range(6):
        #去掉既没有下注，又没有筹码的人
        if(rtSit.betlist[i]<0 and rtSit.chiplist[i]<0):
            quitCnt=quitCnt+1
        else:
            survivorCnt=survivorCnt+1
    return quitCnt,survivorCnt

#得到还有几个人没有动作
def getWaitingman(rtSit):
    if len(rtSit.cardlist)==0 :
        #如果翻前没有人加注，则我之后到大盲还有几个人
        if(max(rtSit.betlist)==rtSit.bb):
            #如果在翻前，那么用大盲注的人，减去我的位置
            if rtSit.position+2>5: bbpos=rtSit.position-4
            else: bbpos=rtSit.position+2
            for i in range(bbpos,bbpos+6):
                ri=i%6
                if rtSit.betlist[ri]==rtSit.bb:
                    bbpos=ri
                    break
            #如果我就是大盲，返回0个人
            cnt=0
            if rtSit.myseat==ri: return cnt
            if rtSit.myseat<ri:
                for i in range(rtSit.myseat+1,ri+1):
                    if(rtSit.chiplist[i]>-1):
                        cnt=cnt+1
                return cnt
            if rtSit.myseat>ri:
                for i in range(rtSit.myseat-5,ri+1):
                    if(rtSit.chiplist[i]>-1):
                        cnt=cnt+1
                return cnt

            return 6
        #如果翻前有人加注，则假设再没人加注，有几个人等待行动
        if(max(rtSit.betlist)>rtSit.bb):
            cnt=0
            for i in range(1,5):
                tmppos=(rtSit.myseat+i)%6
                if(rtSit.chiplist[tmppos]>-1 and rtSit.betlist[tmppos]<max(rtSit.betlist)):
                    cnt=cnt+1
            return cnt
    
    if len(rtSit.cardlist)>=3 :
        #如果在翻后，那么用BTN位置，减去我的位置，再减去弃牌的人
        #如果没有人下注
        if(max(rtSit.betlist)==rtSit.betlist[rtSit.myseat]):
            cnt=0
            for i in range(rtSit.myseat+1,rtSit.position+1):
                tmppos=i%6
                if rtSit.chiplist[i]>-1:
                    cnt=cnt+1
            return cnt
        #如果翻后有人下注
        if(max(rtSit.betlist)>rtSit.betlist[rtSit.myseat]):
            cnt=0
            for i in range(1,5):
                tmppos=(rtSit.myseat+i)%6
                if(rtSit.chiplist[tmppos]>-1 and rtSit.betlist[tmppos]<max(rtSit.betlist)):
                    cnt=cnt+1
            return cnt
    return 'error'

#返回全下的对手位置
def IsAllIn(rtSit):
    for i in range(6):
        if i!=rtSit.myseat and rtSit.chiplist[i]<=0 and rtSit.betlist[i]>0:
            return i
    return None

#是否有位置优势
def IsAfter(rtSit):
    cntme=0
    for i in range(rtSit.position+1,rtSit.position+6):
         tmpi=i%6
         if(rtSit.chiplist[tmpi]>=0 and tmpi!=rtSit.myseat and cntme==0): return True
         if(tmpi==rtSit.myseat): cntme=1
    return False

#得到公共牌，对外
def getPubList(rtSit):
    return rtSit.cardlist


