#import time
import dealer
import math
import random
#import readpot
from dealer import IsDraw
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
from dealer import cardtypeOf
from dealer import SameSuit

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
                #特别大看情况过牌骗人
                if finalWinrate>=0.98: 
                    if nextWinrate[1]<-0.15: 
                        print(nextWinrate[1],'如果很领先，不希望看到河牌，还是保护吧')
                        return (3,1)
                    return (2,0)
                elif nextWinrate[1]<-0.03 and finalWinrate>0.85 and rtSit.potsize<20*rtSit.bb:
                    print('是否需要保护:', nextWinrate[1])
                    return (3,1)
                elif nextWinrate[1]<-0.03 and finalWinrate>0.93:
                    print('比较大的牌，应该保护，第一次测试4，2')
                    return (3,1)               
                #对手一过牌我就保持进攻，看看效果，看起来不行
                #if MyTurn(rtSit)==2: return (3,1)
                if MyTurn(rtSit)==2 and rtSit.potsize<4*rtSit.bb*leftman: 
                    print('面对CHECK,和两条街示弱，永远转牌咋呼')
                    return (3,1) 
                elif MyTurn(rtSit)==1 and rtSit.potsize<4*rtSit.bb*leftman:
                    print('对手翻牌面对我的CHECK也CHECK，应该是示弱，我出击')
                    return (3,1)
                else: 
                    if finalWinrate>0.85 and rtSit.potsize<15*rtSit.bb*leftman: 
                        print('转牌觉得自己挺大的，还是要保持进攻')
                        return (3,1)
                
                if IsDraw(wholehandlist) and rtSit.potsize<10*rtSit.bb*leftman:
                    print('小底池听牌要保持攻击力')
                    return (3,1)
                return (2,0)
            #如果我还没有下注
            if(rtSit.betlist[rtSit.myseat]<=0):
                if(rtSit.callchip<rtSit.potsize/leftman and rtSit.potsize<15*rtSit.bb):
                    #超级大就是要骗人
                    if(finalWinrate>=0.98): return (2,0)
                    if(finalWinrate>=0.93): return (2,0)
                    if(finalWinrate>=0.90): return (2,0)
                    if(finalWinrate>=0.70): 
                        print('小池小赔率，随便跟跟看啦')
                        return (2,0)
                    if(IsDrawFlush(wholehandlist)): return (3,4)
                    if(IsDrawStraight(wholehandlist)): return(3,4)
                    #print('测试到这里吗？')
                    if(rtSit.callchip/rtSit.potsize<nextWinrate[0]/2): 
                        print('赔率实在太诱人，两高张都可以跟')
                        return (2,0)
                    return (0,0)
                
                if(rtSit.callchip<rtSit.potsize/2 and rtSit.potsize>=15*rtSit.bb and rtSit.potsize<=30*rtSit.bb):
                    print('转牌下小注，我根据底池赔率决定走不走')
                    if(finalWinrate>=0.98):  
                        if(nextWinrate[1]>=-0.01): return (3,3)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.92): 
                        if random.randint(0,9)>4:
                            print('92%，面对连续两条街，到底该如何决定')
                            return (2,0)
                        else:
                            print('92%，还是低调一点')
                            return (2,0)
                    
                    if(finalWinrate>=0.8): return (2,0)
                    if finalWinrate>0.75 and IsDraw(wholehandlist): return (2,0)
                    if finalWinrate>0.7: 
                        print('这么小的底池，老子不怕不怕')
                        return (2,0)
                    if(rtSit.callchip/rtSit.potsize<0.1):
                        print('奇怪底池赔率的计算，永远有诈唬的可能性')
                        return (2,0)
                    #认为底池赔率略高于我的胜率增加
                    if(rtSit.callchip/rtSit.potsize<=nextWinrate[1]*1.5):
                        print('听牌胜率的计算',nextWinrate[1])
                        if(IsDrawFlush(wholehandlist)): return (2,2)
                        if(IsDrawStraight(wholehandlist)): return(2,2)
                    return (0,0)
                if rtSit.callchip/rtSit.potsize<=0.05:
                    #0218，又一个逻辑漏洞
                    print('这种底池赔率是在搞笑吧')
                    return (2,0)
                if rtSit.callchip/rtSit.potsize<=0.15:
                    #0203加入，弥补一个逻辑漏洞
                    print('这种底池赔率不要考虑了，死跟')
                    if finalWinrate>0.8: return (2,0)
                
                
                if(rtSit.callchip<rtSit.potsize/2 and rtSit.callchip>=rtSit.potsize/3 
                    and rtSit.potsize>=30*rtSit.bb and rtSit.potsize<=60*rtSit.bb):
                    print('底池有点大了，我要考虑清楚')
                    if(finalWinrate>=0.985):  
                        if(nextWinrate[1]>=-0.01): return (3,3)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.92): return (2,0)
                    #0205转牌还是不要跟大底池的，保存实力，超对跟不动啊
                    if finalWinrate>=0.80 and rtSit.callchip<12*rtSit.bb: 
                        #超对面对转牌牌面，也不用太弱。
                        print('转牌跟动大底池，大下注')
                        return (2,0)
                    if(rtSit.callchip/rtSit.potsize<0.1):
                        print('奇怪底池赔率的计算，永远有诈唬的可能性')
                        return (2,0)
                    #认为底池赔率略高于我的胜率增加
                    if(rtSit.callchip/rtSit.potsize<=nextWinrate[1]):
                        print('听牌胜率的计算',nextWinrate[0],nextWinrate[1])
                        if(IsDrawFlush(wholehandlist)): return (2,2)
                        if(IsDrawStraight(wholehandlist)): return(2,2)
                    return (0,0)
                if(rtSit.callchip<rtSit.potsize/2 and rtSit.callchip>=rtSit.potsize/3 
                    and rtSit.potsize>=60*rtSit.bb):
                    print('底池非常大了，绝对要进行常考')
                    if(finalWinrate>=0.98):  
                        if(nextWinrate[1]>=-0.01): return (3,3)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.92): return (3,3)
                    if(finalWinrate>=0.80): return (2,0)
                    if(rtSit.callchip/rtSit.potsize<0.1):
                        print('奇怪底池赔率的计算，永远有诈唬的可能性')
                        return (2,0)
                    #认为底池赔率略高于我的胜率增加
                    if nextWinrate[0]<0.8:
                        print('转牌跟注河牌翻身没啥机会')
                        if(rtSit.callchip/rtSit.potsize<=nextWinrate[1]/2):
                            print('听牌胜率的计算',nextWinrate[0],nextWinrate[1])
                            if(IsDrawFlush(wholehandlist)): return (2,2)
                            if(IsDrawStraight(wholehandlist)): return(2,2)
                    if nextWinrate[0]>=0.8:
                        print('转牌跟注河牌翻身有点机会')
                        if(rtSit.callchip/rtSit.potsize<=nextWinrate[1]):
                            print('听牌胜率的计算',nextWinrate[0],nextWinrate[1])
                            if(IsDrawFlush(wholehandlist)): return (2,2)
                            if(IsDrawStraight(wholehandlist)): return(2,2)
                    return (0,0)
                #0224还有好多逻辑漏洞，这里面对一个小下注居然跟不动了
                if rtSit.callchip<rtSit.potsize/2.9 and rtSit.callchip<10*rtSit.bb:
                    print('小底池，面对一个半池左右的下注')
                    if finalWinrate>0.98: return (3,4)
                    callrate=0.6
                    if rtSit.callchip/rtSit.potsize<(finalWinrate-callrate)/callrate and finalWinrate>callrate: 
                        print('底池赔率好，一定要跟下去')
                        return (2,0)
                if rtSit.callchip<rtSit.potsize/2.9:
                    print('面对一个半池左右的下注')
                    if finalWinrate>0.98: return (3,4)
                    if finalWinrate>0.92 and IsDraw(wholehandlist): 
                        print('本身胜率也可以，还有听牌')
                        return (2,0)
                    #0613 这个还是太弱了，好多逻辑漏洞，
                    if finalWinrate>0.8:
                        print('两人对战，0.8的胜率也需要跟')
                        return (2,0)
                
                if(rtSit.callchip>=rtSit.potsize/leftman):
                    print('转牌，下注好大，啥意思？',nextWinrate[1])
                    if(finalWinrate>=0.97):  
                        if(nextWinrate[1]>=-0.01): return (2,0)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.85 and nextWinrate[1]>0.1): 
                        return (2,0)
                    if(nextWinrate[1]>=rtSit.callchip/rtSit.potsize): return (2,0)
                    if rtSit.potsize<=20*rtSit.bb:
                        print('下注比例大，但底池小呀')
                        if finalWinrate>0.7: return (2,0)
                    return (0,0)

            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                print('遭遇加注的情况')
                if(finalWinrate>=0.98): return (3,4)
                if rtSit.potsize/rtSit.callchip>0.15/(finalWinrate-0.85) and finalWinrate>0.85 and rtSit.potsize<=50*rtSit.bb:
                    print('赔率可以，已经套池，跟下去吧')
                    return (2,0)
                if rtSit.potsize/rtSit.callchip>0.11/(finalWinrate-0.89) and finalWinrate>0.89:
                    print('大牌大底池，小牌小底池')
                    #0615加入判断同花面的反击
                    if cardtypeOf(wholehandlist)<9 and len(SameSuit(publist))>=3:
                        print('外面有同花面，我要小心')
                        return (0,0)
                    return (2,0)
                if rtSit.potsize/rtSit.callchip>4.5 and (IsDrawFlush(wholehandlist) or IsDrawStraight(wholehandlist)):
                    print('这么好的赔率，听牌还是要试试的')
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
                    print('多人底池转牌硬打')
                    #0205，多人底池，牌力需要更强一点，三条以上等，两对全下有点过了
                    if(finalWinrate>=0.975):  
                        if(nextWinrate[1]>=-0.01): return (3,3)
                        if(nextWinrate[1]<-0.03): return (3,4)
                    if(finalWinrate>=0.91): return (3,3)
                    if(finalWinrate>=0.80): 
                        print('我顶对，应该不怕')
                        return (2,0)
                    if(finalWinrate>=0.7): return (0,0)
                    if(IsDrawFlush(wholehandlist)): return (2,0)
                    if(IsDrawStraight(wholehandlist)): return(2,0)
                    #print('多人底池转牌没必要继续')
                    #if(rtSit.callchip/rtSit.potsize<finalWinrate): return (2,0)
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
                    print('转牌正常跟加注，不用太暴露牌力')
                    if(nextWinrate[1]>0.3): return (3,4)
                    if(nextWinrate[1]>0.15): return (2,0)
                    if(finalWinrate>=0.97):  
                        if(nextWinrate[1]>=-0.01): return (2,0)
                        if(nextWinrate[1]<-0.03): return (3,3)
                    if rtSit.callchip<=80*rtSit.bb:   
                        print('是到这里了吗？')             
                        if(finalWinrate>=0.8): return (2,0)
                    return (0,0)
            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                if(finalWinrate>=0.98): return (3,4)
                if rtSit.callchip/rtSit.potsize<=0.15 and finalWinrate>0.7:
                    print('这种赔率，只要能抓诈唬都跟，就为了看看牌')
                    return (2,0)
                if rtSit.callchip/rtSit.potsize<=0.25 and finalWinrate>0.87:
                    print('这种赔率，我有点牌力，虽然落后但弃不掉')
                    return (2,0)
                if rtSit.potsize/rtSit.callchip>0.15/(finalWinrate-0.85) and finalWinrate>0.85:
                    print('没办法套池了，跟吧')
                    return (2,0)
                return (0,0)
        return (0,0)
    #----------------河牌战斗-------------------------------------------
    #0615河牌还需要好好调整
    if(pubnum==5):
        #还剩2个人
        if(leftman==2):
            #没人下注，底池小积极偷，底池大如果牌大就努力争取
            if rtSit.callchip==0:
                if(finalWinrate>=0.98): return (3,4)
                #对手没啥实力，我价值下注，不下注就没钱了
                if finalWinrate>0.94 and rtSit.potsize<50*rtSit.bb: return (3,3)
                if(finalWinrate>0.85) and rtSit.potsize<30*rtSit.bb: 
                    #0203，这里0.8的改动，到底该不该价值下注，有点疑惑
                    #0205, 这里改成0.85，找大哥式下注还是要避免
                    print('这里到底该不该价值下注？')
                    if random.randint(0,9)>4: return (3,3)
                    else: return (3,1)
                #尝试下2/3底池
                if finalWinrate>0.93: return (3,3)
                #没有摊牌价值，必须诈唬
                if finalWinrate<0.4 and finalWinrate>0.1 and rtSit.potsize<28*rtSit.bb:
                    print('河牌咋呼,只在小底池')
                    return (3,1)
                if finalWinrate>0.8 and rtSit.potsize<15*rtSit.bb:
                    print('大家都没实力，我最后有增强')
                    return (3,3)
                #否则摊牌比牌
                return (2,0)
            #如果我还没有下注
            if(rtSit.betlist[rtSit.myseat]<=0):
                #对手下了小注
                if(rtSit.callchip>0 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)/3):
                    print('对手河牌下小注')
                    if(finalWinrate>=0.94): return (3,4)
                    #根据最后胜率来决定
                    if rtSit.potsize<=20*rtSit.bb or rtSit.callchip<=10*rtSit.bb:
                        if(rtSit.potsize/rtSit.callchip>0.6/(finalWinrate-0.4) and finalWinrate>=0.4): 
                            print('小池子跟小注，打死也跟了，我头就是硬')
                            return (2,0)
                    if(rtSit.potsize<12*rtSit.bb):
                        if(finalWinrate>0.60): return (2,0)
                        
                    if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<20*rtSit.bb): 
                        if(finalWinrate>=0.66): return (2,0)
                        
                    if(rtSit.potsize>=20*rtSit.bb):
                        if(finalWinrate>=0.94): return (3,4)
                        if(finalWinrate>=0.91): return (3,1)
                        if(finalWinrate>=0.8): return (2,0)
                    if rtSit.callchip/rtSit.potsize<0.15: 
                        #0205虽然我知道我很落后了。
                        print('严重套池，这种赔率总归打光了')
                        return (2,0)
                    return (0,0)
                #对手表现出很强的实力
                #0214半池才在这里，满池不在这里
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)/3 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)*0.8):
                    print("对手下注半个底池，是在偷吗？头铁跟跟看")
                    if(finalWinrate>=0.96): return (3,4)
                    if(rtSit.potsize<12*rtSit.bb):
                        if(finalWinrate>0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=12*rtSit.bb and rtSit.potsize<20*rtSit.bb): 
                        if(finalWinrate>=0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=20*rtSit.bb and rtSit.potsize<40*rtSit.bb):
                        if(finalWinrate>=0.76): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=40*rtSit.bb and rtSit.potsize<65*rtSit.bb):
                        print('有一定的胜率还是要跟的')
                        if(finalWinrate>=0.82): return (2,0)
                        return (0,0)
                    if (rtSit.potsize>=65*rtSit.bb) :
                        print('大底池，弃不掉啊，有一定的胜率还是要跟的')
                        #0531，从0.92改成0.85，河牌面对1/2底池的下注，头比较铁，跟到底
                        if(finalWinrate>=0.85): return (2,0)
                        return (0,0)
                    return (0,0)
                #面对一个满池甚至超POT大下注
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)*0.8):
                    print('满池左右的下注，相当的自信')
                    if(finalWinrate>=0.97): return (3,4)
                    if rtSit.callchip<=24*rtSit.bb:
                        print('有胜率就跟吧，对方有可能是诈唬')
                        if finalWinrate>=0.8: return (2,0)
                    if rtSit.callchip<=40*rtSit.bb:
                        print('河牌面对满池也不用这么弱吧，跟跟看')                
                        if(finalWinrate>=0.91): return (2,0)
                        return (0,0)
                    
            
                    return (0,0)
            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                if(finalWinrate>=0.97): return (3,4)
                if rtSit.potsize/rtSit.callchip>0.15/(finalWinrate-0.85) and finalWinrate>0.85:
                    #0615河牌不能太弱
                    print('河牌套池干到底试试')
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
                    print('对手下注很小，多人底池')
                    if(finalWinrate>=0.97): return (3,4)
                    
                    if rtSit.callchip/rtSit.potsize<=0.1 and finalWinrate>0.5: 
                        print('惊人的小注，我总是跟注')
                        return (2,0)
                    if(rtSit.potsize<7*rtSit.bb*leftman ):
                        if(finalWinrate>0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=7*rtSit.bb*leftman and rtSit.potsize<=15*rtSit.bb*leftman): 
                        if(finalWinrate>=0.8): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>15*rtSit.bb*leftman and rtSit.potsize<=40*rtSit.bb*leftman):
                        if(finalWinrate>=0.97): return (3,4)
                        if(finalWinrate>=0.91): return (2,0)
                        if(finalWinrate>=0.76): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>40*rtSit.bb*leftman):
                        if(finalWinrate>=0.97): return (3,4)
                        if(finalWinrate>=0.92): return (0,0)
                        if(finalWinrate>=0.8): return (0,0)
                        return (0,0)
                    return (0,0)
                #对手表现出很强的实力
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)/3 and rtSit.callchip<(rtSit.potsize-rtSit.callchip)):
                    print('多人底池，对手下注1/2底池左右')
                    if(finalWinrate>=0.97): return (3,4)
                    
                    if rtSit.callchip/rtSit.potsize<=0.1 and finalWinrate>0.5: 
                        print('惊人的小注，我总是跟注')
                        return (2,0)
                    if(rtSit.potsize<7*rtSit.bb*leftman ):
                        if(finalWinrate>0.7): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>=7*rtSit.bb*leftman and rtSit.potsize<=15*rtSit.bb*leftman): 
                        if(finalWinrate>=0.8): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>15*rtSit.bb*leftman and rtSit.potsize<=40*rtSit.bb*leftman):
                        if(finalWinrate>=0.97): return (3,4)
                        if(finalWinrate>=0.91): return (2,0)
                        if(finalWinrate>=0.76): return (2,0)
                        return (0,0)
                    if(rtSit.potsize>40*rtSit.bb*leftman):
                        if(finalWinrate>=0.97): return (3,4)
                        if(finalWinrate>=0.92): return (0,0)
                        if(finalWinrate>=0.8): return (0,0)
                        return (0,0)
                    return (0,0)
                #面对一个超POT大下注
                if(rtSit.callchip>=(rtSit.potsize-rtSit.callchip)):
                    if(finalWinrate>=0.98): return (3,4)
                    if rtSit.callchip<=30*rtSit.bb:                
                        if(finalWinrate>=0.9): 
                            print('小底池就算是超池我也跟得动，明显是偷')
                            return (2,0)
                        return (0,0)
                    return (0,0)
                return (0,0)
            #如果我下注后遭到对方反击
            if(rtSit.betlist[rtSit.myseat]>0):
                if(finalWinrate>=0.97): return (3,4)
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
        #finalWinrate=math.pow(myWinrate,leftman-1)
        finalWinrate=myWinrate
        if IsDrawFlush(myhand):
            if(pubnum==3):
                if(myhand[0].suit==myhand[1].suit):
                    if(finalWinrate<0.5):
                        print('同花听牌，胜率增加%.4f' % 0.3)
                        finalWinrate=finalWinrate 
                if(len(dealer.SameSuit(rtSit.cardlist))==3):
                    if(IsFlush(myhand)==False):
                        print('公面三同花,胜率减少%.4f' % 0.1)
                        finalWinrate=finalWinrate-0.1
            if pubnum==4:  #and len(dealer.SameSuit(rtSit.cardlist))<3):
                print('同花听牌,胜率增加%.4f' % 0.1)
                finalWinrate=finalWinrate
        if IsDrawStraight(myhand):
            if pubnum==3:
                if(finalWinrate<0.5):
                    print('顺子听牌，胜率增加%.4f' % 0.3)
                    finalWinrate=finalWinrate
            if pubnum==4 and IsDrawStraight(rtSit.cardlist)==False :
                if(finalWinrate<0.6):
                    print('顺子听牌，胜率增加%.4f' % 0.15)
                    finalWinrate=finalWinrate
        
        print('最后胜率%.4f' % finalWinrate)
        #翻牌后的决策
        mydecision=afterFlopDecision(pubnum,nextWinrate,finalWinrate,leftman,rtSit)
        print('并非最终决定：',mydecision)
        finalDecision=mydecision
    
    #实际情况还要结合自己的筹码，才能决定到底点击哪里
    newDecision=getClickDecision(finalDecision,rtSit)
    return newDecision


#根据自己手里的筹码多少，下注一个比例
#3，1   半池
#3，2   2/3底池
#3，3   底池
#3，5   1/3底池
#3，6   3/4底池
#3，7   1.5底池
#2，0   过牌/跟注
#0，0   弃牌

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
    if finalDecision==(0,0) and rtSit.callchip<=0 : 
        #如果决策是弃牌，但是需要跟注为0，决策自动改为跟注
        rtDecision=(2,1)
    return rtDecision
    
#获得下注的按键
def getDragTarget(Sit,betsize):
    return 500,500

