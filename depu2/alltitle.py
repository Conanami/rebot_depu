#! /usr/bin/env python
# -*- coding: utf-8 -*-
from win32gui import *
titles = set()
def foo(hwnd,mouse):
    #去掉下面这句就所有都输出了，但是我不需要那么多
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
    #if IsWindow(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))

def findTitle(title):
    EnumWindows(foo, 0)
    lt = [t for t in titles if t]
    lt.sort()
    for t in lt:
        if title in t:
            return t
    return None

# r = findTitle('发起会话')
# print(r)
