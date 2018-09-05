from PIL import Image
from skimage import io,data
import time
import numpy as np
import pandas as pd
import sqlite3

#定义一个牌的类
class card:
    def __init__(self,suit,num):
        self.suit=suit
        self.num=num
    def __str__(self):
        suitlist=['黑','红','梅','方']
        clist=['na','A','2','3','4','5','6','7','8','9','10','J','Q','K','A']
        if(self.suit is None or self.num is None):
            return "none"
        elif(self.num==-1):
            return "na"
        else:
            return suitlist[self.suit]+"|"+clist[self.num]

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
    # print('img.shape %s' % img)
    # print('sample.shape %s' % sample)
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
    return None

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
        return (float(numstr)*10000)
    else:
        #如果没有万，就正常返回
        return (float(numstr))

#得到每个人的数字
def PicListToNum(wholeimg,betboxlist,start,chip_num_sample_img,num_step,point_step):
    i=0
    result = {}
    for betbox in betboxlist:
        betsize=SinglePicToNum(wholeimg,betbox,start,chip_num_sample_img,num_step,point_step)
        result[i] = betsize
        print(str(i)+':'+str(betsize))
        i=i+1
    return result

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

def readCard(wholeimg,suitbox,suit_sample_img,numbox,num_sample_img,numlist,thres):
    rtcard=card(-1,-1)
    tmpnum=getNumFromList(wholeimg,numbox,num_sample_img,thres)
    if(tmpnum is None):
        rtcard.num = None
    else:
        rtcard.num=numlist[tmpnum]
    rtcard.suit=getNumFromList(wholeimg,suitbox,suit_sample_img,thres)
    return rtcard

def PicListToStatus(wholeimg,staboxlist,status_sample_img):
    rtlist=[]
    for tmpbox in staboxlist:
        mybox=(tmpbox.x1,tmpbox.y1,tmpbox.x2,tmpbox.y2)
        rtlist.append(getNumFromList(wholeimg,mybox,status_sample_img))
    return rtlist

#得到7张牌
def getCardlist(wholeimg,thres, result):
    rtlist=[]
    numlist=[2,3,4,5,6,7,8,9,10,11,12,13,14,10,8,12]
    #clist=['2','3','4','5','6','7','8','9','T','J','Q','K','A','T','8','Q']

    #本人的第一张牌的花色
    firstsuitbox=(618,433,631,447)
    first_suit_sample=[r'depu\samples\first_suit\1_s.png',r'depu\samples\first_suit\1_h.png',
        r'depu\samples\first_suit\1_c.png',r'depu\samples\first_suit\1_d.png']
    first_suit_sample_img=file2img(first_suit_sample)
    # 第一张牌的数字
    firstnumbox=(614,414,628,433)
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
    first_num_sample_img=file2img(first_num_sample)

    card1=readCard(wholeimg,firstsuitbox,first_suit_sample_img,firstnumbox,first_num_sample_img,numlist,thres)
    result['my1'] = '%s|%s' % (card1.num, card1.suit)
    #print(suitlist[card1.suit]+'|'+clist[card1.num])
    print('第一张牌 %s ' % card1)
    rtlist.append(card1)

    #第二张牌
    secondsuitbox=(648,431,661,445)
    second_suit_sample=[r'depu\samples\second_suit\2_s.png',r'depu\samples\second_suit\2_h.png'
        ,r'depu\samples\second_suit\2_c.png',r'depu\samples\second_suit\2_d.png']
    second_suit_sample_img=file2img(second_suit_sample)
    secondnumbox=(649,412,663,431)
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
    second_num_sample_img=file2img(second_num_sample)

    card2=readCard(wholeimg,secondsuitbox,second_suit_sample_img,secondnumbox,second_num_sample_img,numlist,thres)
    result['my2'] = '%s|%s' % (card2.num, card2.suit)
    #print(suitlist[card2.suit]+'|'+clist[card2.num])
    print('第二张牌 %s ' % card2)
    rtlist.append(card2)
    
    #所有的公共牌
    x1=425
    x2=441
    y1=262
    y2=279
    pubsuitbox=(x1,y1,x2,y2)
    pub_suit_sample=[r'depu\samples\pub_suit\p_s.png',r'depu\samples\pub_suit\p_h.png'
        ,r'depu\samples\pub_suit\p_c.png',r'depu\samples\pub_suit\p_d.png']
    pub_suit_sample_img=file2img(pub_suit_sample)
    pub_num_sample=[r'depu\samples\pub_num\p_2.png',r'depu\samples\pub_num\p_3.png',r'depu\samples\pub_num\p_4.png'
                    ,r'depu\samples\pub_num\p_5.png',  \
                    r'depu\samples\pub_num\p_6.png',r'depu\samples\pub_num\p_7.png',r'depu\samples\pub_num\p_8.png'
                    ,r'depu\samples\pub_num\p_9.png', \
                    r'depu\samples\pub_num\p_t.png',r'depu\samples\pub_num\p_j.png',r'depu\samples\pub_num\p_q.png'
                    ,r'depu\samples\pub_num\p_k.png',r'depu\samples\pub_num\p_a.png', \
                    r'depu\samples\pub_num\p_tr.png',r'depu\samples\pub_num\p_8r.png',r'depu\samples\pub_num\p_qr.png']
    pub_num_sample_img=file2img(pub_num_sample)
    #拿5张公共牌
    for i in range(5):
        pubsuitbox=((x1+i*62),y1,x2+i*62,y2)
        pubnumbox=((423+i*62),237,(439+i*62),261)
        tmpcard=readCard(wholeimg,pubsuitbox,pub_suit_sample_img,pubnumbox,pub_num_sample_img,numlist,thres)
        if tmpcard.num:
            result['pub%d' % (i+1)] = '%s|%s' % (tmpcard.num, tmpcard.suit)
        else:
            result['pub%d' % (i+1)] = None
        rtlist.append(tmpcard)

    return rtlist

#得到底池各种信息
def readimg(wholeimg):
    ''' 读取图片的信息  '''
    result = {}
    start =time.clock()
    # file_name=r'depu\0828\dz_28191925.png'
    # file_name=r'depu\dz_sample\dz_23163621.png' 
    # wholeimg=Image.open(file_name).convert('L')
    thres=80
    # cardlist=[]
    getCardlist(wholeimg,thres, result)
    if 'None' in result['my1']:
        # 读取我的牌面失败，退出
        print('无效页面')
        return
    # for card in cardlist:
    #     print(card)
    num_step=7
    point_step=3
    
    #底池大小范围
    x1=530
    x2=620
    y1=187
    y2=202
       
    
    numstart=0
    dcpicbox=picbox(x1,y1,x2,y2)
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
    
    dc_num_sample_img=file2img(dc_num_sample)
    potsize=SinglePicToNum(wholeimg,dcpicbox,numstart,dc_num_sample_img,num_step,point_step)
    result['potsize'] = potsize
    print('potsize:'+str(potsize))
    
   
    #下面是读筹码的情况
    
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

    chip_num_sample_img=file2img(chip_num_sample)
    
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
    r =  PicListToNum(wholeimg,chipboxlist,numstart,chip_num_sample_img,num_step,point_step)
    result['chip1'] = r[0] 
    result['chip2'] = r[1]
    result['chip3'] = r[2]
    result['chip4'] = r[3]
    result['chip5'] = r[4]
    result['chip6'] = r[5]

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
    r = PicListToNum(wholeimg,betboxlist,numstart,chip_num_sample_img,num_step,point_step)
    result['dc1'] = r[0] 
    result['dc2'] = r[1]
    result['dc3'] = r[2]
    result['dc4'] = r[3]
    result['dc5'] = r[4]
    result['dc6'] = r[5]
    
    #读所有的状态
    #每个人的状态样本
    status_sample=[r'depu\samples\status\status_fold.png', 
                    r'depu\samples\status\status_check.png', 
                    r'depu\samples\status\status_call.png', 
                    r'depu\samples\status\status_raise.png' 
    ]
    status_sample_img=file2img(status_sample)
    staWidth=30
    staHeight=16
    staboxlist=[picbox(555,389,555+staWidth,389+staHeight), \
                picbox(156,210,156+staWidth,210+staHeight), \
                picbox(342,57,342+staWidth,57+staHeight), \
                picbox(759,57,759+staWidth,57+staHeight), \
                picbox(951,210,951+staWidth,210+staHeight), \
                picbox(779,388,779+staWidth,388+staHeight)
                ]
    statuslist = PicListToStatus(wholeimg,staboxlist,status_sample_img)
    result['status1'] = statuslist[0]
    result['status2'] = statuslist[1]
    result['status3'] = statuslist[2]
    result['status4'] = statuslist[3]
    result['status5'] = statuslist[4]
    result['status6'] = statuslist[5]

    numstart=0
    #得到大盲注，玩的级别
    bbWidth=80
    bbHeight=15
    bbbox=picbox(592,335,592+bbWidth,335+bbHeight)
    blind = SinglePicToNum(wholeimg,bbbox,numstart,dc_num_sample_img,num_step,point_step)
    if r'/' in str(blind):
        print('大盲注 %s' % blind.split('/')[1])
        result['bbnum'] = blind.split('/')[1]
    else:
        result['bbnum'] = '0'
    
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
    btnsample=[r'depu\samples\btn_sample.png']
    btnsample_img=file2img(btnsample)
    btn=findSampleInList(wholeimg,btnsample_img[0],btnboxlist)
    print(btn)
    result['btnpos'] = btn 

    #得到需要跟注的数量
    #跟注大小数字
    call_num_sample=[r'depu\samples\call_num\call_0.png', 
                    r'depu\samples\call_num\call_1.png', 
                    r'depu\samples\call_num\call_2.png', 
                    r'depu\samples\call_num\call_3.png', 
                    r'depu\samples\call_num\call_4.png', 
                    r'depu\samples\call_num\call_5.png', 
                    r'depu\samples\call_num\call_6.png', 
                    r'depu\samples\call_num\call_7.png', 
                    r'depu\samples\call_num\call_8.png', 
                    r'depu\samples\call_num\call_9.png', 
                    r'depu\samples\call_num\call_dot.png', 
                    r'depu\samples\call_num\call_wan.png' ]
    call_num_sample_img=file2img(call_num_sample)
    x1=445
    y1=543
    x2=490
    y2=559
    callbox=picbox(x1,y1,x2,y2)
    numstart=0
    callchip=SinglePicToNum(wholeimg,callbox,numstart,call_num_sample_img,11,4)
    if(callchip<=0): callchip=0
    result['callchip'] = callchip
    
    #计算运行时间
    end = time.clock()
    print('Running time: %s Seconds'%(end-start))
    
    result['createtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(result)
    conn = sqlite3.connect('game.db')
    df = pd.DataFrame.from_records([result])
    pd.io.sql.to_sql(df, 'depu_log', conn, if_exists='append', index=False)

if __name__ == '__main__':
    # file_name=r'depu\0828\dz_28191925.png'
    file_name=r'tmp\0903\dz_03224028.png'
    wholeimg=Image.open(file_name).convert('L')
    readimg(wholeimg)