from PIL import Image
from skimage import io,data
import time
import numpy as np
import dealer
import math
import random
import pandas as pd
import sqlite3
from dealer import card


'''
    该类对外公开 analysisImg 方法，完成图片的解析 以及数据入库
'''


#定义一个情况类
class situation:
    def __init__(self):
        #每个人的手牌
        self.handlist=[]
        #公共牌
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
            if len(self.cardlist)==3:
                result['pub1'] = '%s|%s' % (self.cardlist[2].num, self.cardlist[2].suit)
            if len(self.cardlist)==4:
                result['pub1'] = '%s|%s' % (self.cardlist[2].num, self.cardlist[2].suit)
                result['pub2'] = '%s|%s' % (self.cardlist[3].num, self.cardlist[3].suit)
        if len(self.cardlist)>=5:
            result['pub1'] = '%s|%s' % (self.cardlist[2].num, self.cardlist[2].suit)
            result['pub2'] = '%s|%s' % (self.cardlist[3].num, self.cardlist[3].suit)
            result['pub3'] = '%s|%s' % (self.cardlist[4].num, self.cardlist[4].suit)
        if len(self.cardlist)>=6:
            result['pub4'] = '%s|%s' % (self.cardlist[5].num, self.cardlist[5].suit)
        if len(self.cardlist)>=7:
            result['pub5'] = '%s|%s' % (self.cardlist[6].num, self.cardlist[6].suit)
        result['chip1'] = self.chiplist[0] 
        result['chip2'] = self.chiplist[1]
        result['chip3'] = self.chiplist[2]
        result['chip4'] = self.chiplist[3]
        result['chip5'] = self.chiplist[4]
        result['chip6'] = self.chiplist[5]
        
        result['potsize'] = self.potsize

        
        
        result['dc1'] = self.betlist[0] 
        result['dc2'] = self.betlist[1]
        result['dc3'] = self.betlist[2]
        result['dc4'] = self.betlist[3]
        result['dc5'] = self.betlist[4]
        result['dc6'] = self.betlist[5]
        
        result['btnpos'] = self.position 
        '''
        result['status1'] = self.statuslist[0]
        result['status2'] = self.statuslist[1]
        result['status3'] = self.statuslist[2]
        result['status4'] = self.statuslist[3]
        result['status5'] = self.statuslist[4]
        result['status6'] = self.statuslist[5]

        result['bbnum'] = self.bb
        
        result['callchip'] = self.callchip
        '''
        return result
    def __str__(self):
        return str(self.todict())



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

#矩阵匹配算法
def matchPic(img,sample,thres=127):
    img[img<thres]=0
    img[img>=thres]=1
    sample[sample<thres]=0
    sample[sample>=thres]=1
    if(img==sample).all(): return True
    else: return False

#相同大小的图片匹配
def matchPic2(img,sample,thres=127):
    rows,cols=sample.shape
    irows,icols=img.shape
    #print( str(rows)+","+str(cols))
    #print( str(irows)+","+str(icols))
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
        meetValue=0.98
    else:
        meetValue=0.98
    
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
    isQuan=False
    isXia=False
    while i<(picbox.x2-num_step):
        #每次挖个num_step像素宽度来比对
        tmpbox=(i,picbox.y1,i+num_step,picbox.y2)
        #print(tmpbox)
        num=getNumFromList(wholeimg,tmpbox,dc_num_sample_img,thres)
        if(num is not None and num>=0 and num<=9): 
            numstr=numstr+str(num)
            #print(num)
            #数字样本的宽度
            i=i+num_step
        elif (num==10):
            # 逗号只能在有数字的时候出现
            if(len(numstr)!=0):
                numstr=numstr
                #逗号的宽度
                i=i+point_step
            else:
                #没认出来就慢慢认
                i=i+1
        elif (num==11):
            isQuan=True
            i=i+point_step
        elif (num==12):
            #如果出现“下”字则结束了
            isXia=True
            i=picbox.x2
        else:
            #没认出来就慢慢向右移动
            i=i+1
    #如果有全下，则返回0
    if(isQuan and isXia):
         return 0
    elif(len(numstr)==0):
        #啥都没认出来，就返回-1，大概这个位置上没人
        return (-1)
    else:
        #如果没有全下，就返回数字
        try:
            return (float(numstr))
        except:
            return -1

#得到每个人的数字
def PicListToNum(wholeimg,betboxlist,start,chip_num_sample_img,num_step,point_step,thres=127,statuslist=[1,1,1,1,1,1]):
    rtlist=[]
    i=0
    for betbox in betboxlist:
        if(statuslist[i]==0):
            rtlist.append(0)
        else:
            betsize=SinglePicToNum(wholeimg,betbox,start,chip_num_sample_img,num_step,point_step,thres)
            rtlist.append(betsize)
        i=i+1
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
def findSampleInList(wholeimg,btnsample_img,btnboxlist,thres=127):
    for i,tmpbox in enumerate(btnboxlist):
        mybox=(tmpbox.x1,tmpbox.y1,tmpbox.x2,tmpbox.y2)
        if(MatchPicToSample(wholeimg,mybox,btnsample_img,thres)):
            return i

#得到一组状态
def PicListToStatus(wholeimg,staboxlist,status_sample_img,thres=127):
    rtlist=[]
    for tmpbox in staboxlist:
        mybox=(tmpbox.x1,tmpbox.y1,tmpbox.x2,tmpbox.y2)
        rtlist.append(getNumFromList(wholeimg,mybox,status_sample_img,thres))
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

#上面都是可以重用的函数，下面是需要根据窗体实际调整的函数
#得到每个人的手牌，和公共牌
def getCardlist(wholeimg,pub_suit_sample_img,pub_num_sample_img,thres):
    #每个人的手牌
    handcard=[]
    #公共牌
    pubcard=[]
    numlist=[2,3,4,5,6,7,8,9,10,11,12,13,14]
  
    #所有的公共牌
    num_x=274
    num_y=224
    num_step=54
    num_w=11
    num_h=15

    suit_x=273
    suit_y=239
    suit_step=num_step
    suit_w=13
    suit_h=15
   
    #拿5张公共牌
    
    for i in range(5):
        pubsuitbox=( suit_x+i*suit_step, suit_y, suit_x+suit_w+i*suit_step, suit_y+suit_h)
        pubnumbox=( num_x+i*num_step, num_y, num_x+num_w+i*num_step, num_y+num_h)
        tmpcard=readCard(wholeimg,pubsuitbox,pub_suit_sample_img,pubnumbox,pub_num_sample_img,numlist,thres)
        if tmpcard:
            print(tmpcard)
            pubcard.append(tmpcard)
        else:
            break
    
    #读6个人的手牌,最下面那个开始，顺时针依次为0，1，2，3，4，5
    sixboxlist=[(357,383),(61,287),(61,115),(357,55),(656,115),(656,287)]
    handcard=getHandCard(wholeimg,sixboxlist,pub_suit_sample_img,pub_num_sample_img,numlist,thres)
    
    return pubcard,handcard

#读手牌
def getHandCard(wholeimg,sixboxlist,pub_suit_sample_img,pub_num_sample_img,numlist,thres):
    #6个人，最下面那个开始，顺时针依次为0，1，2，3，4，5
    rtHandcard=[]
    #左右牌之间的距离
    cardstep=48
    #数字宽度
    num_w=11
    #数字高度
    num_h=15
    #花色宽度
    suit_w=13
    #花色高度
    suit_h=15
    #从数字到花色的Y轴距离
    c2s_y=15
    #从数字到花色的X轴距离
    c2s_x=-1

    for (x,y) in sixboxlist:
        leftnumbox=(x,y,x+num_w,y+num_h)
        leftsuitbox=(x+c2s_x,y+c2s_y,x+c2s_x+suit_w,y+c2s_y+suit_h)
        leftcard=readCard(wholeimg,leftsuitbox,pub_suit_sample_img,leftnumbox,pub_num_sample_img,numlist,thres)
        print(leftcard)
        rightnumbox=(x+cardstep,y,x+cardstep+num_w,y+num_h)
        rightsuitbox=(x+cardstep+c2s_x,y+c2s_y,x+cardstep+c2s_x+suit_w,y+c2s_y+suit_h)
        rightcard=readCard(wholeimg,rightsuitbox,pub_suit_sample_img,rightnumbox,pub_num_sample_img,numlist,thres)
        print(rightcard)
        rtHandcard.append((leftcard,rightcard))
    return rtHandcard

#判断是否需要解析整个图片，该方法对外公开
def NeedAnalyse(wholeimg):
    foldbox=(270,540,270+50,540+22)
    if( MatchPicToSample(wholeimg,foldbox,config.foldsample_img[0])==False and
        MatchPicToSample(wholeimg,foldbox,config.foldsample_img[1])==False ): return False
    else: return True

#从筹码量直接取得statuslist
def GetStatusList(chiplist):
    statuslist=[]
    for i in range(6):
        if chiplist[i]<0: statuslist[i]=0
        else: statuslist[i]=1 
    return statuslist


#读整个图片，获取所有信息
def GetSituation(wholeimg, chip_num_sample_img, dc_num_sample_img,pub_suit_sample_img,pub_num_sample_img,btnsample_img):
    
    rtSit=situation()
    
    #得到手牌的情况
    thres=250
    rtSit.cardlist,rtSit.handlist=getCardlist(wholeimg,pub_suit_sample_img,pub_num_sample_img,thres)
    #dealer.printCard(rtSit.cardlist)
    
    #读所有人手里还剩的筹码
    
    numstart=0
    chipWidth=90
    chipHeight=14
    num_step=9
    point_step=9
    thres=200
    chipboxlist=[picbox(382,450,382+chipWidth,450+chipHeight) , \
                picbox(41,354,41+chipWidth,354+chipHeight),  \
                picbox(41,182,41+chipWidth,182+chipHeight),  \
                picbox(337,116,337+chipWidth,116+chipHeight),  \
                picbox(676,182,676+chipWidth,182+chipHeight),  \
                picbox(676,354,676+chipWidth,354+chipHeight)  ]
    rtSit.chiplist=PicListToNum(wholeimg,chipboxlist,numstart,chip_num_sample_img,num_step,point_step,thres)
    
    #底池大小范围
    x1=400
    x2=x1+100
    y1=198
    y2=y1+14
    numstart=0
    dcpicbox=picbox(x1,y1,x2,y2)
    potsize=SinglePicToNum(wholeimg,dcpicbox,numstart,chip_num_sample_img,num_step,point_step,thres)
    rtSit.potsize=potsize

    #读所有的下注
    #if(callchip==0): rtSit.betlist=[0,0,0,0,0,0]
    #else:

    betWidth=120
    betHeight=12
    num_step=8
    point_step=num_step
    thres=200
    numstart=0
    betboxlist=[picbox(337,344,337+betWidth,344+betHeight), \
                picbox(200,315,200+betWidth,315+betHeight), \
                picbox(220,191,220+betWidth,191+betHeight), \
                picbox(385,158,385+betWidth,158+betHeight), \
                picbox(483,191,483+betWidth,191+betHeight), \
                picbox(557,316,557+betWidth,316+betHeight)
    ]
    rtSit.betlist=PicListToNum(wholeimg,betboxlist,numstart,dc_num_sample_img,num_step,point_step,thres)

    #找到谁是BTN位
    btnWidth=28
    btnHeight=24
    btnboxlist=[picbox(459,368,459+btnWidth,368+btnHeight), \
                picbox(198,332,198+btnWidth,332+btnHeight), \
                picbox(173,200,173+btnWidth,200+btnHeight), \
                picbox(332,147,332+btnWidth,147+btnHeight), \
                picbox(618,205,618+btnWidth,205+btnHeight), \
                picbox(584,332,584+btnWidth,332+btnHeight)
    ]
    
    btn=findSampleInList(wholeimg,btnsample_img[0],btnboxlist,thres)
    rtSit.position=btn
    rtSit.statuslist=GetStatusList(rtSit.chiplist)
    #pokerstar要读窗体TITLE
    rtSit.bb=100

    
       
    
    
    
    
    
    

    #得到大盲注，玩的级别
    
    bbWidth=80
    bbHeight=15
    bbbox=picbox(592,335,592+bbWidth,335+bbHeight)
    blind = SinglePicToNum(wholeimg,bbbox,numstart,dc_num_sample_img,num_step,point_step)
    print(blind)
    try:
        if '/' in str(blind):
            smallblind=blind.split('/')[0]
            bigblind=blind.split('/')[1]
            if(float(smallblind)>0):
                rtSit.bb=float(smallblind)*2
            elif(float(bigblind)>0):
                rtSit.bb=float(bigblind)
        else:
            rtSit.bb=float(blind)*2
    except:
        rtSit.bb=max(min(rtSit.betlist),100)
    
    rtSit.bb=10
    
   
    #print(btn)
    '''
    #rtSit.position=0
    
    return rtSit


class sampleconfig:
    ''' 样本配置类 '''

    def __init__(self):
        
        #公共牌的花色样本
        pub_suit_sample=[r'.\samples\pub_suit\p_s.png',
                        r'.\samples\pub_suit\p_h.png',
                        r'.\samples\pub_suit\p_c.png',
                        r'.\samples\pub_suit\p_d.png']
        self.pub_suit_sample_img=file2img(pub_suit_sample)
        #公共牌的数字样本
        pub_num_sample=[r'.\samples\pub_num\p_2.png',
                        r'.\samples\pub_num\p_3.png',
                        r'.\samples\pub_num\p_4.png',
                        r'.\samples\pub_num\p_5.png',
                        r'.\samples\pub_num\p_6.png',
                        r'.\samples\pub_num\p_7.png',
                        r'.\samples\pub_num\p_8.png',
                        r'.\samples\pub_num\p_9.png',
                        r'.\samples\pub_num\p_t.png',
                        r'.\samples\pub_num\p_j.png',
                        r'.\samples\pub_num\p_q.png',
                        r'.\samples\pub_num\p_k.png',
                        r'.\samples\pub_num\p_a.png'
                       ]
        self.pub_num_sample_img=file2img(pub_num_sample)

        #筹码和下注的字符样本
        chip_num_sample=[r'.\samples\chip_num\chip_0.png', \
                        r'.\samples\chip_num\chip_1.png', \
                        r'.\samples\chip_num\chip_2.png', \
                        r'.\samples\chip_num\chip_3.png', \
                        r'.\samples\chip_num\chip_4.png', \
                        r'.\samples\chip_num\chip_5.png', \
                        r'.\samples\chip_num\chip_6.png', \
                        r'.\samples\chip_num\chip_7.png', \
                        r'.\samples\chip_num\chip_8.png', \
                        r'.\samples\chip_num\chip_9.png', \
                        r'.\samples\chip_num\chip_dot.png',
                        r'.\samples\chip_num\chip_quan.png',
                        r'.\samples\chip_num\chip_xia.png'
        ]
        self.chip_num_sample_img=file2img(chip_num_sample)
        
        #底池和大小盲的字符样本
        #如果没有小数点的，就把dc_dot换成dc_wan
        dc_num_sample=[r'.\samples\dc_num\dc_0.png', \
                    r'.\samples\dc_num\dc_1.png', \
                    r'.\samples\dc_num\dc_2.png', \
                    r'.\samples\dc_num\dc_3.png', \
                    r'.\samples\dc_num\dc_4.png', \
                    r'.\samples\dc_num\dc_5.png', \
                    r'.\samples\dc_num\dc_6.png', \
                    r'.\samples\dc_num\dc_7.png', \
                    r'.\samples\dc_num\dc_8.png', \
                    r'.\samples\dc_num\dc_9.png', \
                    r'.\samples\dc_num\dc_dot.png' ]
        self.dc_num_sample_img=file2img(dc_num_sample)
        
         #btn位样本
        btnsample=[r'.\samples\btn_sample.png']
        self.btnsample_img=file2img(btnsample)

        '''
        
        
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
        
        #fold按钮样本
        foldsample=[r'depu\samples\fold_btn.png',\
                    r'depu\samples\fold_btn2.png' ]
        self.foldsample_img=file2img(foldsample)

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
        '''


# 引用的时候，会默认初始化配置文件
config = sampleconfig()


def analysisImg(wholeimg):
    ''' 解析图片, 需要传入 灰度图像 该方法对外公开 '''
    
    #解析              
    rtSit=GetSituation(wholeimg,config.chip_num_sample_img,
                        config.dc_num_sample_img,
                        config.pub_suit_sample_img,
                        config.pub_num_sample_img,
                        config.btnsample_img
                        )

    #入库
    '''
    if(rtSit is not None):
        result = rtSit.todict()
        result['createtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        conn = sqlite3.connect('game.db')
        df = pd.DataFrame.from_records([result])
        pd.io.sql.to_sql(df, 'depu_log', conn, if_exists='append', index=False)
    '''

    return rtSit
    
