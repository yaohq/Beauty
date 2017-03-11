# -*- coding: utf-8 -*-

from urllib import request
from urllib.error import HTTPError, URLError
import linecache
import time

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) \
           Chrome/22.0.1207.1 Safari/537.1"}
URL_OPEN_FAULSE = "URL_OPEN_FAULSE"  # url_open 错误返回状态
IP_LIST = "IP.list"
MAX_READ_TIMES = 10  # response.read() 最多重新读取10次
RESPONSE_READ_FAILED = "response.read failed"

class HtmlDownloader(object):
    def __init__(self):
        self.ip_ss = 0  # 本次ip代理使用数量
        self.max_ip_ss = len(linecache.getlines(IP_LIST))  # 获取ip代理列表行数
        self.max_read_times = MAX_READ_TIMES

    def download(self, url):
        if url is None:
            return None
        req = request.Request(url=url, headers=headers)
        response = request.urlopen(req)
        if response.getcode() != 200:  # 如果返回代码不是200，说明状态错误
            return None

        return response.read()

    def set_proxies(self, req):
        if self.ip_ss == 0:  # 第一次设置代理，说明服务器还没有开始报错，所以不用设置代理
            return

        ip_line = self.ip_ss % self.max_ip_ss
        ip = linecache.getline(IP_LIST, ip_line).strip().strip("\n")
        print("IP代理：第 %d 行：[ %s ]" % (ip_line, ip))
        req.set_proxy(str(ip).strip(), "http")

    def url_open(self, req=None, timeout=None):
        try:
            response = request.urlopen(req, timeout=timeout)
            if response.getcode() != 200:  # 如果返回代码不是200，说明状态错误
                response = URL_OPEN_FAULSE
        except (HTTPError, URLError):
            response = URL_OPEN_FAULSE
        except:
            response = URL_OPEN_FAULSE
        return response

    def response_read(self, response):
        if response:
            try:
                res = response.read()
            except:
                if self.max_read_times > MAX_READ_TIMES:  # 重试次数超过限制
                    res = RESPONSE_READ_FAILED  # 返回失败
                    return res
                self.max_read_times += 1
                time.sleep(60)  # 如果read() 超时，等待1分钟重新read
                self.response_read(response)  # 重新调用自己
        return res

    def download_proxy(self, url):
        if url is None:
            return None
        req = request.Request(url=url, headers = headers)
        while True:
            self.set_proxies(req)  # 设置代理
            response = self.url_open(req, 10)  # 设置超时时间为10s
            if response == URL_OPEN_FAULSE:  # 打开网页错误，换个代理继续
                self.ip_ss += 1
                print("continue")
                continue
            else:
                break
        self.max_read_times = 0  # 每个url读取结束，重置response.read() 的读取次数
        return self.response_read(response)
