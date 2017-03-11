# -*- coding: utf-8 -*-
import os
from urllib import request, parse
import sys

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 \
          (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}


class HtmlSaver(object):
    def get_img(self, img_url):
        req = request.Request(url=img_url, headers=headers)
        response = request.urlopen(req)
        if response.getcode() != 200:  # 如果返回代码不是200，说明状态错误
            return None

        return response.read()

    def get_valid_dir(self, dir_name):
        """删除目录名中的非法字符，有 ( \ / : * ? " < > |  )"""
        for char in ('\\', '/', ':', '*', '?', '"', '<', '>', '|'):
            dir_name.replace(char, "")
        return dir_name

    def mkdir(self, class_name, title_name):
        if not class_name or not title_name:
            return

        class_name = self.get_valid_dir(class_name)
        title_name = self.get_valid_dir(class_name)

        base_path = r"E:\python\git_programs\crawler\beauty\download"  # 前面加r防止字符转义
        class_path = os.path.join(base_path, class_name)
        title_path = os.path.join(class_path, title_name)
        try:
            if not os.path.exists(class_path):
                os.makedirs(class_path)  # makedirs相比mkdir的好处是可以创建多级目录
            if not os.path.exists(title_path):
                os.makedirs(title_path)  # makedirs相比mkdir的好处是可以创建多级目录
            return title_path
        except:
            print('mkdir failed! class_path = %s, title_path = %s' % (class_path, title_path))
            print(sys.exc_info()[0:2])
            sys.exit()

    def save(self, class_name, title_name, url, img_urls):
        if img_urls[0] == 'Null_img':  # 图片为空
            return
        assert len(class_name) > 0 and len(title_name) > 0, \
            'save: check class_name[%s] and title_name[%s]' % (class_name, title_name)
        title_path = self.mkdir(class_name, title_name)
        for num, img_url in enumerate(img_urls):
            if num > 0:  # 一个页面有多张图片，图片名称编号如：1-1.jpg, 1-2.jpg
                img = self.get_img(img_url)
                if len(os.path.split(url)[-1]) > 3:  # 第一页的url没有123的后缀，把该页的图片名称设置为1.jpg
                    img_name = "1-%s.jpg" % str(num)
                else:
                    img_name = os.path.split(url)[-1] + '-%s.jpg' % str(num) # 图片名称
            else:
                img = self.get_img(img_url)
                if len(os.path.split(url)[-1]) > 3:  # 第一页的url没有123的后缀，把该页的图片名称设置为1.jpg
                    img_name = "1.jpg"
                else:
                    img_name = os.path.split(url)[-1] + '.jpg'  # 图片名称

            with open(os.path.join(title_path, img_name), 'wb') as f:   # 图片以二进制形式保存
                f.write(img)
