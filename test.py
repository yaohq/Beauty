# -*- coding: utf-8 -*-
import os

from pymongo import MongoClient
from urllib import parse

find_str = {"class_name": "all_classes", "craw_flag": "Yes", "title_name": "ROSI 139期 精选"}
find_str1 = {"class_name": "all_classes", "craw_flag": "Yes"}

connect = MongoClient()
db = connect['beauty']  # 连接一个数据库，如果没有会自动创建
collection = db['urls']  # 选择一个集合，如果没有会自动创建
# coll = collection.find({"craw_flag": "Yes", "title_name": {'$regex': '\d+'}})
# for i in coll:
#     print(i)

# print(collection.find_one_and_update(find_str1, {'$set':{"craw_flag": "No"}}))
for coll in collection.find(find_str1):
    print(coll)

url = r"http://www.mzitu.com/15781"
img_name = os.path.split(url)
print(len(os.path.split(url)))
print(img_name)
