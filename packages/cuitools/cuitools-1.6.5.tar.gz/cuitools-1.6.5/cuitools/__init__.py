import glob
import math
import os
import re
import shutil
import sys
import termios
import threading

import cuitools.subp


def reset():
    print("\033[2J\033[1H")


def Input(text, normal=False, textcolor="\033[38;5;10m", dotcolor="\033[38;5;7m", usercolor="\033[38;5;12m", dot=True):
    """ \033[0m	指定をリセットし未指定状態に戻す（0は省略可）
        \033[1m	太字
        \033[2m	薄く表示
        \033[3m	イタリック
        \033[4m	アンダーライン
        \033[5m	ブリンク
        \033[6m	高速ブリンク
        \033[7m	文字色と背景色の反転
        \033[8m	表示を隠す（コピペ可能）
        \033[9m	取り消し
        """
    if not normal:
        normal = "\033[1m"
    else:
        normal = "\033[0m"
    if dot:
        inp = input(normal + textcolor + text + dotcolor + ":\033[0m" + usercolor)
    else:
        inp = input(normal + textcolor + text + usercolor)
    return inp


def Key():
    fd = sys.stdin.fileno()

    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)

    new[3] &= ~termios.ICANON
    new[3] &= ~termios.ECHO

    try:
        termios.tcsetattr(fd, termios.TCSANOW, new)
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSANOW, old)

    return ch


def Inputfilegui(title, path=None):
    terminal_size = shutil.get_terminal_size()
    # path = os.path.expanduser("/usr/share")
    if path is None:
        path = os.path.expanduser("~")
    search_text = ""
    filelist = glob.glob(path + "/" + search_text + "*")
    printdata = list(map(lambda n: os.path.basename(n) + "/" * os.path.isdir(n), filelist))
    lenfilelist = max(list(map(lambda n: subp.width_kana(n), printdata))) + 1
    print(filelist)
    print("\033[1;1H\033[2J┏" + "━" * (terminal_size[0] - 2) + "┓")
    print("\033[3;1H┣" + "━" * (terminal_size[0] - 2) + "┫")

    row = math.floor((terminal_size[0] - 2) / lenfilelist)
    # print(len(filelist),row,terminal_size[0]-2,lenfilelist)
    k = ""
    page = 0
    search = 0
    select = page * row * (terminal_size[1] - 5) + 0
    event = threading.Event()
    th = threading.Thread(target=subp.th1, args=([filelist, title, path, event]))
    th.start()
    try:
        while k != "\n" and k != "q":
            print("\033[" + str(terminal_size[1]) + ";1H┗" + "━" * (terminal_size[0] - 2) + "┛", end="")
            print("\033[4;1H", end="")
            if lenfilelist != -1:
                for i in range(math.ceil(len(printdata) / row)):
                    if i > terminal_size[1] - 6:
                        break
                    print("\033[2K┃", end="")
                    tmp = 0
                    for j in range(row):
                        if len(printdata) - 1 < page * (row * (terminal_size[1] - 5)) + (i * row + j):
                            break
                        tmp += 1
                        if select == page * row * (terminal_size[1] - 5) + (i * row + j):
                            print(
                                "\033[7m" + subp.isdir(
                                    subp.ljust_kana(printdata[page * row * (terminal_size[1] - 5) + (i * row + j)],
                                                    lenfilelist), True) + "\033[0m", end="")
                        else:
                            print(subp.isdir(
                                subp.ljust_kana(printdata[page * row * (terminal_size[1] - 5) + (i * row + j)],
                                                lenfilelist)), end="")
                    print(" " * ((terminal_size[0] - 2) - lenfilelist * tmp) + "┃")

                print(("┃" + " " * (terminal_size[0] - 2) + "┃\n") * (
                        terminal_size[1] - (math.ceil(len(printdata) / row) + 5)),
                      end="")
                print("\033[2K┃" + subp.center_kana(
                    "page " + str(page + 1) + "/" + str(math.ceil(len(printdata) / (row * (terminal_size[1] - 5)))),
                    terminal_size[0] - 2) + "┃")
            else:
                print("┃" + subp.center_kana("No file or directory", terminal_size[0] - 2) + "┃")
                print(("┃" + " " * (terminal_size[0] - 2) + "┃\n") * (terminal_size[1] - 5), end="")

            k = Key()
            if k == "\x1b":
                k = Key()
                if k == "[":
                    k = Key()
                    if k == "A":
                        if select - row > -1:
                            select -= row
                            if select < page * row * (terminal_size[1] - 5):
                                page -= 1
                    elif k == "B":
                        if select + row < len(filelist):
                            select += row
                            if select >= (page + 1) * row * (terminal_size[1] - 5):
                                page += 1
                    elif k == "C":
                        if select + 1 < len(filelist):
                            select += 1
                            if select >= (page + 1) * row * (terminal_size[1] - 5):
                                page += 1
                    elif k == "D":
                        if select - 1 > -1:
                            select -= 1
                            if select < page * row * (terminal_size[1] - 5):
                                page -= 1
                    elif k == "1":
                        k = Key()
                        if k == "5":
                            Key()
                            event.set()
                            filelist = glob.glob(path + "/" + search_text + "*")
                            print("\033[1;1H\033[2J┏" + "━" * (terminal_size[0] - 2) + "┓")
                            print("\033[3;1H┣" + "━" * (terminal_size[0] - 2) + "┫")
                            if len(filelist) != 0:
                                printdata = list(
                                    map(lambda n: os.path.basename(n) + "/" * os.path.isdir(n), filelist))
                                lenfilelist = max(list(map(lambda n: subp.width_kana(n), printdata))) + 1
                                row = math.floor((terminal_size[0] - 2) / lenfilelist)
                            else:
                                lenfilelist = -1
                            if len(filelist) - 1 < select:
                                page = 0
                                select = page * row * (terminal_size[1] - 5) + 0
                            event.clear()
                            th = threading.Thread(target=subp.th1,
                                                  args=([filelist, title, path, event, "reloaded"]))
                            th.start()
                elif k == "O":
                    k = Key()
                    if k == "S":
                        search = 1

            elif k == "\n":
                if lenfilelist == -1:
                    k = ""
                    continue
                if os.path.isdir(filelist[select]):
                    k = ""
                    search_text = ""
                    event.set()
                    path = filelist[select]
                    page = 0
                    select = page * row * (terminal_size[1] - 5) + 0
                    filelist = glob.glob(path + "/" + search_text + "*")
                    if len(filelist) != 0:
                        printdata = list(map(lambda n: os.path.basename(n) + "/" * os.path.isdir(n), filelist))
                        lenfilelist = max(list(map(lambda n: subp.width_kana(n), printdata))) + 1
                        row = math.floor((terminal_size[0] - 2) / lenfilelist)
                    else:
                        lenfilelist = -1
                    event.clear()
                    th = threading.Thread(target=subp.th1, args=([filelist, title, path, event]))
                    th.start()
            elif k == "\x7f":
                if search_text == "":
                    event.set()
                    path = "/".join(path.split("/")[:-1])
                    search_text = ""
                    page = 0
                    select = page * row * (terminal_size[1] - 5) + 0
                    filelist = glob.glob(path + "/" + search_text + "*")
                    if len(filelist) != 0:
                        printdata = list(map(lambda n: os.path.basename(n) + "/" * os.path.isdir(n), filelist))
                        lenfilelist = max(list(map(lambda n: subp.width_kana(n), printdata))) + 1
                        row = math.floor((terminal_size[0] - 2) / lenfilelist)
                    else:
                        lenfilelist = -1
                    event.clear()
                    th = threading.Thread(target=subp.th1, args=([filelist, title, path, event]))
                    th.start()
                else:
                    search_text = ""
                    event.set()
                    filelist = glob.glob(path + "/" + search_text + "*")
                    print("\033[1;1H\033[2J┏" + "━" * (terminal_size[0] - 2) + "┓")
                    print("\033[3;1H┣" + "━" * (terminal_size[0] - 2) + "┫")
                    if len(filelist) != 0:
                        printdata = list(
                            map(lambda n: os.path.basename(n) + "/" * os.path.isdir(n), filelist))
                        lenfilelist = max(list(map(lambda n: subp.width_kana(n), printdata))) + 1
                        row = math.floor((terminal_size[0] - 2) / lenfilelist)
                    else:
                        lenfilelist = -1
                    if len(filelist) - 1 < select:
                        page = 0
                        select = page * row * (terminal_size[1] - 5) + 0
                    event.clear()
                    th = threading.Thread(target=subp.th1,
                                          args=([filelist, title, path, event, "initialized"]))
                    th.start()
            if k == "\x06" or search == 1:
                event.set()
                search = 0
                print("\033[1;1H┏" + "━" * 6 + "┳" + "━" * (terminal_size[0] - 10) + "┓")
                print("┃" + subp.ljust_kana("search┃" + search_text, terminal_size[0] - 2) + "┃")
                print("┣" + "━" * 6 + "┻" + "━" * (terminal_size[0] - 10) + "┫", end="")
                redata = re.compile("\w")
                while k != "\n":
                    print("\033[2;1H┃" + subp.ljust_kana("search┃" + search_text, terminal_size[0] - 2) + "┃")
                    k = Key()
                    if redata.match(k) is not None:
                        search_text += k
                    elif k == "\x7f":
                        search_text = search_text[:-1]
                k = ""
                filelist = glob.glob(path + "/" + search_text + "*")
                print("\033[1;1H\033[2J┏" + "━" * (terminal_size[0] - 2) + "┓")
                print("\033[3;1H┣" + "━" * (terminal_size[0] - 2) + "┫")
                if len(filelist) != 0:
                    printdata = list(map(lambda n: os.path.basename(n) + "/" * os.path.isdir(n), filelist))
                    lenfilelist = max(list(map(lambda n: subp.width_kana(n), printdata))) + 1
                    row = math.floor((terminal_size[0] - 2) / lenfilelist)
                else:
                    lenfilelist = -1
                if len(filelist) - 1 < select:
                    page = 0
                    select = page * row * (terminal_size[1] - 5) + 0
                event.clear()
                th = threading.Thread(target=subp.th1, args=([filelist, title, path, event, "searched:" + search_text]))
                th.start()

    except KeyboardInterrupt:
        event.set()
        return -2
    else:
        reset()
        event.set()
        if k != "q":
            return filelist[select]
        else:
            return -1


def Inputfile(text, textcolor="\033[38;5;10m"):
    k = ""
    pk = ""
    terminal_size = shutil.get_terminal_size()
    while k != "\n":
        print(textcolor + text + ":" + pk + "\033[H")
        k = Key()
        print("\033[2J")
        if k == "\x7f":
            pk = pk[0:len(pk) - 1]
        elif k == "\n":
            pass
        elif k == "\t":
            pass
        elif k[0] != chr(92):
            pk += k
        fl = glob.glob(pk + "*")
        tfl = fl
        fl = []
        for i in tfl:
            if os.path.isdir(i):
                fl.append(os.path.basename(i) + "/")
            else:
                fl.append(os.path.basename(i))
        if k == "\t":
            if len(fl) != 0:
                fi = 1
                j = 1
                while fi != 0 and len(tfl[0]) > len(pk) + j:
                    for i in tfl:
                        # print(j)
                        if i.find(tfl[0][0:len(pk) + j]) == -1:
                            fi = 0
                            j = 0
                        elif len(tfl[0]) < len(pk) + j:
                            fi = 0
                            j = 0
                    j += 1

                if len(fl) == 1:
                    pk = tfl[0]
                elif j != 1:
                    pk = tfl[0][0:len(pk) + j]

        print("\033[" + str(int(terminal_size[1] / 2)) + ";1H" + "━" * terminal_size[0])
        if len(fl) == 0:
            fl.append("empty")
        fll = []
        for i in fl:
            fll.append(len(i))
        # print(fll)
        ps = int(terminal_size[0] / (max(fll) + 1))
        for i in range(int(terminal_size[1] / 2) - 1):
            for j in range(ps):
                try:
                    print(fl[i * ps + j] + " " * (max(fll) + 1 - len(fl[i * ps + j])), end="")
                except:
                    pass
            print("")
        print("\033[1H")
    return pk


def box(title="", printtext=None, reset_=False, place="c"):
    if printtext is None:
        printtext = []
    if reset_:
        reset()
    printtext.insert(0, title)
    printtext.append("")
    terminal_size = shutil.get_terminal_size()
    lentext = max(map(subp.width_kana, printtext))
    if place == "c":
        y = int(terminal_size[1] / 2 - len(printtext) / 2)
        x = int(terminal_size[0] / 2 - lentext / 2)
    elif place == "n":
        y = 1
        x = int(terminal_size[0] / 2 - lentext / 2)
    elif place == "nw":
        y = 1
        x = 1
    elif place == "ne":
        y = 1
        x = terminal_size[0] - lentext - 1
    elif place == "e":
        y = int(terminal_size[1] / 2 - len(printtext) / 2)
        x = terminal_size[0] - lentext - 1
    elif place == "w":
        y = int(terminal_size[1] / 2 - len(printtext) / 2)
        x = 1
    elif place == "s":
        y = terminal_size[1] - len(printtext)
        x = int(terminal_size[0] / 2 - lentext / 2)
    elif place == "sw":
        y = terminal_size[1] - len(printtext)
        x = 1
    elif place == "se":
        y = terminal_size[1] - len(printtext)
        x = terminal_size[0] - lentext - 1
    else:
        raise IndexError("placeはc,n,nw,ne,e,w,s,sw,seのみ対応しています")
    for i in range(len(printtext)):
        if i == 0:
            print("\033[" + str(y + i) + ";" + str(x) + "H┏" + subp.center_kana(printtext[i], lentext, "━") + "┓")
        elif i == len(printtext) - 1:
            print("\033[" + str(y + i) + ";" + str(x) + "H┗" + subp.center_kana(printtext[i], lentext, "━") + "┛")
        else:
            print("\033[" + str(y + i) + ";" + str(x) + "H┃" + subp.center_kana(printtext[i], lentext, " ") + "┃")


def table(printtext, listed=0):
    tabletext = []
    lentext = []
    for i in range(len(printtext[0])):
        temp = []
        for j in printtext:
            temp.append(str(j[i]))
        lentext.append(max(map(subp.width_kana, temp)))

    temp = "┏"
    for i in range(len(lentext)):
        temp += "━" * lentext[i]
        if i != len(lentext) - 1:
            temp += "┳"
        else:
            temp += "┓"

    tabletext.append(temp)

    for i in range(len(printtext)):
        temp = "┃"
        for j in range(len(printtext[i])):
            # print(subp.width_kana(str(printtext[i][j])))
            temp += subp.center_kana(str(printtext[i][j]), lentext[j], " ") + "┃"
        tabletext.append(temp)

        if i != len(printtext) - 1:
            temp = "┣"
            for j in range(len(lentext)):
                if j == len(lentext) - 1:
                    temp += "━" * lentext[j] + "┫"
                else:
                    temp += "━" * lentext[j] + "╋"
        else:
            temp = "┗"
            for j in range(len(lentext)):
                if j == len(lentext) - 1:
                    temp += "━" * lentext[j] + "┛"
                else:
                    temp += "━" * lentext[j] + "┻"
        tabletext.append(temp)
    # print(lentext)
    if listed == 1:
        return tabletext
    else:
        return "\n".join(tabletext)


def printlist(title, listdata=None, center=True):
    if listdata is None or listdata == []:
        empty = 1
        listdata = ["empty", "Press Enter Key"]
    else:
        empty = 0
    k = ""
    select = 0
    page = 0
    # event = threading.Event()
    # threadingfunc = threading.Thread(target=subp.threading, args=(title, 1, event))
    # threadingfunc.start()
    while k != "\n":
        terminal_size = shutil.get_terminal_size()
        reset()
        # print("\033[" + str(terminal_size[1] + 1) + ";0HUP/DOWN:CURSOR MOVE", end="")
        print("\033[" + str(terminal_size[1] + 1) + ";0H" + str(select + 1) + "/" + str(len(listdata)) + " " + str(
            int((select + 1) / len(listdata) * 10000) / 100) + "%", end="")
        if subp.width_kana(title) < terminal_size[0]:
            print("\033[" + "0;0H" + subp.center_kana(title, terminal_size[0], " "))
        else:
            n = subp.whilexcount(title, terminal_size[0])
            print("\033[" + "0;0H" + subp.center_kana(title, terminal_size[0], " ")[:n - 3] + "...")
        print()
        for i in range(len(listdata)):
            if i - page + 3 > 2 and i - page + 1 < terminal_size[1] - 2:
                if center:
                    if select == i:
                        # print(terminal_size[0]-(int(terminal_size[0]/2-len(listdata[i])/2)+len(listdata[i])))
                        if subp.width_kana(listdata[i]) < terminal_size[0]:
                            print(
                                "\033[" + str(i - page + 3) + ";0H\033[7m" + subp.center_kana(listdata[i],
                                                                                              terminal_size[0],
                                                                                              " ") + "\033[0m")
                        else:
                            n = subp.whilexcount(listdata[i], terminal_size[0])
                            print("\033[" + str(i - page + 3) + ";0H\033[7m" + subp.center_kana(
                                subp.center_kana(listdata[i], terminal_size[0], " ")[:n - 3] + "...", terminal_size[0],
                                " ") + "\033[0m")
                    else:
                        # print("\033[" + str(i + 3) + ";0H" + subp.center_kana(listdata[i], terminal_size[0], " "))
                        if subp.width_kana(listdata[i]) < terminal_size[0]:
                            print("\033[" + str(i - page + 3) + ";0H" + subp.center_kana(listdata[i], terminal_size[0],
                                                                                         " "))
                        else:
                            n = subp.whilexcount(listdata[i], terminal_size[0])
                            print("\033[" + str(i - page + 3) + ";0H" + subp.center_kana(
                                subp.center_kana(listdata[i], terminal_size[0], " ")[:n - 3] + "...", terminal_size[0],
                                " "))
                else:
                    if select == i:
                        # print(terminal_size[0]-(int(terminal_size[0]/2-len(listdata[i])/2)+len(listdata[i])))
                        if subp.width_kana(listdata[i]) < terminal_size[0]:
                            print(
                                "\033[" + str(i - page + 3) + ";0H\033[7m" + subp.ljust_kana(listdata[i],
                                                                                             terminal_size[0],
                                                                                             " ") + "\033[0m")
                        else:
                            n = subp.whilexcount(listdata[i], terminal_size[0])
                            print("\033[" + str(i - page + 3) + ";0H\033[7m" + subp.ljust_kana(
                                subp.center_kana(listdata[i], terminal_size[0], " ")[:n - 3] + "...", terminal_size[0],
                                " ") + "\033[0m")
                    else:
                        # print("\033[" + str(i + 3) + ";0H" + subp.center_kana(listdata[i], terminal_size[0], " "))
                        if subp.width_kana(listdata[i]) < terminal_size[0]:
                            print("\033[" + str(i - page + 3) + ";0H" + subp.ljust_kana(listdata[i], terminal_size[0],
                                                                                        " "))
                        else:
                            n = subp.whilexcount(listdata[i], terminal_size[0])
                            print("\033[" + str(i - page + 3) + ";0H" + subp.ljust_kana(
                                subp.center_kana(listdata[i], terminal_size[0], " ")[:n - 3] + "...", terminal_size[0],
                                " "))
        k = Key()
        if k == "\x1b":
            k = Key()
            if k == "[":
                k = Key()
                if k == "A":
                    if select != 0:
                        if select - page != 0:
                            select -= 1
                        else:
                            page -= 1
                            select -= 1
                elif k == "B":
                    if len(listdata) - 1 != select:
                        if select - page + 2 != terminal_size[1] - 2:
                            select += 1
                        else:
                            page += 1
                            select += 1
    reset()
    if empty == 1:
        return -1
    else:
        return select
