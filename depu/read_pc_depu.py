from PIL import Image
from skimage import io,data
import time
import numpy as np
import dealer
import math
import random
import pandas as pd
import sqlite3


'''
    该类对外公开 analysisImg 方法，完成图片的解析 以及数据入库
'''


#定义一个情况类
class situation:
    def __init__(self):
        #牌
        self.cardlist=[]
        #后手筹码
        self.chiplist=[]
        #下注情况
        self.betlist=[]
        #弃牌跟注加注情况
        self.statuslist=[]
        self.position=0
        self.potsize=0
        self.bb=0
        self.callchip=0

    def todict(self):
        ''' 结果转换为 dict对象 '''
        result = {}
        if len(self.cardlist)>=2:
            result['my1'] = '%s|%s' % (self.cardlist[0].num, self.cardlist[0].suit)
            result['my2'] = '%s|%s' % (self.cardlist[1].num, self.cardlist[1].suit)
        
        result['pub1'] = None
        result['pub2'] = None
        result['pub3'] = None
        result['pub4'] = None
        result['pub5'] = None
        if len(self.cardlist)>=5:
            result['pub1'] = '%s|%s' % (self.cardlist[2].num, self.cardlist[2].suit)
            result['pub2'] = '%s|%s' % (self.cardlist[3].num, self.cardlist[3].suit)
            result['pub3'] = '%s|%s' % (self.cardlist[4].num, self.cardlist[4].suit)
        if len(self.cardlist)>=6:
            result['pub4'] = '%s|%s' % (self.cardlist[5].num, self.cardlist[5].suit)
        if len(self.cardlist)>=7:
            result['pub5'] = '%s|%s' % (self.cardlist[6].num, self.cardlist[6].suit)
        
        result['potsize'] = self.potsize

        result['chip1'] = self.chiplist[0] 
        result['chip2'] = self.chiplist[1]
        result['chip3'] = self.chiplist[2]
        result['chip4'] = self.chiplist[3]
        result['chip5'] = self.chiplist[4]
        result['chip6'] = self.chiplist[5]

        result['dc1'] = self.betlist[0] 
        result['dc2'] = self.betlist[1]
        result['dc3'] = self.betlist[2]
        result['dc4'] = self.betlist[3]
        result['dc5'] = self.betlist[4]
        result['dc6'] = self.betlist[5]

        result['status1'] = self.statuslist[0]
        result['status2'] = self.statuslist[1]
        result['status3'] = self.statuslist[2]
        result['status4'] = self.statuslist[3]
        result['status5'] = self.statuslist[4]
        result['status6'] = self.statuslist[5]

        result['bbnum'] = self.bb
        result['btnpos'] = self.position 
        result['callchip'] = self.callchip

        return result
    def __str__(self):
        return str(self.todict())


#定义一个牌的类
class card:
    def __init__(self,suit,num):
        self.suit=suit
        self.num=num
    def __str__(self):
        suitlist=['黑','红','梅','方']
        clist=['na','A','2','3','4','5','6','7','8','9','T','J','Q','K','A']
        if(self.suit is None or self.num is None):
            return "none"
        elif(self.num==-1):
            return "na"
        else:
            return clist[self.num] + "|" + suitlist[self.suit]

#定义一个图片框类
class picbox:
    def __init__(self,x1,y1,x2,y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2 

#在一个长条形状中，取得样本出现的X位置,入参都是numpy
def getPos(img,sample):
    rows,cols=img.shape
    srows,scols=sample.shape
    minrows=rows if rows<srows else srows

    for x in range(cols-scols):
        samecnt=0
        for i in range(minrows):
            for j in range(scols):
                if(img[i,x+j]<=127):
                    img[i,x+j]=0
                else:
                    img[i,x+j]=255
                
                if(sample[i,j]<=127):
                    sample[i,j]=0
                else:
                    sample[i,j]=255
                if(img[i,x+j]==sample[i,j]):
                    samecnt=samecnt+1
        #print(str(x)+':'+str(samecnt/(srows*scols)))
        if(samecnt/(srows*scols)>0.86):
            return x+j
    return -1

#相同大小的图片匹配
def matchPic(img,sample,thres=127):
    rows,cols=sample.shape
    samecnt=0
    for i in range(rows):
        for j in range(cols):
            if(img[i,j]<=thres):
                #black
                img[i,j]=0
            else:
                #white
                img[i,j]=255
                
            if(sample[i,j]<=thres):
                sample[i,j]=0
            else:
                sample[i,j]=255
            if(img[i,j]==sample[i,j]):
                samecnt=samecnt+1
    #print(samecnt/(rows*cols))
    
    if(thres==127):
        meetValue=0.92
    else:
        meetValue=0.88
    
    if((samecnt/(rows*cols))>=meetValue):
        return True
    else:
        return False

#img是完整图片的img,box是切下区域，sample是标准样本img
def MatchPicToSample(img,box,sample,thres=127):
    roi=img.crop(box)
    img_array=np.array(roi)
    sampleArray=np.array(sample)
    return matchPic(img_array,sampleArray,thres)

#从样本列表得到下标
def getNumFromList(img,box,samplelist,thres=127):
    for i,v in enumerate(samplelist):
        if ( MatchPicToSample(img,box,v,thres) ):
            return i

#从打开的文件，得到要处理的区域
def imreadGreyImg(wholeimg,dcbox):
    roi=wholeimg.crop(dcbox)
    dcimg=np.array(roi) #打开底池区域图像
    return dcimg

#wholeimg整个图片
#picbox是要读取数字的区域
#dc_num_sample是数字样本，包括小数点，还有个万字
#num_step是数字样本的宽度
#num_point是小数点样本的宽度
def SinglePicToNum(wholeimg,picbox,start,dc_num_sample_img,num_step,point_step,thres=127):
    i=picbox.x1+start
    numstr=""
    isWan=False
    isSlash=False
    while i<(picbox.x2-num_step):
        #每次挖个7像素宽度来比对
        tmpbox=(i,picbox.y1,i+num_step,picbox.y2)
        #print(i)
        num=getNumFromList(wholeimg,tmpbox,dc_num_sample_img,thres)
        if(num is not None and num>=0 and num<=9): 
            numstr=numstr+str(num)
            #print(num)
            #数字样本的宽度
            i=i+num_step
        elif (num==10):
            #小数点只有在有数字的时候才能出现，只能有一个小数点
            if(len(numstr)!=0 and numstr.__contains__(".")==False):
                numstr=numstr+'.'
                #小数点的宽度
                i=i+point_step
            else:
                #没认出来就慢慢认
                i=i+1
            
        elif (num==12):
            #如果出现/号，说明是大小盲标记
            isSlash=True
            numstr=numstr+'/'
            #print(num)
            #数字样本的宽度
            i=i+point_step
        elif (num==11):
            #如果出现“万”字则结束了
            isWan=True
            i=picbox.x2
        else:
            #没认出来就慢慢向右移动
            i=i+1
    if(len(numstr)==0):
        #啥都没认出来，就返回-1，大概这个位置上没人
        return (-1)
    elif(isSlash):
        return numstr
    elif(isWan):
        #如果有万，返回数值*10000
        try:
            return (float(numstr)*10000)
        except:
            return 0
        #如果有万，返回数值*10000
        
    else:
        #如果没有万，就正常返回
        try:
            return (float(numstr))
        except:
            return 0
#得到每个人的数字
def PicListToNum(wholeimg,betboxlist,start,chip_num_sample_img,num_step,point_step):
    rtlist=[]
    for betbox in betboxlist:
        betsize=SinglePicToNum(wholeimg,betbox,start,chip_num_sample_img,num_step,point_step)
        rtlist.append(betsize)
    return rtlist

#把文件列表全部载入内存中
def file2img(dc_num_sample):
    rtlist=[]
    for filename in dc_num_sample:
        img=Image.open(filename).convert('L')
        #imgarray=np.array(img)
        rtlist.append(img)
    return rtlist

#在一组框中找到样本
def findSampleInList(wholeimg,btnsample_img,btnboxlist):
    for i,tmpbox in enumerate(btnboxlist):
        mybox=(tmpbox.x1,tmpbox.y1,tmpbox.x2,tmpbox.y2)
        if(MatchPicToSample(wholeimg,mybox,btnsample_img)):
            return i

def PicListToStatus(wholeimg,staboxlist,status_sample_img):
    rtlist=[]
    for tmpbox in staboxlist:
        mybox=(tmpbox.x1,tmpbox.y1,tmpbox.x2,tmpbox.y2)
        rtlist.append(getNumFromList(wholeimg,mybox,status_sample_img))
    return rtlist

def readCard(wholeimg,suitbox,suit_sample_img,numbox,num_sample_img,numlist,thres):
    rtcard=card(-1,-1)
    tmpnum=getNumFromList(wholeimg,numbox,num_sample_img,thres)
    if(tmpnum is None):
        return None
    else:
        rtcard.num=numlist[tmpnum]
        rtcard.suit=getNumFromList(wholeimg,suitbox,suit_sample_img,thres)
        return rtcard

#得到7张牌
def getCardlist(wholeimg,first_suit_sample_img,first_num_sample_img, \
                        second_suit_sample_img,second_num_sample_img, \
                        pub_suit_sample_img,pub_num_sample_img,thres):
    rtlist=[]
    numlist=[2,3,4,5,6,7,8,9,10,11,12,13,14,10,8,12,13]
    #clist=['2','3','4','5','6','7','8','9','T','J','Q','K','A','T','8','Q']

    #第一张牌
    
    firstsuitbox=(618,433,631,447)
    
    firstnumbox=(614,414,628,433)
    

    card1=readCard(wholeimg,firstsuitbox,first_suit_sample_img,firstnumbox,first_num_sample_img,numlist,thres)
    if card1:
        rtlist.append(card1)

    #第二张牌
    secondsuitbox=(648,431,661,445)
    
    secondnumbox=(649,412,663,431)
    

    card2=readCard(wholeimg,secondsuitbox,second_suit_sample_img,secondnumbox,second_num_sample_img,numlist,thres)
    if card2:
        rtlist.append(card2)
    
    # 如果个人牌解析不完整，退出
    if len(rtlist)<2:
        return []

    #所有的公共牌
    x1=425
    x2=441
    y1=262
    y2=279
    pubsuitbox=(x1,y1,x2,y2)
    
    #拿5张公共牌
    
    for i in range(5):
        pubsuitbox=((x1+i*62),y1,x2+i*62,y2)
        pubnumbox=((423+i*62),237,(439+i*62),261)
        tmpcard=readCard(wholeimg,pubsuitbox,pub_suit_sample_img,pubnumbox,pub_num_sample_img,numlist,thres)
        if tmpcard:
            rtlist.append(tmpcard)
        else:
            break

    return rtlist

#读整个图片，获取所有信息
def GetSituation(wholeimg,first_suit_sample_img,first_num_sample_img, \
                        second_suit_sample_img,second_num_sample_img, \
                        pub_suit_sample_img,pub_num_sample_img, \
                        dc_num_sample_img,chip_num_sample_img,status_sample_img,call_num_sample_img,btnsample_img):
    
    rtSit=situation()
    
    #得到7张牌的情况
    thres=200
    rtSit.cardlist=getCardlist(wholeimg,first_suit_sample_img,first_num_sample_img, \
                        second_suit_sample_img,second_num_sample_img, \
                        pub_suit_sample_img,pub_num_sample_img,thres)
    

    thres=127  
    num_step=7
    point_step=3
    
    

    #底池大小范围
    x1=530
    x2=620
    y1=187
    y2=202
       
    
    numstart=20
    dcpicbox=picbox(x1,y1,x2,y2)
    
    potsize=SinglePicToNum(wholeimg,dcpicbox,numstart,dc_num_sample_img,num_step,point_step)
    
    rtSit.potsize=potsize
    
    #得到需要跟注的数量
    x1=445
    y1=543
    x2=490
    y2=559
    callbox=picbox(x1,y1,x2,y2)
    numstart=0
    callchip=SinglePicToNum(wholeimg,callbox,numstart,call_num_sample_img,11,4)
    if(callchip<=0): callchip=0
    rtSit.callchip=callchip
    
    #print('potsize:'+str(potsize))
    
   
    #下面是读筹码的情况
       
    
    #读所有人手里还剩的筹码
    numstart=0
    chipWidth=78
    chipHeight=15
    chipboxlist=[picbox(532,488,532+chipWidth,488+chipHeight) , \
                picbox(131,310,131+chipWidth,310+chipHeight),  \
                picbox(319,157,319+chipWidth,157+chipHeight),  \
                picbox(737,157,737+chipWidth,157+chipHeight),  \
                picbox(928,310,928+chipWidth,310+chipHeight),  \
                picbox(756,488,756+chipWidth,488+chipHeight)  ]
    rtSit.chiplist=PicListToNum(wholeimg,chipboxlist,numstart,chip_num_sample_img,num_step,point_step)

    #读所有的下注
    betWidth=60
    betHeight=15
    betboxlist=[picbox(549,362,549+betWidth,362+betHeight), \
                picbox(243,323,243+betWidth,323+betHeight), \
                picbox(344,185,344+betWidth,185+betHeight), \
                picbox(761,185,761+betWidth,185+betHeight), \
                picbox(859,310,859+betWidth,310+betHeight), \
                picbox(778,357,778+betWidth,357+betHeight)
    ]
    rtSit.betlist=PicListToNum(wholeimg,betboxlist,numstart,chip_num_sample_img,num_step,point_step)
    
    #读所有的状态
    
    staWidth=30
    staHeight=16
    staboxlist=[picbox(555,389,555+staWidth,389+staHeight), \
                picbox(156,210,156+staWidth,210+staHeight), \
                picbox(342,57,342+staWidth,57+staHeight), \
                picbox(759,57,759+staWidth,57+staHeight), \
                picbox(951,210,951+staWidth,210+staHeight), \
                picbox(779,388,779+staWidth,388+staHeight)
                ]
    numstart=0
    rtSit.statuslist=PicListToStatus(wholeimg,staboxlist,status_sample_img)

    #得到大盲注，玩的级别
    bbWidth=80
    bbHeight=15
    bbbox=picbox(592,335,592+bbWidth,335+bbHeight)
    blind = SinglePicToNum(wholeimg,bbbox,numstart,dc_num_sample_img,num_step,point_step)
    #print(blind)
    smallblind=blind.split('/')[0]
    
    rtSit.bb=float(smallblind)*2

    #找到谁是BTN位
    btnWidth=22
    btnHeight=22
    btnboxlist=[ picbox(628,378,628+btnWidth,378+btnHeight), \
                picbox(245,235,245+btnWidth,235+btnHeight), \
                picbox(404,169,404+btnWidth,169+btnHeight), \
                picbox(821,169,821+btnWidth,169+btnHeight), \
                picbox(887,247,887+btnWidth,247+btnHeight), \
                picbox(851,384,851+btnWidth,384+btnHeight)
    ]
    
    btn=findSampleInList(wholeimg,btnsample_img[0],btnboxlist)
    #print(btn)
    rtSit.position=btn
    return rtSit


class sampleconfig:
    ''' 样本配置类 '''

    def __init__(self):
        #第一张的花色样本
        first_suit_sample=[r'depu\samples\first_suit\1_s.png',
                            r'depu\samples\first_suit\1_h.png',
                            r'depu\samples\first_suit\1_c.png',
                            r'depu\samples\first_suit\1_d.png']
        self.first_suit_sample_img=file2img(first_suit_sample)
        #第一张的牌数字样本
        first_num_sample=[r'depu\samples\first_num\1_2.png', \
                            r'depu\samples\first_num\1_3.png', \
                            r'depu\samples\first_num\1_4.png', \
                            r'depu\samples\first_num\1_5.png', \
                            r'depu\samples\first_num\1_6.png', \
                            r'depu\samples\first_num\1_7.png', \
                            r'depu\samples\first_num\1_8.png', \
                            r'depu\samples\first_num\1_9.png', \
                            r'depu\samples\first_num\1_t.png', \
                            r'depu\samples\first_num\1_j.png', \
                            r'depu\samples\first_num\1_q.png', \
                            r'depu\samples\first_num\1_k.png', \
                            r'depu\samples\first_num\1_a.png' ]
        self.first_num_sample_img=file2img(first_num_sample)

        #第二张的花色样本
        second_suit_sample=[r'depu\samples\second_suit\2_s.png',
                            r'depu\samples\second_suit\2_h.png',
                            r'depu\samples\second_suit\2_c.png',
                            r'depu\samples\second_suit\2_d.png']
        self.second_suit_sample_img=file2img(second_suit_sample)
        #第二张的牌数字样本
        second_num_sample=[ r'depu\samples\second_num\2_2.png', \
                            r'depu\samples\second_num\2_3.png', \
                            r'depu\samples\second_num\2_4.png', \
                            r'depu\samples\second_num\2_5.png', \
                            r'depu\samples\second_num\2_6.png', \
                            r'depu\samples\second_num\2_7.png', \
                            r'depu\samples\second_num\2_8.png', \
                            r'depu\samples\second_num\2_9.png', \
                            r'depu\samples\second_num\2_t.png', \
                            r'depu\samples\second_num\2_j.png', \
                            r'depu\samples\second_num\2_q.png', \
                            r'depu\samples\second_num\2_k.png', \
                            r'depu\samples\second_num\2_a.png' ]
        self.second_num_sample_img=file2img(second_num_sample)
        
        #公共牌的花色样本
        pub_suit_sample=[r'depu\samples\pub_suit\p_s.png',
                        r'depu\samples\pub_suit\p_h.png',
                        r'depu\samples\pub_suit\p_c.png',
                        r'depu\samples\pub_suit\p_d.png']
        self.pub_suit_sample_img=file2img(pub_suit_sample)
        #公共牌的数字样本
        pub_num_sample=[r'depu\samples\pub_num\p_2.png',
                        r'depu\samples\pub_num\p_3.png',
                        r'depu\samples\pub_num\p_4.png',
                        r'depu\samples\pub_num\p_5.png',
                        r'depu\samples\pub_num\p_6.png',
                        r'depu\samples\pub_num\p_7.png',
                        r'depu\samples\pub_num\p_8.png',
                        r'depu\samples\pub_num\p_9.png',
                        r'depu\samples\pub_num\p_t.png',
                        r'depu\samples\pub_num\p_j.png',
                        r'depu\samples\pub_num\p_q.png',
                        r'depu\samples\pub_num\p_k.png',
                        r'depu\samples\pub_num\p_a.png',
                        r'depu\samples\pub_num\p_tr.png',
                        r'depu\samples\pub_num\p_8r.png',
                        r'depu\samples\pub_num\p_qr.png',
                        r'depu\samples\pub_num\p_kr.png']
        self.pub_num_sample_img=file2img(pub_num_sample)


        #底池和大小盲的字符样本
        dc_num_sample=[r'depu\samples\dc_num\dc_0.png', \
                    r'depu\samples\dc_num\dc_1.png', \
                    r'depu\samples\dc_num\dc_2.png', \
                    r'depu\samples\dc_num\dc_3.png', \
                    r'depu\samples\dc_num\dc_4.png', \
                    r'depu\samples\dc_num\dc_5.png', \
                    r'depu\samples\dc_num\dc_6.png', \
                    r'depu\samples\dc_num\dc_7.png', \
                    r'depu\samples\dc_num\dc_8.png', \
                    r'depu\samples\dc_num\dc_9.png', \
                    r'depu\samples\dc_num\dc_dot.png', \
                    r'depu\samples\dc_num\dc_wan.png', \
                    r'depu\samples\dc_num\dc_slash.png' ]
        self.dc_num_sample_img=file2img(dc_num_sample)

        #筹码和下注的字符样本
        chip_num_sample=[r'depu\samples\chip_num\chip_0.png', \
                        r'depu\samples\chip_num\chip_1.png', \
                        r'depu\samples\chip_num\chip_2.png', \
                        r'depu\samples\chip_num\chip_3.png', \
                        r'depu\samples\chip_num\chip_4.png', \
                        r'depu\samples\chip_num\chip_5.png', \
                        r'depu\samples\chip_num\chip_6.png', \
                        r'depu\samples\chip_num\chip_7.png', \
                        r'depu\samples\chip_num\chip_8.png', \
                        r'depu\samples\chip_num\chip_9.png', \
                        r'depu\samples\chip_num\chip_dot.png', \
                        r'depu\samples\chip_num\chip_wan.png' 
        ]
        self.chip_num_sample_img=file2img(chip_num_sample)
        #每个人的状态样本
        status_sample=[r'depu\samples\status\status_fold.png', \
                        r'depu\samples\status\status_check.png', \
                        r'depu\samples\status\status_call.png', \
                        r'depu\samples\status\status_raise.png' 
        ]
        self.status_sample_img=file2img(status_sample)
        #btn位样本
        btnsample=[r'depu\samples\btn_sample.png']
        self.btnsample_img=file2img(btnsample)

        #跟注大小数字
        call_num_sample=[r'depu\samples\call_num\call_0.png', \
                        r'depu\samples\call_num\call_1.png', \
                        r'depu\samples\call_num\call_2.png', \
                        r'depu\samples\call_num\call_3.png', \
                        r'depu\samples\call_num\call_4.png', \
                        r'depu\samples\call_num\call_5.png', \
                        r'depu\samples\call_num\call_6.png', \
                        r'depu\samples\call_num\call_7.png', \
                        r'depu\samples\call_num\call_8.png', \
                        r'depu\samples\call_num\call_9.png', \
                        r'depu\samples\call_num\call_dot.png', \
                        r'depu\samples\call_num\call_wan.png' ]
        self.call_num_sample_img=file2img(call_num_sample)

# 引用的时候，会默认初始化配置文件
config = sampleconfig()


def analysisImg(wholeimg):
    ''' 解析图片, 需要传入 灰度图像 该方法对外公开 '''
    rtSit=GetSituation(wholeimg,
                        config.first_suit_sample_img,
                        config.first_num_sample_img,
                        config.second_suit_sample_img,
                        config.second_num_sample_img,
                        config.pub_suit_sample_img,
                        config.pub_num_sample_img,
                        config.dc_num_sample_img,
                        config.chip_num_sample_img,
                        config.status_sample_img,
                        config.call_num_sample_img,
                        config.btnsample_img)

    #入库
    result = rtSit.todict()
    result['createtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    conn = sqlite3.connect('game.db')
    df = pd.DataFrame.from_records([result])
    pd.io.sql.to_sql(df, 'depu_log', conn, if_exists='append', index=False)
    return rtSit

