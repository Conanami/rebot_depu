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
# from read_pc_depu import analysisImg
from multiprocessing import Queue
from alltitle import findTitle
# import player as p

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # logging.basicConfig函数对日志的输出格式及方式做相关配置

'''
    德州扑克截图工具, 每3秒录制一次屏幕
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

def get_total_area():
    '''   获取整个应用区域  '''
    window_title = findTitle('德州扑克')
    print(window_title)
    if not window_title:
        print('没有找到应用')
        return 0,0,0,0 

    hwnd = win32gui.FindWindow(win32con.NULL,window_title)
    if hwnd == 0 :
        print('%s not found' % window_title)
        return 0,0,0,0 

    window_left,window_top,window_right,window_bottom = win32gui.GetWindowRect(hwnd)
    return window_left,window_top,window_right,window_bottom


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

@async
def run_game(q):
    lastkey = keyboard.Key.esc
    while True:
        if not q.empty():
            key =  q.get(True)
            print('msg %s' % key)
            lastkey = key
            
        if lastkey == keyboard.Key.esc:
            print('wait')
            time.sleep(1.0)
            continue
        elif lastkey == keyboard.KeyCode.from_char('p'):
            # 截屏
            print('take photo')
            window_left,window_top,window_right,window_bottom  = get_total_area()
            pyautogui.moveTo(window_left,window_top)
            total_image = grab_screen(window_left,window_top, window_right, window_bottom)
            total_image.save(r'tmp\pokerstars\%s.png' % time.strftime("%d%H%M%S", time.localtime()))

            lastkey = keyboard.Key.esc
        elif (lastkey == keyboard.KeyCode.from_char('r') or lastkey == keyboard.KeyCode.from_char('R')):
            print('take photo')
            window_left,window_top,window_right,window_bottom  = get_total_area()
            pyautogui.moveTo(window_left,window_top)
            total_image = grab_screen(window_left,window_top, window_right, window_bottom)
            total_image.save(r'tmp\pokerstars\%s.png' % time.strftime("%d%H%M%S", time.localtime()))
        else:
            lastkey = keyboard.Key.esc
            pass
        time.sleep(5)

if __name__ == '__main__':
    q = Queue()
    run_game(q)
    run_monitor_key(q)


