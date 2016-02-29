#-*-coding:utf8-*-

import ctypes
import time

# def hideWindows():
whnd = ctypes.windll.kernel32.GetConsoleWindow()

if whnd != 0:
    print u'2秒后隐藏'
    time.sleep(2)
    ctypes.windll.user32.ShowWindow(whnd, 0)
    message = 'jikexueyuan\n\n窗口隐藏以后依然可以默默的运行。'
    with open('1.txt', 'w') as f:
        f.write(message)
    time.sleep(5)
    ctypes.windll.user32.ShowWindow(whnd, 1)
    ctypes.windll.kernel32.CloseHandle(whnd)

raw_input('press enter')

# def showWindows():
#     whnd = ctypes.windll.kernel32.GetConsoleWindow()
#     if whnd != 0:
#         ctypes.windll.user32.ShowWindow(whnd, 1)
#         ctypes.windll.kernel32.CloseHandle(whnd)

