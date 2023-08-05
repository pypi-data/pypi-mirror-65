from os import path
import os
import time
import pickle
import inspect


def find_the_longest(dic):
    global h
    dk = list(dic.keys())
    h = 0
    ht = ""
    for w in dk:
        if len(w) > h:
            h = len(w)
            ht = w
    # print(h)
    # print(ht)


def openfile(ch=True, ti=True, ha=True, add=True):
    # dic = [] #list
    dic = {}
    # with open ("path.join(fpath, "dict_no_space.txt"),"r",encoding= "utf8",errors= "ignore") as f:
    #     for line in f :
    #         # dic.append(line[0:-1]) #list
    #         dic[line[0:-1]]=0

    fpath = path.split(path.abspath(inspect.getfile(openfile)))[0]

    with open(path.join(fpath, "data", "ch_dict_no_space.pickle"), "rb") as f:
        ch_dic = pickle.load(f)
        # print(dic)

    with open(path.join(fpath, "data", "ti_dict.pickle"), "rb") as f:
        ti_dic = pickle.load(f)
        # print(dic)

    with open(path.join(fpath, "data", "ha_dict.pickle"), "rb") as f:
        ha_dic = pickle.load(f)
        # print(dic)

    with open(path.join(fpath, "data", "dict_add.txt"), "r", encoding="utf8", errors="ignore") as da:
        add_dic = {}
        for line in da:
            # dic.append(line[0:-1]) #list
            add_dic[line[0:-1]] = 0
            # print(line)

    all_dic = {**ch_dic, **ti_dic, **ha_dic, **add_dic}

    if ch:
        dic = {**dic, **ch_dic}

    if ti:
        dic = {**dic, **ti_dic}

    if ha:
        dic = {**dic, **ha_dic}

    if add:
        dic = {**dic, **add_dic}
    symbol = {'9', '|', '/', ')', 'B', 'P', '@', 'b', 'A', '，', '$', '1', 'y', ']', 't', '？', '&', 'w', 'K', 'g', '*', '=', '_', 's', 'D', ';', 'z', '"', '>', '2', '%', 'V', 'i', 'n', 'f', 'J', '0', '\\', 'M', '+', 'R', '#', "'", 'S', 'x', '`', 'r', '{', 'q', ' ', 'k',
              'u', ':', 'E', '「', '}', 'Q', 'C', '3', '~ ', '」', 'j', '-', '6', '7', 'H', 'T', 'p', 'a', '<', '!', 'X', 'l', 'd', 'W', 'm', '~', '5', '?', '、', 'Z', '8', '(', '4', 'e', 'c', 'N', '：', '[', 'o', 'I', 'v', 'U', 'G', '^', 'L', 'h', '。', 'O', ',', 'F', 'Y', '.'}
    return all_dic, dic, symbol


def get_len(dic, symbol, sentence):
    global h
    length = []
    for i in range(0, len(sentence)):
        length.append(1)
        stop = 0
        if len(sentence)-i < h:
            p = len(sentence)-i
        else:
            if i + h == len(sentence):
                p = len(sentence) - i
            else:
                p = h
            # print(p)
        while stop != 1:
            if sentence[i:i+p] in dic:
                length[i] = p
                # print(length)
                stop = 1
            elif sentence[i] in symbol:
                length[i] = 1
                stop = 1
            elif not(sentence[i] in dic):
                length[i] = 1
                dic[sentence[i]] = dict()
                stop = 1
            p = p - 1
    # print(length)
    return length


def reverse_max(dic, new_sentence, length):
    global h
    pos = {}
    while new_sentence != "`"*len(new_sentence):
        index = len(length)-1 - length[::-1].index(max(length))
        one_len = length[index]
        pos[index] = new_sentence[index:index+length[index]]
        # new_sentence = new_sentence.replace(new_sentence[index:index+one_len],"-"*one_len)
        for s in range(0, one_len):
            new_sentence = new_sentence[0:index] + \
                "`"*one_len + new_sentence[index+one_len:]
        for h in range(0, one_len):
            length[index + h] = 0
        # if index != 0:
        if index > h:
            # print(index)
            for x in range(index-1, index-1 - h, -1):
                if length[x] > index-x:
                    length[x] = index - x
                # if length[x] > index-1-x:
                # 	length[x] = index-1-x
        else:
            # print(index)
            for x in range(index-1, -1, -1):
                # print(length[x],index-(x-1))
                if length[x] > index-x:
                    length[x] = index - x
        # print(new_sentence)
        # print(length)
    ans = ""
    x = 0
    # print(pos)
    ans_list = []
    while x != len(new_sentence):
        ans += pos[x] + " / "
        ans_list.append(pos[x])
        try:
            x += len(pos[x])
        except KeyError:
            print("boom")
            break
    print(ans[0:-3])
    return ans_list


def add_to_dict(ans_list, all_dic, dic, symbol):
    fpath = path.split(path.abspath(inspect.getfile(openfile)))[0]

    with open(path.join(fpath, "data", "dict_don't_add.txt"), "r", encoding="utf8", errors="ignore") as blf:
        bl = blf.readlines()

    with open(path.join(fpath, "data", "dict_add.txt"), "a+", encoding="utf8", errors="ignore") as da:
        f = ""
        new_list = []
        for a in ans_list:
            if len(a) > 1 or a in symbol:
                ef = f + "\n"
                if not(ef in da.readlines()) and not(ef in bl) and not(f in all_dic):
                    new_list.append(f)
                    da.write(ef)
                    print(f)
                f = ""
            else:
                f = f + a

    return new_list


def split(sentence, ch=True, ti=True, ha=True, add=True, add_dic=True):
    startime = time.time()
    all_dic, dic, symbol = openfile(ch, ti, ha, add)
    find_the_longest(dic)
    # sentence = "猴子喜歡吃香蕉"
    # sentence = "你的猴子喜歡吃香蕉"
    # sentence = "我們在野生動物園玩"
    # sentence = "徐希潔"
    # sentence = "我不信"
    # sentence = "屏東縣政府"
    # sentence = "我想聽派對動物"
    # sentence = "我們 在野生動物，園玩。"
    # sentence = "印尼的首都是雅加達"
    # sentence = "台北市長柯文哲、鴻海集團創辦人郭台銘、立委王金平三方結盟甚囂塵上，三方幕僚預計明天舉行會前會，「郭柯王」結盟浮出檯面。"
    # sentence = "本系為南台灣第一個純以資訊及計算機工程為重心的高級學術單位，於民國七十六年八月成立碩士班，八十一年八月成立博士班，於八十六年八月成立大學部，九十一年八月擴增大學部為兩班，並於九十五學年度再增設醫學資訊研究所，一百年八月製造資訊與系統研究所整合至本系，以一系三所之模式進行。"
    # sentence = input("請輸入文章:")
    length = get_len(dic, symbol, sentence)
    ans_list = reverse_max(dic, sentence, length)
    if add_to_dict:
        new = add_to_dict(ans_list, all_dic, dic, symbol)
    ttime = time.time()-startime
    print(ttime)
    return ans_list


if __name__ == "__main__":
    sentence = input("請輸入文章:")
    split(sentence)
