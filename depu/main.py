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
from threading import Thread
from pynput import keyboard
from pynput.keyboard import Listener
from read_pc_depu import analysisImg
from read_pc_depu import NeedAnalyse
from multiprocessing import Queue
import player as p

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置

'''
    德州扑克截图工具, 每三秒录制一次
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

def get_gamescreen_area():
    ''' 获取区域 '''
    window_title = '天天德州扑克'
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    hwnd = win32gui.FindWindow(win32con.NULL,window_title)
    if hwnd == 0 :
        print('%s not found' % window_title)
        return 0,0,0,0

    window_left,window_top,window_right,window_bottom = win32gui.GetWindowRect(hwnd)
    # logging.info('find window size complete %s %s %s %s ' % (window_left,window_top,window_right,window_bottom))
    if min(window_left,window_top) < 0\
        or window_right > screen_width\
        or window_bottom > screen_height:
        print('window is at wrong position')
        return 0,0,0,0
    window_width = window_right - window_left
    window_height = window_bottom - window_top
    
    #区域大小是固定的 1155*650  使用默认大小进行游戏
    game_area_width = 1155
    game_area_height = 650

    game_area_left = window_left + (window_width - game_area_width)/2
    game_area_top = window_top +70
    
    return game_area_left, game_area_top, game_area_width, game_area_height

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
    #kind, no = 3,4
    logging.info('完成决策， 结果 %s %s' %(kind, no))
    if kind==0:
        #弃牌
        target = 350, 550
    elif kind == 1 or kind==2:
        # 追加
        target = 508, 550
    elif kind ==3:
        if no==1:
            target = 590, 550
        elif no==2:
            target = 700, 550
        elif no==3:
            target = 800, 550
        elif no==4:
            allin(game_area_left,game_area_top)
            
    if target[0]:
        pyautogui.moveTo(game_area_left+target[0],game_area_top+target[1])
        pyautogui.click()

#全下
def allin(game_area_left,game_area_top):
    pyautogui.moveTo(game_area_left+300,game_area_top+600)
    pyautogui.dragTo(game_area_left+663,game_area_top+600,1.0)
    pyautogui.moveTo(game_area_left+750,game_area_top+600)           
    pyautogui.click()

@async
def run_game(q):
    lastkey = keyboard.Key.esc
    needCnt = 0
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
            game_area_left, game_area_top, game_area_width, game_area_height = get_gamescreen_area()
            if game_area_left:
                #pyautogui.moveTo(game_area_left,game_area_top)
                game_area_image = get_game_data(game_area_left, game_area_top, game_area_width, game_area_height)
                #如果需要解析
                logging.info('是否需要解析:'+str(needCnt))
                if ( NeedAnalyse (game_area_image.convert('L'))): 
                    if(needCnt>=2):
                        logging.info('开始解析图像')
                        rt = analysisImg(game_area_image.convert('L'))
                        logging.info('完成解析图像')
                        if(rt is not None):
                            game_area_image.save(r'tmp/dz_%s%s.png' % (time.strftime("%m%d", time.localtime()), time.strftime("%H%M%S", time.localtime())))
                            handle(game_area_left, game_area_top, rt)
                    else: needCnt=needCnt+1
                else:
                    needCnt=0
        else:
            lastkey = keyboard.Key.esc
            pass
        time.sleep(0.8)

if __name__ == '__main__':
    q = Queue()
    run_game(q)
    run_monitor_key(q)


