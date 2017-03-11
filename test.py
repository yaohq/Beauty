# -*- coding: utf-8 -*-
import os

import re
from pymongo import MongoClient
from urllib import parse
from bs4 import BeautifulSoup
from urllib import request
import linecache
import string

def test1():
    find_str = {"class_name": "all_classes", "craw_flag": "Yes", "title_name": "ROSI 139期 精选"}
    find_str1 = {"class_name": "all_classes", "craw_flag": "No"}

    connect = MongoClient()
    db = connect['beauty']  # 连接一个数据库，如果没有会自动创建
    collection = db['urls']  # 选择一个集合，如果没有会自动创建
    # coll = collection.find({"craw_flag": "Yes", "title_name": {'$regex': '\d+'}})
    coll = collection.find({"craw_flag": "Failed"})
    for i in coll:
        print(i)

    # print(collection.find_one_and_update(find_str1, {'$set':{"craw_flag": "No"}}))
    # for coll in collection.find(find_str1):
    #     print(coll)
    #
    # url = r"http://www.mzitu.com/15781"
    # img_name = os.path.split(url)
    # print(len(os.path.split(url)))
    # print(img_name)

def test2():
    url = "http://www.mzitu.com/9267"
    req = request.urlopen(url)
    content = req.read()
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    img_obj = soup.find('div', class_="main-image").find_all('img')  # 查找图片
    for num, img in enumerate(img_obj):
        print(str(num) + " : " + img['src'])


def test3():
    with open("IP.list", 'r') as f:
        # for line in f.readlines():
        #     print(line)
        print(repr(f.readline().strip("\n")))

    print(linecache.getline("IP.list", 10))
    print(len(open("IP.list", "r").readlines()))
    print(len(linecache.getlines("IP.list")))
    print(10 % 100)


def  test4():
    print(string.printable)
    print(string.punctuation)
    print(string)
    print(request.getproxies_environment())


def test5():
    def one(*x):
        """输出传入的第一个参数"""
        """*号会将x转化为一个tupple"""
        print(x[0])
        print(x)
        print(type(x))

    lst = ["a", "b", "c", "d"]

    stri = "http://www.pythontab.com"
    print(re.sub('[^0-9a-zA-Z-.,;_ ]', '_', stri))

    print("_".join(str for str in stri.split("/")))
    for str in stri.split("/"):
        print(str)

class Test6(object):
    __private_var = "yaohq"
    _public_var = "yaohq"
    bbb = "aaa"
    def yaohq(self):
        pass


if __name__ == '__main__':
    aaa = Test6()
    print(aaa.__dir__())

