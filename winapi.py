# -*- coding:utf-8 -*-
'''
    filename : winapi.py
'''
from ctypes import *
import win32con

__all__ = ['flash']

FlashWindowEx = windll.user32.FlashWindowEx

class FLASHWINFO(Structure):
    _fields_ = [('cbSize', c_uint),
                ('hwnd', c_uint),
                ('dwFlags', c_uint),
                ('uCount', c_uint),
                ('dwTimeout', c_uint)]
    
def flash(hwnd):
    '''Flash a window with caption and tray.'''
    info = FLASHWINFO(0, hwnd, win32con.FLASHW_ALL | win32con.FLASHW_TIMERNOFG, 0, 0)
    info.cbSize = sizeof(info)
    FlashWindowEx(byref(info))
    
    
    
"""
import winapi
winapi.flash(self.GetHandle())
FLASHW_ALL(0x00000003)：同时闪烁窗口标题栏和任务栏按钮，等于FLASHW_CAPTION | FLASHW_TRAY；
FLASHW_CAPTION(0x00000001)：闪烁窗口标题栏；
FLASHW_STOP(0)：停止闪烁，系统重置窗口到初始状态
FLASHW_TIMER(0x00000004)：不停的闪烁，知道FLASHW_TOP标记被设置
FLASHW_TIMERNOFG(0x0000000C):不停闪烁，直到窗口前端显示
FLASHW_TRAY(0x00000002)：闪烁窗口在任务栏的按钮；
"""