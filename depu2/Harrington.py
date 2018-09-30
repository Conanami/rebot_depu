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
#from player import beforeFlopDecision
from chiper import ClickControl
from dealer import cardtypeOf
from dealer import GetTopSame
from dealer import LikeStraight
from dealer import IsFlush
from reader import getWaitingman
from dealer import IsGunshotStraight
#做出决策
def makeDecision(rtSit):
    #得到公共牌的张数
    pubnum=getPubnum(rtSit)
    if pubnum==0:
        decision=(2,0)
        #decision=beforeFlopDecision(rtSit,callchip)
    if pubnum==3:
        decision=flopDecision(rtSit)
    if pubnum==4:
        decision=turnDecision(rtSit)
    if pubnum==5:
        decision=riverDecision(rtSit)
    return ClickControl(decision)

#翻牌决策
def flopDecision(Sit):
    #剩下几个人
    leftman=getSurvivor(Sit)[1]
    #得到手牌胜率
    winRate=calcuWinrate(Sit)
    #得到我的手牌
    myhand=getMyHand(Sit)
    #得到公共牌
    publist=Sit.cardlist
    #得到目前形成的牌
    mycardlist=myhand+publist
    #得到我的牌型
    cardtype=cardtypeOf(mycardlist)
    print('我的胜率%s' % winRate)

    if(leftman==2):
        print('翻后还剩2人')
        #2表示后行动
        if MyTurn(Sit)==2:
            #我在后位对手过牌
            if Sit.callchip==0:
                print('我在后面没人下注')
                #我有对，外面没有公对
                if cardtype==3 and cardtypeOf(publist)==2:
                    mypair=GetTopSame(mycardlist)
                    toppub=GetTopSame(publist)[0].num
                    #我是超对
                    if mypair[0].num>toppub and myhand[0].num==myhand[1].num:
                        return (3,3)
                    #我是顶对
                    if mypair[0].num==toppub:
                        return (3,3)
                    #我是小对
                    if mypair[0].num<toppub:
                        return (3,3)
                #外面牌有公对，我中了对
                if cardtype==6 and cardtypeOf(publist)==3:
                    return (3,3)
                #如果我中了两对
                if cardtype==6 and cardtypeOf(publist)==2:
                    #外面有危险的同花面，要重打
                    if len(SameSuit(publist))>=2:
                        return (3,3)
                    #外面有危险的顺子面，也要重打，结束战斗
                    if LikeStraight(publist)==True:
                        return (3,3)
                    #没有危险则80%加注，看上去像是正常牌
                    if random.random()>0.2 : return (3,1)
                    else: return (2,0)
                #如果我中了暗三条
                if cardtype==7 and myhand[0].num==myhand[1].num:
                    #外面有危险的同花面，要重打
                    if len(SameSuit(publist))>=2:
                        return (3,3)
                    #外面有危险的顺子面，也要重打，结束战斗
                    if LikeStraight(publist)==True:
                        return (3,3)
                    #没有危险则一半过牌，一半加半池，看上去像是正常牌
                    if random.random()>0.5 : return (3,1)
                    else: return (2,0)
                #如果我中了明三条
                if cardtype==7 and myhand[0].num!=myhand[1].num and cardtypeOf(publist)==3:
                    #外面有危险的同花面，要重打
                    if len(SameSuit(publist))>=2:
                        return (3,3)
                    #外面有危险的顺子面，也要重打，结束战斗
                    if LikeStraight(publist)==True:
                        return (3,3)
                    #没有危险则一半过牌，一半加半池，看上去像是正常牌
                    if random.random()>0.5 : return (3,1)
                    else: return (2,0)
                #如果我中了天顺以上牌力
                if cardtype==8:
                    #如果有听同花需要结束战斗
                    if len(SameSuit(publist))>=2:
                        return (3,3)
                    #则只有20%机会加注去掩盖牌力
                    if random.random()>0.8: return (3,1)
                    else: return (2,0)
                #如果我中了天同花,则肯定掩盖牌力，晚点打跑对方
                if cardtype==9:
                    if(myhand[0].num==14 or myhand[1].num==14):
                        return (2,0)
                    #如果不是A花，还是要防止再出一张同花的
                    else: return (3,3)
                #如果我中了葫芦以上牌力，肯定掩饰牌力
                if cardtype>9 and cardtypeOf(publist)!=7:
                    return (2,0)
                #如果我只是口袋对，外面是三条
                if cardtype==10 and cardtypeOf(publist)==7:
                    return (2,0)
                #如果是小牌，一半时间持续下注，让对手摸不准我
                if random.random()>0.4: return (3,1)
                else: return (2,0)

                return (2,0)
            #我还没有下注
            if Sit.betlist[Sit.myseat]<=0:    
                #前位对手下了一个小注
                if Sit.callchip<=Sit.potsize/3:
                    #我有对，外面没有公对
                    if cardtype==3 and cardtypeOf(publist)==2:
                        mypair=GetTopSame(mycardlist)
                        toppub=GetTopSame(publist)[0].num
                        #我是超对
                        if mypair[0].num>toppub and myhand[0].num==myhand[1].num:
                            return (3,3)
                        #我是顶对
                        if mypair[0].num==toppub:
                            if random.random()>0.5: return (2,0)
                            return (3,3)
                        #我是小对
                        if mypair[0].num<toppub:
                            return (2,0)
                    #外面牌有公对，我中了对
                    if cardtype==6 and cardtypeOf(publist)==3:
                        if random.random()>0.5: return (2,0)
                        else: return (3,3)
                    #如果我中了两对
                    if cardtype==6 and cardtypeOf(publist)==2:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,3)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,3)
                        #没有危险则80%加注，看上去像是正常牌
                        if random.random()>0.5 : return (3,1)
                        else: return (2,0)
                    #如果我中了暗三条
                    if cardtype==7 and myhand[0].num==myhand[1].num:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,3)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,3)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        return (2,0)
                    #如果我中了明三条
                    if cardtype==7 and myhand[0].num!=myhand[1].num and cardtypeOf(publist)==3:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,3)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,3)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        return (2,0)
                    #如果我中了天顺以上牌力
                    if cardtype==8:
                        #如果有听同花需要结束战斗
                        if len(SameSuit(publist))>=2:
                            return (3,3)
                        #则只有20%机会加注去掩盖牌力
                        if random.random()>0.8: return (3,1)
                        else: return (2,0)
                    #如果我中了天同花,则肯定掩盖牌力，晚点打跑对方
                    if cardtype==9:
                        if(myhand[0].num==14 or myhand[1].num==14):
                            return (2,0)
                        #如果不是A花，还是要防止再出一张同花的
                        else: return (3,3)
                    #如果我中了葫芦以上牌力，肯定掩饰牌力
                    if cardtype>9:
                        return (2,0)
                    
                    if IsGunshotStraight(mycardlist)>=1:
                        print('单挑小注，顺子听牌要跟')
                        return (2,0)
                    if IsDrawFlush(mycardlist) and myhand[1].suit==myhand[0].suit: 
                        print('单挑小注，同花跟')
                        return (2,0)
                    if IsDrawFlush(mycardlist) and len(SameSuit(publist))==3 and MyFlushTop(myhand,publist)>=10:
                        print('单挑小注，三张同花我有大于10跟')
                        return (2,0)
                    #如果是小牌，就根据底池赔率决定是否要跟注
                    if Sit.potsize/Sit.callchip>0.5/(winRate-0.5) and winRate>0.5: return (2,0)
                    return (0,0)
                
                '''单挑我有利位置，对手下了一个超过半池的注'''
                if Sit.callchip>Sit.potsize/3 and Sit.callchip<(Sit.potsize-Sit.callchip)*0.75:
                    print('单挑前面的对手下一个超过半池的注')
                    #我有对，外面没有公对
                    if cardtype==3 and cardtypeOf(publist)==2:
                        mypair=GetTopSame(mycardlist)
                        toppub=GetTopSame(publist)[0].num
                        #我是超对
                        if mypair[0].num>toppub and myhand[0].num==myhand[1].num:
                            return (3,3)
                        #我是顶对
                        if mypair[0].num==toppub:
                            if random.random()>0.5: return (2,0)
                            return (2,0)
                        #我是小对
                        if mypair[0].num<toppub:
                            return (2,0)
                    #外面牌有公对，我中了对
                    if cardtype==6 and cardtypeOf(publist)==3:
                        if random.random()>0.5: return (2,0)
                        else: return (2,0)
                    #如果我中了两对
                    if cardtype==6 and cardtypeOf(publist)==2:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #如果两对碰到大牌就认命
                        return (3,4)
                    #如果我中了暗三条
                    if cardtype==7 and myhand[0].num==myhand[1].num:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        return (2,0)
                    #如果我中了明三条
                    if cardtype==7 and myhand[0].num!=myhand[1].num and cardtypeOf(publist)==3:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        return (2,0)
                    #如果我中了天顺牌力
                    if cardtype==8:
                        #如果有听同花需要结束战斗
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #则只有20%机会加注去掩盖牌力
                        if random.random()>0.8: return (3,1)
                        else: return (2,0)
                    #如果我中了天同花,则肯定掩盖牌力，晚点打跑对方
                    if cardtype==9:
                        if(myhand[0].num==14 or myhand[1].num==14):
                            return (2,0)
                        #如果不是A花，还是要防止再出一张同花的
                        else: return (3,4)
                    #如果我中了葫芦以上牌力，肯定掩饰牌力
                    if cardtype>9:
                        return (2,0)
                    #如果是听顺，则对小加注跟注
                    if IsDrawStraight(mycardlist): return (2,0)
                    #如果是听花，我手里两张花，则跟注
                    if IsDrawFlush(mycardlist) and myhand[1].suit==myhand[0].suit: return (2,0)
                    #如果是听花，外面3张花，则我手里那张大于10跟注，小于10就看后面随机搞了
                    if IsDrawFlush(mycardlist) and len(SameSuit(publist))==3 and MyFlushTop(myhand,publist)>=10: return (2,0)
                    #如果是小牌，就根据底池赔率决定是否要跟注
                    if Sit.potsize/Sit.callchip>0.3/(winRate-0.7) and winRate>0.7: return (2,0)
                    return (0,0)
                #前位对手下了一个重注
                if Sit.callchip>=(Sit.potsize-Sit.callchip)*0.75 and Sit.callchip<(Sit.potsize-Sit.callchip)*1.5 :
                    #我有对，外面没有公对
                    if cardtype==3 and cardtypeOf(publist)==2:
                        mypair=GetTopSame(mycardlist)
                        toppub=GetTopSame(publist)[0].num
                        #我是超对
                        if mypair[0].num>toppub and myhand[0].num==myhand[1].num:
                            return (2,0)
                        #我是顶对
                        if mypair[0].num==toppub:
                            if random.random()>0.5: return (2,0)
                            return (2,0)
                        #我是小对
                        if mypair[0].num<toppub:
                            return (0,0)
                    #外面牌有公对，我中了对
                    if cardtype==6 and cardtypeOf(publist)==3:
                        if random.random()>0.5: return (2,0)
                        else: return (0,0)
                    #如果我中了两对
                    if cardtype==6 and cardtypeOf(publist)==2:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #如果两对翻牌就碰到大牌就认命
                        return (3,4)
                    #如果我中了暗三条
                    if cardtype==7 and myhand[0].num==myhand[1].num:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        return (3,4)
                    #如果我中了明三条
                    if cardtype==7 and myhand[0].num!=myhand[1].num and cardtypeOf(publist)==3:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        return (2,0)
                    #如果我中了天顺牌力
                    if cardtype==8:
                        #如果有听同花需要结束战斗
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #则只有20%机会加注去掩盖牌力
                        if random.random()>0.8: return (3,1)
                        else: return (2,0)
                    #如果我中了天同花,则肯定掩盖牌力，晚点打跑对方
                    if cardtype==9:
                        if(myhand[0].num==14 or myhand[1].num==14):
                            return (2,0)
                        #如果不是A花，还是要防止再出一张同花的
                        else: return (3,4)
                    #如果我中了葫芦以上牌力，肯定掩饰牌力
                    if cardtype>9:
                        return (2,0)
                    #如果是听顺，则对小加注跟注
                    if IsDrawStraight(mycardlist): return (2,0)
                    #如果是听花，我手里两张花，则跟注
                    if IsDrawFlush(mycardlist) and myhand[1].suit==myhand[0].suit: return (2,0)
                    #如果是听花，外面3张花，则我手里那张大于10跟注，小于10就看后面随机搞了
                    if IsDrawFlush(mycardlist) and len(SameSuit(publist))==3 and MyFlushTop(myhand,publist)>=10: return (2,0)
                    #如果是小牌，就根据底池赔率决定是否要跟注
                    if Sit.potsize/Sit.callchip>0.2/(winRate-0.8) and winRate>0.8: return (2,0)
                    return (0,0)
                #前位对手下了一个超重注
                if Sit.callchip>=Sit.callchip<(Sit.potsize-Sit.callchip)*1.5:
                    if Sit.potsize/Sit.callchip>0.1/(winRate-0.9) and winRate>0.9: return (3,4)
            #前位对手面对我的后位下注，加注了不少
            if Sit.betlist[Sit.myseat]>0 and Sit.callchip>Sit.potsize/4:
                #我有对，外面没有公对
                if cardtype==3 and cardtypeOf(publist)==2:
                    mypair=GetTopSame(mycardlist)
                    toppub=GetTopSame(publist)[0].num
                    #我是超对，就当翻前全下了
                    if mypair[0].num>toppub and myhand[0].num==myhand[1].num:
                        if mypair[0].num>=12:
                            return (3,4)
                        else:
                            return (0,0)
                    #我是顶对
                    if mypair[0].num==toppub:
                        #如果踢脚不行，就弃牌，否则干到底
                        if MyKicker(toppub,myhand)<=10: return (0,0)
                        return (2,0)
                    #我是小对
                    if mypair[0].num<toppub:
                        return (0,0)
                #外面牌有公对，我中了对
                if cardtype==6 and cardtypeOf(publist)==3:
                    return (0,0)
                #如果我中了两对
                if cardtype==6 and cardtypeOf(publist)==2:
                    #外面有危险的同花面，要重打
                    if len(SameSuit(publist))>=2:
                        return (3,4)
                    #外面有危险的顺子面，也要重打，结束战斗
                    if LikeStraight(publist)==True:
                        return (3,4)
                    return (3,4)
                #如果我中了暗三条
                if cardtype==7 and myhand[0].num==myhand[1].num:
                    return (3,4)
                #如果我中了明三条
                if cardtype==7 and myhand[0].num!=myhand[1].num and cardtypeOf(publist)==3:
                    return (3,4)
                #如果我中了天顺以上牌力
                if cardtype==8:
                    return (3,4)
                #如果我中了天同花,则肯定掩盖牌力，晚点打跑对方
                if cardtype==9:
                    return (3,4)
                #如果我中了葫芦以上牌力，肯定掩饰牌力
                if cardtype>9 and cardtypeOf(publist)!=7:
                    return (3,4)
                #如果我只是口袋对，外面是三条
                if cardtype==10 and cardtypeOf(publist)==7 and myhand[0].num>=10:
                    return (3,4)
                if winRate>=0.95: return (3,4)           
                return (0,0)    
        #1表示先行动
        if MyTurn(Sit)==1:
            #对手还没有动作
            if Sit.callchip==0:
                print('我在前面还没人下注')
                #只中一对要稍微凶一点，不打完缠斗不利
                if cardtype==3: 
                    if random.random()>0.2: return (3,3)
                    return (3,1)
                #只有葫芦慢打
                if cardtype>=10 and cardtypeOf(publist)!=7:
                    return (2,0)
                #其它牌前位都可以随机打
                if random.random()>0.5: return (3,1)
                return (2,0)
            #后面的对手check_raise了
            if Sit.callchip>Sit.betlist[Sit.myseat]:
                #对手只是不相信我的连续下注
                if Sit.betlist[Sit.myseat]<=Sit.oldpot/2:
                    #我有对，外面没有公对
                    if cardtype==3 and cardtypeOf(publist)==2:
                        mypair=GetTopSame(mycardlist)
                        toppub=GetTopSame(publist)[0].num
                        #我是超对
                        if mypair[0].num>toppub and myhand[0].num==myhand[1].num:
                            if mypair[0].num>=13:
                                return (3,4)
                            else:
                                return (2,0)
                        #我是顶对,至少跟一条街
                        if mypair[0].num==toppub:
                            return (2,0)
                        #我是中小对
                        if mypair[0].num<toppub:
                            return (0,0)
                    #外面牌有公对，我中了对，至少可以跟注
                    if cardtype==6 and cardtypeOf(publist)==3:
                        return (2,0)
                    #如果我中了两对
                    if cardtype==6 and cardtypeOf(publist)==2:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #不相信就干死你
                        return (3,4)
                    #如果我中了暗三条
                    if cardtype==7 and myhand[0].num==myhand[1].num:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        return (3,4)
                    #如果我中了明三条
                    if cardtype==7 and myhand[0].num!=myhand[1].num and cardtypeOf(publist)==3:
                        #外面有危险的同花面，要重打
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #外面有危险的顺子面，也要重打，结束战斗
                        if LikeStraight(publist)==True:
                            return (3,4)
                        #没有危险则一半过牌，一半加半池，看上去像是正常牌
                        if random.random()>0.5 : return (3,4)
                        else: return (3,4)
                    #如果我中了天顺以上牌力
                    if cardtype==8:
                        #如果有听同花需要结束战斗
                        if len(SameSuit(publist))>=2:
                            return (3,4)
                        #则只有20%机会加注去掩盖牌力
                        if random.random()>0.8: return (3,4)
                        else: return (3,4)
                    #如果我中了天同花,则肯定掩盖牌力，晚点打跑对方
                    if cardtype==9:
                        if(myhand[0].num==14 or myhand[1].num==14):
                            return (2,0)
                        #如果不是A花，还是要防止再出一张同花的
                        else: return (3,4)
                    #如果我中了葫芦以上牌力，肯定掩饰牌力
                    if cardtype>9 and cardtypeOf(publist)!=7:
                        return (2,0)
                    #如果我只是口袋对，外面是三条
                    if cardtype==10 and cardtypeOf(publist)==7:
                        if myhand[0].num>=7: return (3,4)
                        else: return (2,0)
                                     
                #对手是真有大牌，钓到我这条鱼了
                if Sit.betlist[Sit.myseat]>Sit.oldpot/2:
                    if winRate>0.98: return (3,4)
                    if Sit.potsize/Sit.callchip>0.1/(winRate-0.9) and winRate>0.9:
                        return (2,0)
                    if IsDrawFlush(mycardlist) and IsDrawStraight(mycardlist): 
                        print('同时听花听顺，肯定要一战到底')
                        return (3,4)
                
                
        return (0,0)
    #多人底池的打法，多人底池不慢打
    if(leftman>=3):
        print('翻后还剩3人')
        #如果没有人下注
        if Sit.callchip==0:
            print('没人下注')
            #我是最后一个说话的，积极点偷
            if getWaitingman(Sit)==0:
                if random.random()>0.3: return (3,1)
            #我是倒数第二个说话的，想办法偷
            if getWaitingman(Sit)==1:
                if random.random()>0.6: return (3,1)
            #我有点牌，赶走别人
            if winRate>0.8: return (3,1)
            return (2,0)
        #如果有人下注，但是小于等于半个底池
        if Sit.callchip>0 and Sit.callchip<=Sit.oldpot/2:
            print('对手下个小注')
            if winRate>0.96: return (3,4)
            if winRate>0.88: return (2,0)
        #如果有人下注，但是大于等于半个底池
        if Sit.callchip>Sit.oldpot/2 and Sit.callchip<=Sit.oldpot:
            print('对手下个半个底池以上的注')
            if winRate>0.96: return (3,4)
            if winRate>0.92: return (2,0)
        #如果有人下个超级大注
        if Sit.callchip>Sit.oldpot:
            print('对手下个大于底池的注')
            if winRate>0.96: return (3,4)
        #如果赔率合适，我有听牌机会
        if IsDrawFlush(mycardlist) and myhand[0].suit==myhand[1].suit:
            print('外面两张的同花听牌')
            if Sit.potsize/Sit.callchip>3: return (2,0)
        if IsDrawFlush(mycardlist) and MyFlushTop(myhand,publist)>=10:
            print('外面三张的同花听牌，我有张大于10的')
            if Sit.potsize/Sit.callchip>3: return (2,0)
        #如果又听花又听顺
        if IsGunshotStraight(mycardlist)>=1 and IsDrawFlush(mycardlist): 
            print('花顺双抽')
            return (2,0)
        #听顺也要跟跟的呀
        if IsDrawStraight(mycardlist): 
            print('听两头顺')
            if Sit.potsize/Sit.callchip>3: return (2,0)
        #卡顺有赔率也玩
        if IsGunshotStraight(mycardlist)==1:
            print('听卡顺')
            if Sit.potsize/Sit.callchip>6: return (2,0)
        #其它牌全部按底池赔率来跟
        if Sit.potsize/Sit.callchip>0.33/(winRate-0.66) and winRate>0.66: 
            print('底池赔率合适，剩下的情况')
            return (2,0)
        #否则弃牌
        
        return (0,0)
    return (0,-1)


#得到我的踢脚
def MyKicker(num,myhand):
    if(myhand[0].num==num): return myhand[1].num
    if(myhand[1].num==num): return myhand[0].num
    return 0

#得到我的同花是多大的
def MyFlushTop(myhand,publist):
    myhandlist=myhand+publist
    flushtop=0
    if IsDrawFlush(myhandlist)==False and IsFlush(myhandlist)==False: return 0
    else:
        theSuit=SameSuit(publist)[0].suit
        for card in myhand:
            if card.suit==theSuit and card.num>flushtop:
                flushtop=card.num
        return flushtop
    return 0

    

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
#转牌决策
def turnDecision(Sit):
    #剩下几个人
    leftman=getSurvivor(Sit)[1]
    if(leftman==2):
        if(Sit.callchip==0):
            #我在后位，对方没有下注
            if(MyTurn(Sit)==2):
                return (2,0)
            return (2,0)
        return (0,0)
    if(leftman>=3):
        return (0,0)
    
    return (0,-1)

#河牌决策
def riverDecision(Sit):
    #剩下几个人
    leftman=getSurvivor(Sit)[1]
    if(leftman==2):
        return (0,0)
    if(leftman==3):
        return (0,0)
    if(leftman>=4):
        return (0,0)
    return (0,-1)

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



