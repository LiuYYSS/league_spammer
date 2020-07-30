# -*- coding: UTF-8 -*-
import time
import pyautogui as g
import requests
import pyperclip
import keyboard
import threading
import random
import jieba
import win32api
import win32con
import win32gui
from pypinyin import lazy_pinyin, Style
# import pydirectinput as g


enable = False
shuffle = False
activate_key = "F8"
deactivate_key = "F9"
exit_key = "F10"
language_source = "和谐版语料库"


def getMessageOnline():
    url = 'https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn'  # 需要爬数据的网址
    page = requests.Session().get(url)
    text = page.text + "\n"
    print(text)
    pyperclip.copy(text)
    g.a("ctrl", "v")


def getMessageOfflineWithPinYin(message):
    print(message)
    message = message.strip()
    g.press("enter")
    temp = jieba.cut(message)
    temp = list(temp)
    temp = [lazy_pinyin(word, style=Style.NORMAL) for word in temp]
    for pinyin in temp:
        word_pinyin = "".join(pinyin)
        g.typewrite(word_pinyin)
        g.press("space")
    g.press("enter")
    lock.release()


def listen_operation_cmd():
    global enable
    while True:
        if keyboard.is_pressed('F8') and not enable:
            enable = True
            print("开始")
        if keyboard.is_pressed('F9') and enable:
            enable = False
            print("结束了")
        if keyboard.is_pressed('F10'):
            exit()


if __name__ == "__main__":
    lock = threading.Lock()
    wait_time = 0.1
    last_call_time = time.time()
    sentence_source = open('和谐版语料库', encoding='utf-8')
    lines = sentence_source.readlines()
    if shuffle:
        random.shuffle(lines)
    lines_index = 0
    t1 = threading.Thread(target=listen_operation_cmd)
    t1.start()
    jieba.initialize()
    print("程序启动成功 F8:开始 F9:停止 F10:退出")

    while True:
        time.sleep(0)
        lock.acquire()
        if enable and time.time() - last_call_time > wait_time:
            hwnd = win32gui.GetForegroundWindow()
            result = win32api.SendMessage(hwnd, win32con.WM_INPUTLANGCHANGEREQUEST, 0, 0x8040804)
            if lines_index == len(lines):
                lines_index = 0
                if shuffle:
                    random.shuffle(lines)
            t2 = threading.Thread(target=getMessageOfflineWithPinYin, args=[lines[lines_index], ])
            t2.start()
            last_call_time = time.time()
            # getMessageOfflineWithPinYin(lines[lines_index])
            lines_index += 1
        if not enable:
            lock.release()
