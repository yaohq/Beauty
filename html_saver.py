# -*- coding: utf-8 -*-
import os
from urllib import request, parse
import sys

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}


class HtmlSaver(object):
    def get_img(self, img_url):
        req = request.Request(url=img_url, headers=headers)
        response = request.urlopen(req)
        if response.getcode() != 200:  # 如果返回代码不是200，说明状态错误
            return None

        return response.read()

    def mkdir(self, class_name, title_name):
        if not class_name or not title_name:
            return

        base_path = r"E:\python\git_programs\crawler\beauty\download"
        class_path = os.path.join(base_path, class_name)
        title_path = os.path.join(class_path, title_name)
        try:
            if not os.path.exists(class_path):
                os.mkdir(class_path)
            if not os.path.exists(title_path):
                os.mkdir(title_path)

            return title_path
        except:
            print('mkdir failed! class_path = %s, title_path = %s' % (class_path, title_path))
            print(sys.exc_info()[0:2])
            sys.exit()

    def save(self, class_name, title_name, url, img_url):
        if img_url == 'Null_img':  # 图片为空
            return
        img = self.get_img(img_url)

        if len(os.path.split(url)[-1]) > 3:  # 第一张图片没有 /1 后缀
            img_name = "1.jpg"
        else:
            img_name = os.path.split(url)[-1] + '.jpg'  # 图片名称
        title_path = self.mkdir(class_name, title_name)

        with open(os.path.join(title_path, img_name), 'wb') as f:
            f.write(img)
