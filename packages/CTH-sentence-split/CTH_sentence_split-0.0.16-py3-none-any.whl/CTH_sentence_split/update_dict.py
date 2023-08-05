from os import path
import inspect

import pickle

import hashlib

import json

import requests

import time


def openfile():
    c_dics = []
    fpath = path.split(path.abspath(inspect.getfile(openfile)))[0]

    with open(path.join(fpath, "data", "ch_dict_no_space.pickle"), "rb") as f:
        c_dics.append(pickle.load(f))

    with open(path.join(fpath, "data", "ti_dict.pickle"), "rb") as f:
        c_dics.append(pickle.load(f))

    with open(path.join(fpath, "data", "ha_dict.pickle"), "rb") as f:
        c_dics.append(pickle.load(f))

    with open(path.join(fpath, "data", "dict_add.txt"), "r", encoding="utf8", errors="ignore") as da:
        add_dic = {}
        for line in da:
            # dic.append(line[0:-1]) #list
            add_dic[line[0:-1]] = 0
            # print(line)
        c_dics.append(add_dic)

    with open(path.join(fpath, "data", "dict_don't_add.txt"), "r", encoding="utf8", errors="ignore") as da:
        bl_dic = {}
        for line in da:
            # dic.append(line[0:-1]) #list
            bl_dic[line[0:-1]] = 0
            # print(line)
        c_dics.append(bl_dic)

    return c_dics


def write_n_dics(n_dics):
    fpath = path.split(path.abspath(inspect.getfile(openfile)))[0]

    with open(path.join(fpath, "data", "ch_dict_no_space.pickle"), "wb") as f:
        pickle.dump(n_dics[0], f)

    with open(path.join(fpath, "data", "ti_dict.pickle"), "wb") as f:
        pickle.dump(n_dics[1], f)

    with open(path.join(fpath, "data", "ha_dict.pickle"), "wb") as f:
        pickle.dump(n_dics[2], f)

    with open(path.join(fpath, "data", "dict_add.txt"), "w", encoding="utf8", errors="ignore") as da:
        for word in sorted(list(n_dics[3].keys())):
            da.write(word)

    with open(path.join(fpath, "data", "dict_don't_add.txt"), "w", encoding="utf8", errors="ignore") as blf:
        for word in sorted(list(n_dics[3].keys())):
            blf.write(word)


def dict_to_md5(c_dics):
    c_dics_md5 = []
    ch_md5_tran = hashlib.md5()
    ch_dic_key = str(sorted(list(c_dics[0].keys())))
    ch_md5_tran.update(ch_dic_key.encode("utf-8"))
    c_dics_md5.append(ch_md5_tran.hexdigest())

    ti_md5_tran = hashlib.md5()
    ti_dic_key = str(sorted(list(c_dics[1].keys())))
    ti_md5_tran.update(ti_dic_key.encode("utf-8"))
    c_dics_md5.append(ti_md5_tran.hexdigest())

    ha_md5_tran = hashlib.md5()
    ha_dic_key = str(sorted(list(c_dics[2].keys())))
    ha_md5_tran.update(ha_dic_key.encode("utf-8"))
    c_dics_md5.append(ha_md5_tran.hexdigest())

    add_md5_tran = hashlib.md5()
    add_dic_key = str(sorted(list(c_dics[3].keys())))
    add_md5_tran.update(add_dic_key.encode("utf-8"))
    c_dics_md5.append(add_md5_tran.hexdigest())

    bl_md5_tran = hashlib.md5()
    bl_dic_key = str(sorted(list(c_dics[4].keys())))
    bl_md5_tran.update(bl_dic_key.encode("utf-8"))
    c_dics_md5.append(bl_md5_tran.hexdigest())

    return c_dics_md5


def check_to_server(c_dics_md5):
    print("Checking")
    server_ip = "http://140.116.245.152:50003/check"
    jd = {}
    jd["c_dics_md5"] = c_dics_md5
    js = json.dumps(jd, ensure_ascii=False, indent=4)
    r = requests.post(server_ip, data={'data': js})
    re = r.text
    if_news = json.loads(re)["if_news"]
    return if_news


def update_dics(if_news, c_dics):
    print("Updating")
    server_ip = "http://140.116.245.152:50003/update"
    n_dics = c_dics
    need_dic = [3]
    for index in range(0, len(if_news)):
        if if_news[index]:
            if index in need_dic:
                jd = {}
                jd["index"] = index
                jd["dic"] = c_dics[index]

            else:
                jd = {}
                jd["index"] = index
                jd["dic"] = {}
            js = json.dumps(jd, ensure_ascii=False, indent=4)
            r = requests.post(server_ip, data={'data': js})
            re = r.text
            rd = json.loads(re)
            n_dics[index] = rd["n_dic"]
    return n_dics


def run_update():
    c_dics = openfile()
    c_dics_md5 = dict_to_md5(c_dics)
    if_news = check_to_server(c_dics_md5)
    n_dics = update_dics(if_news, c_dics)
    write_n_dics(n_dics)


if __name__ == "__main__":

    startime = time.time()
    run_update()

    ttime = time.time()-startime
    print(ttime)
