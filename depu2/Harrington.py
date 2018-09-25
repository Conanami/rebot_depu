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
def DontLikeRate(Sit):
    wholehand=getMyHand(Sit)
    wholehand=wholehand+Sit.cardlist
    rtRate=0
    #转牌我不想看见的牌
    if getPubnum(Sit)==3 :
        #我没有同花听牌，外面也没有同花听牌
        if IsDrawFlush(wholehand)==False :
            if len(SameSuit(Sit.cardlist))<2: 
                nowrate=dealer.winRate(wholehand)
                nextrate=calcuNumRate(wholehand)
                print('Now Rate:'+str(nowrate))
                print('Next Rate:'+str(nextrate))
                print(nextrate-nowrate)
            #翻牌有同花可能
            if len(SameSuit(Sit.cardlist))==2:
                nowrate=dealer.winRate(wholehand)
                nextrate=calcuNumRate(wholehand)-0.15
                print('Now Rate:'+str(nowrate))
                print('Next Rate:'+str(nextrate))
                print(nextrate-nowrate)
        if IsDrawStraight(wholehand)==True:
            #公共牌为3张
            if len(SameSuit(Sit.cardlist))==3:
                nowrate=dealer.winRate(wholehand)
                nextrate=calcuNumRate(wholehand)
                print('Now Rate:'+str(nowrate))
                print('Next Rate:'+str(nextrate))
                print(nextrate-nowrate)
            if len(SameSuit(Sit.cardlist))==2:
                nowrate=dealer.winRate(wholehand)
                nextrate=calcuNumRate(wholehand)+0.15
                print('Now Rate:'+str(nowrate))
                print('Next Rate:'+str(nextrate))
                print(nextrate-nowrate)
                



