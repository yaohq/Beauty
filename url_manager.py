# -*- coding: utf-8 -*-
import sys
from pymongo import MongoClient


"""测试查找模式"""
find_str = {"class_name": "all_classes", "craw_flag": "No"}


class UrlManager(object):
    def __init__(self):
        """创建mongodb的连接，然后才能操作mongodb"""
        self.connect = MongoClient()
        self.db = self.connect['beauty']  # 连接一个数据库，如果没有会自动创建
        self.collection = self.db['urls']  # 选择一个集合，如果没有会自动创建
        # self.collection.delete_many({})  # 清空urls集合中的所有数据，如果urls集合不存在也不会报错

    def __del__(self):
        self.connect.close()  # 关闭数据库连接

    """传入类名，主题名和url"""
    def add_new_url(self, class_name='', title_name='', url=''):
        # print("class_name = %s, title_name = %s, url = %s" % (class_name, title_name, url))
        if not class_name or len(class_name) == 0:
            print('insert failed, class_name is Null, url = %s' % url)
            return

        if not title_name or len(title_name) == 0:
            print('insert failed, title_name is Null, url = %s' % url)
            return

        if not url or len(url) == 0:
            print('insert failed, url is Null, url = %s' % url)
            return

        if self.collection.count({"url": str(url)}) > 0:  # url已存在
            # print("url already exists, please check!")
            return

        data = {"class_name": str(class_name), "title_name": str(title_name), "url": str(url), "craw_flag": "No"}
        try:
            self.collection.insert(data)
        except:
            print('insert url failed')
            print(sys.exc_info()[0:2])
            sys.exit()

    def has_new_url(self):
        return self.collection.count(find_str)  # 只要all_classes类型的url

    def get_new_url(self):
        try:
            url = self.collection.find_one(find_str)['url']  # test
        except TypeError:
            print('crawl finished...')
            url = ""
        finally:
            return url

    """更新flag为Yes"""
    def update_url_flag(self, url, flag):
        if not url or len(url) == 0:
            return

        assert flag == 'Yes' or flag == 'No', 'flag must be "Yes" or "No"'

        try:
            self.collection.update_one({"url": str(url)}, {'$set': {"craw_flag": str(flag)}})
        except:
            print('update_url_flag failed! url = %s' % url)
            print(sys.exc_info()[0:2])
            sys.exit()
