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


def makeDecision(rtSit):
    #得到还剩几个人
    leftman=getSurvivor(rtSit)

#判断前后两次读到的信息，是否同一手牌
def IsSameHand(Sit1,Sit2):
    #手里的牌要完全一样
    if Sit1.position==Sit2.position:
        if IsSameMyhand(Sit1,Sit2):
            #外面的公共牌要后面比前面多,而且露出来的要完全一样
            if getPubnum(Sit2)>=getPubnum(Sit1):
                if IsSameCardlist(Sit1.cardlist,Sit2.cardlist,min(len(Sit1.cardlist),len(Sit2.cardlist))):
                    return True
    else:
        return False
    return False

#手里的牌要一模一样
def IsSameMyhand(Sit1,Sit2):
    if Sit1.handlist[Sit1.myseat][0].equals(Sit2.handlist[Sit2.myseat][0]) \
        and Sit1.handlist[Sit1.myseat][1].equals(Sit2.handlist[Sit2.myseat][1]):
        return True
    return False

#外面看得见的公共牌也要一模一样
def IsSameCardlist(cardlist1,cardlist2,cnt):
    if cnt==0: return True
    if cnt>0:
        for i in range(cnt):
            if(cardlist1[i].equals(cardlist2[i])==False):
                return False
        return True

#我不想看见的牌
def DontLikeRate(Sit,nowRate):
    wholehand=getMyHand(Sit)
    wholehand=wholehand+Sit.cardlist
    rtRate=0
    nextRate=0
    #转牌我不想看见的牌
    if getPubnum(Sit)==3 or getPubnum(Sit)==4 :

        #我没有同花听牌，外面也没有同花听牌
        if IsDrawFlush(wholehand)==False :
            if len(SameSuit(Sit.cardlist))<2: 
                nextRate=calcuNumRate(wholehand,0)
                rtRate=nextRate-nowRate
            #翻牌有同花可能
            if len(SameSuit(Sit.cardlist))==2:
                #反正第四张只考虑不同花的，同花自己处理
                if SameSuit(Sit.cardlist)[0].suit<3: mysuit=3
                else: mysuit=0
                nextRate=calcuNumRate(wholehand,mysuit)-0.15
                rtRate=nextRate-nowRate
        if IsDrawFlush(wholehand)==True:
            #公共牌出现4张同花
            if len(SameSuit(Sit.cardlist))==4:
                if SameSuit(Sit.cardlist)[0].suit<3: mysuit=3
                else: mysuit=0
                nextRate=calcuNumRate(wholehand,mysuit)
                rtRate=nextRate-nowRate
            #公共牌出现3张同花
            if len(SameSuit(Sit.cardlist))==3:
                #print('0000')
                if SameSuit(Sit.cardlist)[0].suit<3: mysuit=3
                else: mysuit=0
                nextRate=calcuNumRate(wholehand,mysuit)
                rtRate=nextRate-nowRate
            #公共牌出现2张同花
            if len(SameSuit(Sit.cardlist))==2:
                if SameSuit(Sit.cardlist)[0].suit<3: mysuit=3
                else: mysuit=0
                nextRate=calcuNumRate(wholehand,mysuit)+0.15
                rtRate=nextRate-nowRate
    #返回下张牌的胜率
    print('变化率：'+str(nextRate)+","+str(rtRate))
    return nextRate,rtRate



