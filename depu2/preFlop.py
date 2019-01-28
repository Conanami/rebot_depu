from reader import getPubnum
from reader import getMyHand

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


#判断手牌是否在openRange中，就是第一个人应该开始的范围
def IsOpenRange(Sit):
    myhand=getMyHand(Sit)
    if (Sit.position-Sit.myseat)%6==3:
        print('UTG')
        return utgOpen(myhand)
    if (Sit.position-Sit.myseat)%6==2:
        print('MP')
        return mpOpen(myhand)
    if (Sit.position-Sit.myseat)%6==1:
        print('CO')
        return coOpen(myhand)
    if (Sit.position-Sit.myseat)%6==0:
        print('BTN')
        return btnOpen(myhand)
    if (Sit.position-Sit.myseat)%6==5:
        print('SB')
        return sbOpen(myhand)
    if (Sit.position-Sit.myseat)%6==4:
        print('BB')
        return bbOpen(myhand)


#枪口位可以开局的牌
def utgOpen(myhand):
    #中大口袋对
    if myhand[0].num==myhand[1].num and myhand[0].num>=7: return True
    #ATs以上
    if (myhand[0].num==14 or myhand[1].num==14) and myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=24:
        return True
    #AJo以上，和KQs, KQo
    if myhand[0].num+myhand[1].num>=25:
        return True
    return False

#MP位可以开局的牌
def mpOpen(myhand):
    #QJs,JTs
    if (myhand[0].suit==myhand[1].suit 
        and myhand[0].num>=10 and myhand[1].num>=10
        and abs(myhand[0].num-myhand[1].num)==1) :
        return True
    #KJs
    if myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=24:
        return True
    #A9s
    if (myhand[0].num==14 or myhand[1].num==14) and myhand[0].suit==myhand[1].suit and   myhand[0].num+myhand[1].num>=23:
        return True
    return utgOpen(myhand)

#CO位可以开局的牌
def coOpen(myhand):
    #44,55,66
    if myhand[0].num==myhand[1].num and myhand[0].num>=4: return True
    #AXs
    if (myhand[0].num==14 or myhand[1].num==14) and myhand[0].suit==myhand[1].suit:
        return True
    #ATo
    if (myhand[0].num==14 or myhand[1].num==14) and myhand[0].num+myhand[1].num>=24:
        return True
    return mpOpen(myhand)

#BTN位可以开局的牌
def btnOpen(myhand):
    #22,33
    if myhand[0].num==myhand[1].num: return True
    #A8o+
    if (myhand[0].num==14 or myhand[1].num==14) and myhand[0].num+myhand[1].num>=22:
        return True
    return coOpen(myhand)

#小盲位可以开局的牌
def sbOpen(myhand):
    #AXo
    if (myhand[0].num==14 or myhand[1].num==14):
        return True
    #K8+
    if (myhand[0].num==13 or myhand[1].num==13) and myhand[0].num+myhand[1].num>=21:
        return True
    #大同花连牌
    if myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=15 and abs(myhand[0].num-myhand[1].num)==1:
        return True
    return btnOpen(myhand)

#大盲位可以保卫盲注的牌
def bbOpen(myhand):
    #小同花连牌
    if myhand[0].suit==myhand[1].suit and abs(myhand[0].num-myhand[1].num)==1:
        return True
    #大同花间隔牌
    if myhand[0].suit==myhand[1].suit and myhand[0].num+myhand[1].num>=16 and abs(myhand[0].num-myhand[1].num)==2:
        return True
    return sbOpen(myhand)

#判断是否第一个人
def IsFirst(Sit):
    pubcnt=getPubnum(Sit)
    if pubcnt==0 :
        cnt=0
        for i in range(Sit.position+3,Sit.position+8):
            if i%6==Sit.myseat and cnt==0:
                return True
            elif Sit.betlist[i%6]>0: 
                cnt = cnt+1
        return False
    else:
        return '不是翻前好不好'
