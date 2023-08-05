import glob
import math
import os
import re
import shutil
import subprocess
import threading
import unicodedata
import cuitools.__init__

# def threading(text,y,event,before=""):
#
#     no = 0
#     while True:
#         terminal_size = shutil.get_terminal_size()
#         temp = terminal_size
#         while terminal_size[0] < width_kana(text):
#             terminal_size = shutil.get_terminal_size()
#             count = 0
#             n = 0
#             for i in text:
#                 count += width_kana(i)
#                 n += 1
#                 # print(width_kana(i))
#                 if count >= terminal_size[0]:
#                     break
#             if count > terminal_size[0]:
#                 n -= 1
#             print(before+"\033["+str(y)+";0H\033[2K"+center_kana(text,terminal_size[0]," ")[no:no+n])
#             if event.wait(timeout=0.5):
#                 break
#             no += 1
#             if no > len(text)-int(terminal_size[0]/3):
#                 no = 0
#         no = 0
#         print("\033["+str(y)+";0H"+center_kana(text, terminal_size[0], " "))
#         if event.wait(timeout=0.1):
#             break
#         terminal_size = shutil.get_terminal_size()
#         if terminal_size != temp:
#             cuitools.__init__.reset()


def isdir(path, select=False):
    if len(path.split("/")) == 2:
        nselect = not select
        return "\033[38;5;12m" * nselect + path.split("/")[0] + "\033[0m" + "\033[7m" * select + "/" + path.split("/")[
            1]
    else:
        return path


def th1(data, title, path, event, text=None):
    terminal_size = shutil.get_terminal_size()
    lentitle = width_kana(path)
    if text is not None:
        print("\033[2;1H┃" + ljust_kana(text, terminal_size[0] - 2) + "┃")
        if event.wait(timeout=1):
            pass
    print("\033[2;1H┃" + ljust_kana("total " + str(len(data)), terminal_size[0] - 2) + "┃")
    if event.wait(timeout=1):
        pass
    if lentitle + 1 < terminal_size[0] - 2:
        print("\033[2;1H┃" + ljust_kana(path + "/", terminal_size[0] - 2) + "┃")
    else:
        print("\033[2;1H┃" + ljust_kana("..." + path[(terminal_size[0] - 6) * -1:] + "/", terminal_size[0] - 2) + "┃")
        # print("\033[2;1H┃..." + ljust_kana(path[(terminal_size[0]-5)*-1:], terminal_size[0] - 2) + "┃")
    if event.wait(timeout=1):
        pass
    else:
        lentitle = width_kana(title)
        if lentitle < terminal_size[0] - 2:
            print("\033[2;1H┃" + ljust_kana(title, terminal_size[0] - 2) + "┃")
        else:
            print("\033[2;1H┃" + ljust_kana(title[:terminal_size[0] - 5] + "...", terminal_size[0] - 2) + "┃")


def whilexcount(text, x):
    count = 0
    n = 0
    for i in text:
        count += width_kana(i)
        n += 1
        # print(width_kana(i))
        if count >= x:
            break
    if count > x:
        n -= 1
    return n


def count_zen(str):
    n = 0
    for c in str:
        wide_chars = "WFA"
        eaw = unicodedata.east_asian_width(c)
        if wide_chars.find(eaw) > -1:
            n += 1
    return n


def width_kana(str):
    all = len(str)  # 全文字数
    zenkaku = count_zen(str)  # 全角文字数
    hankaku = all - zenkaku  # 半角文字数

    return zenkaku * 2 + hankaku


def center_kana(str, size, pad=" "):
    space = size - width_kana(str)
    if space > 0:
        str = pad * int(math.floor(space / 2.0)) + str + pad * int(math.ceil(space / 2.0))
    return str


def get_lines(cmd):
    '''
    :param cmd: str 実行するコマンド.
    :rtype: generator
    :return: 標準出力 (行毎).
    '''
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline()
        if line:
            yield line

        if not line and proc.poll() is not None:
            break


def ljust_kana(str, size, pad=" "):
    space = size - width_kana(str)
    if space > 0:
        str = str + pad * space
    return str
