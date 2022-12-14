import os
from skimage import io,data,color
import PIL.ImageGrab
from PIL import Image
import pyautogui
import win32api
import win32gui
import win32con
import numpy
import time
import hashlib,random
import logging
import random
from threading import Thread
from pynput import keyboard
from pynput.keyboard import Listener
from read_pokerstar import analysisImg
from read_pokerstar import NeedAnalyse
from read_pokerstar import NeedBackseat
from multiprocessing import Queue
from alltitle import findTitle
import player as p

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置

#得到玩的级别
def getLevel(topic):
    tmplevel=topic[topic.find('/')+1:len(topic)]
    tmplevel=tmplevel[:tmplevel.find('美')]
    print( str(tmplevel))
    #tmplevel=100
    return float(tmplevel)

'''
    德州扑克截图工具, 按下 P 录制屏幕

    更改启动方式，  修改 玩家BenJamin.Thomas登录 为 自己的账户即可。
'''

def async(f):
    ''' 异步装饰方法 '''
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def grab_screen(left,top,right,bottom):
        return PIL.ImageGrab.grab((left,top,right,bottom))

def copy_part_image(image_,left,top,right,bottom):
    return image_.crop((left,top,right,bottom))

def checkTeamView():
    ''' check teamview exist '''
    window_title = findTitle('发起会话')
    if not window_title:
        return
    print('find teamview dialog')
    hwnd = win32gui.FindWindow(win32con.NULL,window_title)
    if hwnd == 0 :
        print('%s not found' % window_title)
        return 

    window_left,window_top,window_right,window_bottom = win32gui.GetWindowRect(hwnd)
    # print(window_left,window_top,window_right,window_bottom)
    pyautogui.moveTo(window_left+411,window_top+144)
    pyautogui.click()

def get_total_area():
    '''   获取整个应用区域  '''
    checkTeamView()

    window_title = findTitle('无限注')
    #print(window_title)
    if not window_title:
        print('没有找到应用')
        return 0,0,0,0,window_title 

    hwnd = win32gui.FindWindow(None,window_title)
    if hwnd == 0 :
        print('%s not found' % window_title)
        return 0,0,0,0,window_title

    window_left,window_top,window_right,window_bottom = win32gui.GetWindowRect(hwnd)
    return window_left,window_top,window_right,window_bottom,window_title


def get_game_data(game_area_left, game_area_top, game_area_width, game_area_height):
    '''  获取区域的图像数据   '''
    game_area_image = grab_screen(game_area_left,game_area_top,
                                      game_area_left + game_area_width, game_area_top + game_area_height)
    # game_area_image.save(r'dz_sample/dz_%s.png' % time.strftime("%d%H%M%S", time.localtime()))
    return game_area_image

def on_release(key):
    print('{0} released'.format(key))
    q.put(key)

@async
def run_monitor_key(q):
    ''' 监听键盘事件 '''
    with Listener(on_release=on_release) as listener:
        listener.join()

def handle(game_area_left, game_area_top, rtSit):
    '''  处理结果 '''
    target = 0, 0
    logging.info('开始决策')
    kind, no = p.makeDecision(rtSit)


    #kind, no = 3,5
    #if kind==3 and no==5:
        #测试点击
    #    target=p.getDragTarget(0.3)
    #    dragbet(game_area_left,game_area_top,target)

    logging.info('完成决策， 结果 %s %s' %(kind, no))
    if kind==0:
        #弃牌
        target = 500, 550
    elif kind == 1 or kind==2:
        # 追加
        target = 640, 550
        raisebet(game_area_left,game_area_top,target)
    
    elif kind ==3:
        if no==1:
            target = 650, 480
        elif no==2:
            target = 650, 480
        elif no==3:
            target = 700, 480
        elif no==4:
            target = 750, 480
        
            #allin(game_area_left,game_area_top)
        raisebet(game_area_left,game_area_top,target)

    if target[0] and kind==0:
        pyautogui.moveTo(game_area_left+target[0]+random.randint(0,10),game_area_top+target[1]+random.randint(0,10))
        pyautogui.click()

#下注
def raisebet(game_area_left,game_area_top,target):
    pyautogui.moveTo(game_area_left+target[0]+random.randint(0,10),game_area_top+target[1]+random.randint(0,2),0.17)
    pyautogui.click()
    betbtn=750,550
    pyautogui.moveTo(game_area_left+betbtn[0]+random.randint(0,10),game_area_top+betbtn[1]+random.randint(0,10),0.19)
    pyautogui.click()

#拖动下注
def dragbet(game_area_left,game_area_top,target):
    pyautogui.moveTo(game_area_left+645,game_area_top+503)
    pyautogui.dragTo(game_area_left+target[0],game_area_top+target[1],0.6)
    betbtn=750,550
    pyautogui.moveTo(game_area_left+betbtn[0]+random.randint(0,10),game_area_top+betbtn[1]+random.randint(0,10),0.3)
    pyautogui.click()

#点击回到座位
def ClickBackSeat(game_area_left,game_area_top):
    backseatpos=650,509
    pyautogui.moveTo(game_area_left+backseatpos[0]+random.randint(0,10),game_area_top+backseatpos[1]+random.randint(0,10),0.3)
    pyautogui.click()


@async
def run_game(q):
    lastkey = keyboard.Key.esc
    needCnt=0
    while True:
        
        if not q.empty():
            key =  q.get(True)
            print('msg %s' % key)
            lastkey = key
                
        if lastkey == keyboard.Key.esc:
            print('wait')
            time.sleep(1.0)
            continue
        elif (lastkey == keyboard.KeyCode.from_char('r') or lastkey == keyboard.KeyCode.from_char('R')):
            #检测目标是否存在
            AnswerFlag=True
            window_left,window_top,window_right,window_bottom,window_title  = get_total_area()
            if window_left:
                #pyautogui.moveTo(game_area_left,game_area_top)
                game_area_image = get_game_data(window_left, window_top, window_right-window_left, window_bottom-window_top)
                
                #game_area_image.save(r'tmp/dz_%s%s.png' % (time.strftime("%m%d", time.localtime()), time.strftime("%H%M%S", time.localtime())))
                if ( NeedBackseat(game_area_image.convert('L')) ):
                    logging.info('回到座位了')
                    ClickBackSeat(window_left,window_top)
                else:
                    logging.info('是否需要解析:'+str(needCnt))
                    if ( NeedAnalyse (game_area_image.convert('L'))): 
                        if(needCnt>=1):
                            logging.info('开始解析图像')
                            levelbb=getLevel(window_title)
                            rt = analysisImg(game_area_image.convert('L'),levelbb)
                            logging.info('完成解析图像')
                            if(rt is not None):
                                game_area_image.save(r'tmp/dz_%s%s.png' % (time.strftime("%m%d", time.localtime()), time.strftime("%H%M%S", time.localtime())))
                                #如果赚了2块，就退出不玩了，这样测试可以保证每天的盈利
                                #if(rt.chiplist[rt.myseat]<200*rt.bb):
                                handle(window_left, window_top, rt)
                        else: needCnt=needCnt+1
                    else:
                        needCnt=0
                
            time.sleep(0.8)
        else:
            lastkey = keyboard.KeyCode.from_char('r') 
            pass
        

if __name__ == '__main__':
    q = Queue()
    run_game(q)
    run_monitor_key(q)


