# -*- coding: utf-8 -*-
from urllib import request

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}


class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        req = request.Request(url=url, headers=headers)
        response = request.urlopen(req)
        if response.getcode() != 200:  # 如果返回代码不是200，说明状态错误
            return None

        return response.read()



