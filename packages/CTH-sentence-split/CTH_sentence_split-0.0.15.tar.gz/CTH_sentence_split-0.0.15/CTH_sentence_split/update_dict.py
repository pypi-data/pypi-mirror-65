from os import path
import inspect

import pickle

import hashlib

import json

import requests

import time


def openfile():
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

    with open(path.join(fpath, "data", "dict_don't_add.txt"), "r", encoding="utf8", errors="ignore") as da:
        bl_dic = {}
        for line in da:
            # dic.append(line[0:-1]) #list
            bl_dic[line[0:-1]] = 0
            # print(line)

    return ch_dic, ti_dic, ha_dic, add_dic, bl_dic


def update_l_dics(n_dics):
    fpath = path.split(path.abspath(inspect.getfile(openfile)))[0]

    with open(path.join(fpath, "data", "ch_dict_no_space.pickle"), "wb") as f:
        pickle.dump(n_dics[0], f)

    with open(path.join(fpath, "data", "ti_dict.pickle"), "wb") as f:
        pickle.dump(n_dics[1], f)
        # print(dic)

    with open(path.join(fpath, "data", "ha_dict.pickle"), "wb") as f:
        pickle.dump(n_dics[2], f)
        # print(dic)

    with open(path.join(fpath, "data", "dict_add.txt"), "w", encoding="utf8", errors="ignore") as da:
        for word in list(n_dics[3].keys()).sort():
            da.write(word)

    with open(path.join(fpath, "data", "dict_don't_add.txt"), "w", encoding="utf8", errors="ignore") as blf:
        for word in list(n_dics[4].keys()).sort():
            blf.write(word)


def key_to_md5(ch_dic, ti_dic, ha_dic, add_dic, bl_dic):
    ch_md5_tran = hashlib.md5()
    ch_dic_key = str(sorted(list(ch_dic.keys())))
    ch_md5_tran.update(ch_dic_key.encode("utf-8"))
    ch_dic_md5 = ch_md5_tran.hexdigest()

    ti_md5_tran = hashlib.md5()
    ti_dic_key = str(sorted(list(ti_dic.keys())))
    ti_md5_tran.update(ti_dic_key.encode("utf-8"))
    ti_dic_md5 = ti_md5_tran.hexdigest()

    ha_md5_tran = hashlib.md5()
    ha_dic_key = str(sorted(list(ha_dic.keys())))
    ha_md5_tran.update(ha_dic_key.encode("utf-8"))
    ha_dic_md5 = ha_md5_tran.hexdigest()

    add_md5_tran = hashlib.md5()
    add_dic_key = str(sorted(list(add_dic.keys())))
    print(add_dic_key)
    add_md5_tran.update(add_dic_key.encode("utf-8"))
    add_dic_md5 = add_md5_tran.hexdigest()

    bl_md5_tran = hashlib.md5()
    bl_dic_key = str(sorted(list(bl_dic.keys())))
    print(bl_dic_key)
    bl_md5_tran.update(bl_dic_key.encode("utf-8"))
    bl_dic_md5 = bl_md5_tran.hexdigest()

    return ch_dic_md5, ti_dic_md5, ha_dic_md5, add_dic_md5, bl_dic_md5


def all_to_json(ch_dic_key_md5, ti_dic_key_md5, ha_dic_key_md5, add_dic_key_md5, bl_dic_key_md5):
    ad = {}
    ad["ch_dic_md5"] = ch_dic_key_md5
    ad["ti_dic_md5"] = ti_dic_key_md5
    ad["ha_dic_md5"] = ha_dic_key_md5
    ad["add_dic_md5"] = add_dic_key_md5
    ad["bl_dic_md5"] = bl_dic_key_md5

    aj = json.dumps(ad, ensure_ascii=False, indent=4)

    return aj


def check(aj):
    print("Checking")
    server_ip = "http://140.116.245.152:50003/check"

    # try:
    #     r = requests.post(server_ip, data={'data': aj})
    #     re = r.text
    #     if re == "True":
    #         if_new = True
    #         print("Have a new dict.")
    #     else:
    #         if_new = False
    #         print("Doesn't have a new dict.")
    #     print("Checked")
    #     return if_new
    # except:
    #     raise ConnectionError

    r = requests.post(server_ip, data={'data': aj})
    re = r.text
    if re == "True":
        if_new = True
        print("Have a new dict.")
    else:
        if_new = False
        print("Doesn't have a new dict.")
    print("Checked")
    return if_new


def update(l_dics):
    print("Updating")
    server_ip = "http://140.116.245.152:50003/update"

    # try:
    #     r = requests.post(server_ip, data={'data': str(l_dics)})
    #     n_dics = list(r.text)
    #     print(n_dics)
    #     print(type(n_dics))
    #     update_l_dics(n_dics)
    #     print("Updated")
    # except:
    #     raise ConnectionError
    r = requests.post(server_ip, data={'data': str(l_dics)})
    n_dics = list(r.text)
    print(n_dics)
    print(type(n_dics))
    update_l_dics(n_dics)
    print("Updated")


def run_update():
    ch_dic, ti_dic, ha_dic, add_dic, bl_dic = openfile()
    l_dics = []
    l_dics.append(ch_dic)
    l_dics.append(ti_dic)
    l_dics.append(ha_dic)
    l_dics.append(add_dic)
    l_dics.append(bl_dic)
    ch_dic_key_md5, ti_dic_key_md5, ha_dic_key_md5, add_dic_key_md5, bl_dic_key_md5 = key_to_md5(
        ch_dic, ti_dic, ha_dic, add_dic, bl_dic)
    print(ch_dic_key_md5, ti_dic_key_md5, ha_dic_key_md5,
          add_dic_key_md5, bl_dic_key_md5)
    aj = all_to_json(ch_dic_key_md5, ti_dic_key_md5,
                     ha_dic_key_md5, add_dic_key_md5, bl_dic_key_md5)
    # print(aj)
    if_new = check(aj)
    if if_new:
        update(l_dics)


if __name__ == "__main__":

    startime = time.time()
    run_update()

    ttime = time.time()-startime
    print(ttime)
