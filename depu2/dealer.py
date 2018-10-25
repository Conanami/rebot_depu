import random
import copy
import time

class card:
    def __init__(self,suit,num):
        self.suit=suit
        self.num=num
    def __str__(self):
        suitlist=['Spade','Heart','Club','Diamond']
        clist=['na','A','2','3','4','5','6','7','8','9','T','J','Q','K','A']
        if(self.suit is None or self.num is None):
            return "none"
        elif(self.num==-1):
            return "na"
        else:
            return suitlist[self.suit]+","+clist[self.num]
    def equals(self,onecard):
        if(self.suit==onecard.suit 
            and self.num==onecard.num ):
            return True
        else:
            return False
    
class dealer:
    def __init__(self):
        self.cardset=[]
        for suit in range(4):
            for num in range(2,15):
               self.cardset.append(card(suit,num))
   
    
def printCard(cardlist):
    rtstr=''
    for card in cardlist:
        rtstr= rtstr + (str(card))+"|"
    print(rtstr)

#一个LIST减去另一个LIST
def GetLeft(cardlist,myhand):
        rtlist=list(set(cardlist)-set(myhand))
        return rtlist
    
#得到张数最多的最大的牌
def GetTopSame(cardlist):
    #0-14,只用2-14
    rtHand=[]
    cardcnt=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #统计每种的张数
    for card in cardlist:
        cardcnt[card.num]=cardcnt[card.num]+1

    max=0
    index=-1
    for i in range(2,15):
        if(cardcnt[i]>=max):
            max=cardcnt[i]
            index=i
			
    for card in cardlist:
        if(card.num==index):
            rtHand.append(card)
		
    return rtHand

#找到连续的4张牌
def GetDrawStraight(cardlist):
    rthand=[]
    myhand=sorted(cardlist,key=lambda card:card.num, reverse=True)
    #dealer().printCard(myhand)
    strtcnt=0
    for i in range(len(myhand)-1):
        if(myhand[i].num-myhand[i+1].num==1):
            strtcnt=strtcnt+1
            rthand.append(myhand[i])
            #如果已经3张了，带上第4张返回
            if(strtcnt>=3):
                rthand.append(myhand[i+1])
                return rthand
		#如果差2格以上，只能重新找顺子    
        elif(myhand[i].num-myhand[i+1].num>1):
            strtcnt=0
            rthand=[]
    return rthand


#找到连续的5张牌
def GetTopStraight(cardlist):
    rthand=[]
    myhand=sorted(cardlist,key=lambda card:card.num, reverse=True)
    #dealer().printCard(myhand)
    strtcnt=0
    for i in range(len(myhand)-1):
        if(myhand[i].num-myhand[i+1].num==1):
            strtcnt=strtcnt+1
            rthand.append(myhand[i])
            #如果已经4张了，带上第5张返回
            if(strtcnt>=4):
                rthand.append(myhand[i+1])
                return rthand
			#A,2,3,4,5的判断
            elif(strtcnt>=3 and myhand[0].num==14 and myhand[i+1].num==2):
                rthand.append(myhand[i+1])
                rthand.append(myhand[0])
                return rthand
        #如果差2格以上，只能重新找顺子    
        elif(myhand[i].num-myhand[i+1].num>1):
            strtcnt=0
            rthand=[]
    return rthand

#找到最多的同花色
def SameSuit(cardlist):
    rtHand = []
    suitcnt=[0,0,0,0]
    for card in cardlist:
        suitcnt[card.suit]=suitcnt[card.suit]+1
    
    max=0
    maxsuit=-1
    for i in range(4):
        if(suitcnt[i]>max):
            max=suitcnt[i]
            maxsuit=i
	
    for card in cardlist:
        if(card.suit==maxsuit):
            rtHand.append(card)
    
    return rtHand

#牌面是不是像有顺面
def LikeStraight(cardlist):
    cnt=0
    for num in range(2,15):
        tmplist=copy.copy(cardlist)
        tmplist.append(card(0,num))
        if IsGunshotStraight(tmplist)>=1:
            cnt=cnt+1
    if cnt>=1: return True
    return False

#判断牌的类型
def cardtypeOf(cardlist):
    #如果没牌
    if(len(cardlist)==0 or cardlist is None):
        return 0
    #同花顺
    if(IsRoyal(cardlist)):
        return 12 
    #四条
    if(IsFour(cardlist)): 
        return 11
    #葫芦
    if(IsHulu(cardlist)):
        return 10
    #同花
    if(IsFlush(cardlist)): 
        return 9
    #顺子
    if(IsStraight(cardlist)): 
        return 8
	#三条
    if(IsThree(cardlist)):
        return 7
	#两对
    if(IsTwoPair(cardlist)): 
        return 6
    #听花
    #if(IsDrawFlush(cardlist)):
    #    return 5
    #听顺
    #if(IsDrawStraight(cardlist)):
    #    return 4
	#一对
    if(IsOnePair(cardlist)):
        return 3
	#高张
    if(IsHigh(cardlist)):
        return 2
    return 0

#判断是否同花顺
def IsRoyal(cardlist):
    myhand=SameSuit(cardlist)
    if(len(myhand)>=5):
        m2=GetTopStraight(myhand)
        if(len(m2)>=5): return True
        else: return False
    else: return False

#判断是否四条
def IsFour(cardlist):
    myhand=GetTopSame(cardlist)
    if(len(myhand)==4):
        return True
    else:
        return False

#判断是否葫芦
def IsHulu(cardlist):
    myhand=GetTopSame(cardlist)
    if(len(myhand)==3):
        lefthand=GetLeft(cardlist,myhand)
        myhand=GetTopSame(lefthand)
        if(len(myhand)>=2):
            return True
        else:
            return False
    else:
        return False

#判断是否同花
def IsFlush(cardlist):
    myhand=SameSuit(cardlist)
    #dealer().printCard(myhand)
    if(len(myhand)>=5):
        return True
    else:
        return False

#判断是否顺子
def IsStraight(cardlist):
    myhand=GetTopStraight(cardlist)
    if(len(myhand)>=5):
        return True
    else:
        return False

#判断是否三条
def IsThree(cardlist):
    myhand=GetTopSame(cardlist)
    if(len(myhand)==3):
        lefthand=GetLeft(cardlist,myhand)
        myhand=GetTopSame(lefthand)
        if(len(myhand)<2):
            return True 
        else:
            return False
    else:
        return False

#判断是否两对
def IsTwoPair(cardlist):
    myhand=GetTopSame(cardlist)
    if(len(myhand)==2):
        lefthand=GetLeft(cardlist,myhand)
        myhand=GetTopSame(lefthand)
        if(len(myhand)==2):
            return True
        else:
            return False
    else:
        return False

#判断是否听花
def IsDrawFlush(cardlist):
    myhand=SameSuit(cardlist)
    #dealer().printCard(myhand)
    if(len(myhand)==4):
        return True
    else:
        return False

#判断是否听顺
def IsDrawStraight2(cardlist):
    myhand=GetDrawStraight(cardlist)
    #四张才是听顺，5张就不对了
    if(len(myhand)==4 and IsStraight(cardlist)==False):
        return True
    else:
        return False

def IsDrawStraight(cardlist):
    if IsGunshotStraight(cardlist)==2:
        return True
    return False



#判断是否高张
def IsHigh(cardlist):
    myhand=GetTopSame(cardlist)
    if(len(myhand)<2):
        return True
    else: 
        return False

#判断是否一对
def IsOnePair(cardlist):
    myhand=GetTopSame(cardlist)
    if(len(myhand)==2):
        lefthand=GetLeft(cardlist,myhand)
        myhand=GetTopSame(lefthand)
        if (len(myhand)<2):
            return True
        else:
            return False
    else:
        return False

#两个人的牌比较
def Judge(list1,list2,cardcnt):
    if(list1 is None or list2 is None or len(list1)==0 or len(list2)==0 or cardcnt==0): return 0
    if(cardtypeOf(list1)>cardtypeOf(list2)):
        return 1
    elif(cardtypeOf(list1)<cardtypeOf(list2)):
        return 2
    elif(cardtypeOf(list1)==cardtypeOf(list2)):
        bothtype=cardtypeOf(list1)
        return CompareDetail(list1,list2,bothtype,cardcnt)

def InList(card, list1):
    for tmpcard in list1:
        if(card.suit==tmpcard.suit and card.num==tmpcard.num): return True
    return False

#计算下一张牌的胜率变化
def nextWinrate(list1,winrate):
    if(len(list1)>=7): return 0
    d=dealer()
    publist=[]
    
    totalrate=0
    totalcnt=0
    for i in range(2,len(list1)):
        publist.append(list1[i])
    #d.printCard(publist)
    for k in range(len(d.cardset)):
        cnt=0
        wincnt=0 
        if(InList(d.cardset[k],list1)==False):
            for i in range(len(d.cardset)):
                l1=list1+[d.cardset[k]]
                for j in range(i+1,len(d.cardset)):
                    list2=copy.copy(publist)
                    if( InList(d.cardset[i],l1)==False and InList(d.cardset[j],l1)==False  ):
                        list2.append(d.cardset[i])
                        list2.append(d.cardset[j])
                              
                        l2=list2+[d.cardset[k]]
                        if(Judge(l1,l2,5)==1):
                            wincnt=wincnt+1
                            cnt=cnt+1
                        elif(Judge(l1,l2,5)==2):
                            cnt=cnt+1
            #计算后面一张牌为K的时候，胜率情况
            tmpwinrate=wincnt/cnt
            totalrate=totalrate+tmpwinrate
            totalcnt=totalcnt+1
    return totalrate/totalcnt-winrate
    
    
#新的计算胜率方法，对手范围有点判断
def winRate2(list1):
    d=dealer()
    publist=[]
    cnt=0
    wincnt=0
    
    for i in range(2,len(list1)):
        publist.append(list1[i])
    #d.printCard(publist)
    for i in range(len(d.cardset)):
        for j in range(i+1,len(d.cardset)):
            list2=copy.copy(publist)
            if( InList(d.cardset[i],list1)==False and InList(d.cardset[j],list1)==False  ):
                list2.append(d.cardset[i])
                list2.append(d.cardset[j])
                weight=Weight(d.cardset[i],d.cardset[j])
                #d.printCard(list2)
                if(Judge(list1,list2,min(len(list1),5))==1):
                    wincnt=wincnt+weight
                    cnt=cnt+weight
                elif(Judge(list1,list2,min(len(list1),5))==2):
                    cnt=cnt+weight
    #print(cnt)
    #print(wincnt)
    #print("怎么会超过1")
    if cnt>0:
        rtrate=wincnt/cnt
    else:
        rtrate=0
    
    return rtrate

#计算对手牌的可能性权重
def Weight(card1,card2):
    if card1.num>=10 and card2.num>=10: return 10
    if (card1.num>=13 or card2.num>=13) and card1.suit==card2.suit: return 10
    if card1.num==card2.num : return 10
    if abs(card1.num-card2.num)==1 and card1.suit==card2.suit: return 10
    if abs(card1.num-card2.num)==2 and card1.suit==card2.suit: return 7
    if abs(card1.num-card2.num)==1 and card1.num>=8: return 7
    if card1.num<9 and card2.num<9 and abs(card1.num-card2.num)>=3 and card1.suit!=card2.num: return 1
    if card1.num<=12 and card2.num<=12 and abs(card1.num-card2.num)>=4 and card1.suit!=card2.num: return 1
    return 4

#计算胜率，前2张是自己的牌，后面都是公共牌
def winRate(list1):
    d=dealer()
    publist=[]
    cnt=0
    wincnt=0
    if len(list1)<5: return 0 
    for i in range(2,len(list1)):
        publist.append(list1[i])
    #d.printCard(publist)
    for i in range(len(d.cardset)):
        for j in range(i+1,len(d.cardset)):
            list2=copy.copy(publist)
            if( InList(d.cardset[i],list1)==False and InList(d.cardset[j],list1)==False  ):
                list2.append(d.cardset[i])
                list2.append(d.cardset[j])
                #d.printCard(list2)
                if(Judge(list1,list2,min(len(list1),5))==1):
                    wincnt=wincnt+1
                    cnt=cnt+1
                elif(Judge(list1,list2,min(len(list1),5))==2):
                    cnt=cnt+1
    #print(cnt)
    #print(wincnt)
    #print("怎么会超过1")
    if cnt>0:
        rtrate=wincnt/cnt
    else:
        rtrate=0
    
    return rtrate

#同类比较
def CompareDetail(list1,list2,bothtype,cardcnt):
    if(cardcnt<=0): return 0
    #高牌比较
    if(bothtype==2):
        if(len(list1)==0 and len(list2)==0 or list1 is None or list2 is None): return 0
        tmplist1=sorted(list1,key=lambda card:card.num, reverse=True)
        tmplist2=sorted(list2,key=lambda card:card.num, reverse=True)
        if(cardcnt<=len(tmplist1)): compareCnt=cardcnt
        else: compareCnt=min(len(tmplist1),len(tmplist2))
        for i in range(compareCnt):
            if(tmplist1[i].num>tmplist2[i].num): return 1
            elif(tmplist1[i].num<tmplist2[i].num): return 2
    #一对比较,三条比较，四条
    if(bothtype==3 or bothtype==7 or bothtype==11):
        m1=GetTopSame(list1)
        m2=GetTopSame(list2)
        if(m1[0].num>m2[0].num): return 1
        elif(m1[0].num<m2[0].num): return 2
        elif(m1[0].num==m2[0].num): 
            l1=GetLeft(list1,m1)
            l2=GetLeft(list2,m2)
            return CompareDetail(l1,l2,2,cardcnt-len(m1))
    #两对比较,葫芦比较
    if(bothtype==6 or bothtype==10):
        m1=GetTopSame(list1)
        m2=GetTopSame(list2)
        if(m1[0].num>m2[0].num): return 1
        elif(m1[0].num<m2[0].num): return 2
        elif(m1[0].num==m2[0].num): 
            l1=GetLeft(list1,m1)
            l2=GetLeft(list2,m2)
            return CompareDetail(l1,l2,3,cardcnt-len(m1))
    #比较顺子
    if(bothtype==8):
        m1=GetTopStraight(list1)
        m2=GetTopStraight(list2)
        if(m1[0].num>m2[0].num): return 1
        elif(m1[0].num<m2[0].num): return 2
        elif(m1[0].num==m2[0].num):	return 0
	#比较同花顺
    if(bothtype==12):
        s1=SameSuit(list1)
        s2=SameSuit(list2)
        m1=GetTopStraight(s1)
        m2=GetTopStraight(s2)
        if(m1[0].num>m2[0].num): return 1
        elif(m1[0].num<m2[0].num): return 2
        elif(m1[0].num==m2[0].num):	return 0
    #比较同花
    if(bothtype==9):
        s1=SameSuit(list1)
        s2=SameSuit(list2)
        return CompareDetail(s1,s2,2,cardcnt)
    return 0

#判断是否顺子听牌,0为不是卡顺，1为卡顺，2为双头卡顺或者双头顺
def IsGunshotStraight(cardlist):
    cnt=0
    for num in range(2,15):
        tmplist=copy.copy(cardlist)
        tmplist.append(card(0,num))
        if(IsStraight(tmplist)):
            cnt=cnt+1
    return cnt

#判断某个数字的牌，外面还有几张
def getLeftNumCardCnt(num,cardlist):
    cnt=0
    for card in cardlist:
        if(card.num==num): cnt=cnt+1
    return 4-cnt


#简单测试用的
def ddd():
    mylist=[card(0,9),card(0,6),card(2,5),card(0,4),card(3,2),card(0,13),card(3,3)]
    #print(IsGunshotStraight(mylist))
    printCard(mylist)
    print(winRate(mylist))

def ccc():
    starttime=time.clock()
    d=dealer()
    #d.printCard(d.cardset)
    random.shuffle(d.cardset)
    #newcardlist=(sorted(d.cardset,key=lambda card:card.num, reverse=True))
    #d.printCard(newcardlist)
    #mylist=[card(2,14),card(2,2),card(1,2),card(2,3),card(1,4),card(3,5),card(2,6)]
    typeStr=['','','高牌','一对','听顺','听花','两对','三条','顺子','同花','葫芦','金刚','同花顺']
    mylist=[]
    opplist=[]
    cardcnt=7
    for i in range(cardcnt):
        mylist.append(d.cardset[i])
        opplist.append(d.cardset[i+2])
    printCard(mylist)
    print(typeStr[cardtypeOf(mylist)])
    printCard(opplist)
    print(typeStr[cardtypeOf(opplist)])
    
    print(Judge(mylist,opplist,cardcnt))
    mywinrate=winRate(mylist)

    print(mywinrate)
    
    print(nextWinrate(mylist,mywinrate))
    #计算运行时间
    endtime = time.clock()
    print('Running time: %s Seconds'%(endtime-starttime))


#ddd()