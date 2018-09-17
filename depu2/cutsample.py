from PIL import Image
from skimage import io,data,color



#得到两张牌的花色
def cutsample():

    
    
       
    # MatchPicToSample(r'.\dz_sample\dz_22164924.png',(225,530,371,574),'fold.png')
    
    
    
    #底池数字切割的显示范围
    #box=(530,187,620,202)
    #第一位数字

    #box=(573,187,580,202)
    #小数点本身
    #box=(581,187,584,202)
    #小数点后一位
    #box=(585,187,592,202)
    #第四位数字
    #box=(597,187,604,202)
    #第二位数字
    #box=(581,187,588,202)
    
    #切割第一张手牌的花色
    #box=(618,433,631,447)
    #切割第二张手牌的花色
    #box=(648,431,661,445)
    #切割第一张手牌的数字
    #box=(614,414,628,433)
    #切割第二张手牌的数字
    #box=(649,412,663,431)
    
    #切割半个万字出来
    #box=(594,187,601,202)
    img=Image.open(r'tmp\dz_0917174517.png')  #打开图像
    

    
    x1=63
    y1=182
    w=9
    h=14
    box=(x1,y1,x1+w,y1+h)
    roi=img.crop(box)
    dc_name='chip_dot.png'
        #sample_name='fold.png'
    roi.save(dc_name)
    roi.show()
    #切割中间的5张牌的数字
    #切割中间的花色
    '''
    x1=357
    y1=116
    w=9
    h=14
    s=9
    for i in range(6):
        #中间5张的数字
        box=((x1+i*s),y1,(x1+w+i*s),y1+h)
        #中间5张的花色
        #box=((425+i*62),262,441+i*62,279)
        roi=img.crop(box)
        dc_name='chip'+str(i)+'.png'
        #sample_name='fold.png'
        roi.save(dc_name)
        roi.show()

    '''
    
cutsample()