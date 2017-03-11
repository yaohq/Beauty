# -*- coding: utf-8 -*-
import sys

from crawler.beauty.html_downloader import HtmlDownloader, RESPONSE_READ_FAILED
from crawler.beauty.html_parser import HtmlParser
from crawler.beauty.url_manager import UrlManager
from crawler.beauty.html_saver import HtmlSaver
from urllib.error import HTTPError


class BeautyMain(object):
    def __init__(self):
        self.urls = UrlManager()  # url 管理器
        self.downloader = HtmlDownloader()  # 下载器
        self.parser = HtmlParser()  # 解析器
        self.saver = HtmlSaver()  # 保存模块

    # 获取http://www.mzitu.com/all页面中的所有主题的链接
    def get_all_titles(self, root_url):
        self.urls.add_new_url(class_name="每日更新", title_name="all_titles", url=root_url)  # 增加root_url到mongodb的urls集合中
        content = self.downloader.download(root_url)
        self.urls.update_url_flag(root_url, 'Yes')  # 更新数据库中的url状态为Yes已爬取
        for class_name, title_name, url in self.parser.parse_root_url(content):  # 专门解析首页数据
            # print(class_name + ' : ' + title_name + ' : ' + url)
            self.urls.add_new_url(class_name, title_name, url)

    def crawler_bak(self):
        count = 0

        while self.urls.has_new_url():  # 如果有待抓取的页面
            new_url = self.urls.get_new_url()  # 获取一个待抓取的url
            count += 1
            print('crawling %d : %s' % (count, new_url))  # 实时打印抓取情况
            content = self.downloader.download_proxy(new_url)  # 获取网页内容
            class_name, title_name = self.parser.parse_path(content)  # 获取一组图片的分类和主题
            print(class_name + ":" + title_name)
            url = new_url  # 把第一页的url赋值给url
            # 把每个图片网页的url保存到数据库，class_name:all_titles
            self.urls.add_new_url("all_titles", title_name, url)
            self.urls.update_url_flag(url, "Success")  # 更新url是否读取成功
            while True:
                img_urls = self.parser.parse(content)  # 返回一个图片url列表，包含一个或多个图片url
                print(url)
                # 按照class_name, title_name 和 img的路径保存图片
                self.saver.save(class_name, title_name, url, img_urls)

                url = self.parser.parse_next(content)  # 获取下一页的url
                if url == 'Null_url':  # 如果返回的url为空，说明当前title已经下载完成，继续下一组title
                    break
                self.urls.add_new_url("all_titles", title_name, url)
                content = self.downloader.download_proxy(url)  # 获取下一页的内容
                if content == RESPONSE_READ_FAILED:  # 如果返回的网页内容为读取失败，本组无法继续，开始下一组
                    self.urls.update_url_flag(url, "Failed")  # 更新url读取状态为失败
                    break
                self.urls.update_url_flag(url, "Success")  # 更新url读取状态为成功(图片网页的url)
            self.urls.update_url_flag(new_url, 'Yes')  # 更新数据库中的该url状态为Yes已爬取(整组图片的开始url)

    def crawler(self):
        count = 0

        while self.urls.has_new_url():  # 如果有待抓取的页面
            new_url = self.urls.get_new_url()  # 获取一个待抓取的url
            count += 1
            print('crawling %d : %s' % (count, new_url))  # 实时打印抓取情况
            content = self.downloader.download_proxy(new_url)  # 获取网页内容
            class_name, title_name = self.parser.parse_path(content)  # 获取一组图片的分类和主题
            print(class_name + ":" + title_name)
            url = new_url  # 把第一页的url赋值给url
            # 把每个图片网页的url保存到数据库，class_name:all_titles
            self.urls.add_new_url("all_titles", title_name, url)
            self.urls.update_url_flag(url, "Success")  # 更新url是否读取成功
            while True:
                img_urls = self.parser.parse(content)  # 返回一个图片url列表，包含一个或多个图片url
                print(url)
                # 按照class_name, title_name 和 img的路径保存图片
                self.saver.save(class_name, title_name, url, img_urls)

                url = self.parser.parse_next(content)  # 获取下一页的url
                if url == 'Null_url':  # 如果返回的url为空，说明当前title已经下载完成，继续下一组title
                    break
                self.urls.add_new_url("all_titles", title_name, url)
                content = self.downloader.download_proxy(url)  # 获取下一页的内容
                if content == RESPONSE_READ_FAILED:  # 如果返回的网页内容为读取失败，本组无法继续，开始下一组
                    self.urls.update_url_flag(url, "Failed")  # 更新url读取状态为失败
                    break
                self.urls.update_url_flag(url, "Success")  # 更新url读取状态为成功(图片网页的url)
            self.urls.update_url_flag(new_url, 'Yes')  # 更新数据库中的该url状态为Yes已爬取(整组图片的开始url)

def main():
    root_url = "http://www.mzitu.com/all"
    beauty = BeautyMain()
    # beauty.get_all_titles(root_url)

    try:
        beauty.crawler()
    except HTTPError:  # 服务器返回错误，继续调用 crawler，死循环了...
        beauty.crawler()


if __name__ == '__main__':
    main()