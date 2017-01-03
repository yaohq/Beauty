# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

class HtmlParser(object):
    def parse_root_url(self, content):
        """专门解析首页数据：http://www.mzitu.com/all"""
        """:return a set([class_name, title_name, url])"""
        return_obj = set()

        if not content or len(content) == 0:
            return

        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        class_name = "all_classes"
        urls = soup.find_all('a', href = re.compile(r'http://www.mzitu.com/\d+'))
        for url in urls:
            return_obj.add((class_name, url.get_text(), url['href']))

        return return_obj

    def parse(self, content):
        """返回每一组title中的一张图片和下一页的url，如果没有下一页就返回空的"""

        if not content or len(content) == 0:
            return
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')

        try:
            img_obj = soup.find('div', class_="main-image").find('img')['src']  # 查找图片
        except TypeError:  # 如果图片为空
            img_obj = 'Null_img'

        return img_obj

    def parse_path(self, content):
        if not content or len(content) == 0:
            return
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        # 查找图片分类：如台湾妹子
        class_name = soup.find('li', class_="current-menu-parent").find('a')
        # 查找title
        title_name = soup.find('h2', class_="main-title")
        return class_name.get_text(), title_name.get_text()

    def parse_next(self, content):
        """返回下一页的url，如果没有下一页就返回  Null_url """
        if not content or len(content) == 0:
            return
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
        try:
            url = soup.find('a', text="下一页»")['href']  # 找到url
        except TypeError:  # 如果url为空
            url = 'Null_url'

        return url





