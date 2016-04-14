# -*- coding: utf-8 -*-

import os
import requests
import time
import threading
from lxml import etree

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class NewsCollector:
    def __init__(self, namelist, start_time, end_time):
        self.keywords = []
        token_cnt = 0
        while token_cnt < len(namelist):
            self.keywords.append(unicode(namelist[token_cnt]))
            token_cnt += 1
        self.st = int(time.mktime(time.strptime(start_time, "%Y-%m-%d")))
        self.et = int(time.mktime(time.strptime(end_time, "%Y-%m-%d")))
        self.start_url = "http://news.baidu.com/ns?from=news&cl=2&bt=" + str(self.st) + \
                         "&et=" + str(self.et) + \
                         "&submit=%B0%D9%B6%C8%D2%BB%CF%C2&mt=0&lm=&s=2&tn=news&word="

    def get_keyword(self, index):
        return self.keywords[index]

    def size(self):
        return len(self.keywords)

    def get_start_url(self, index):
        return self.start_url + self.keywords[index]


def create_file(save_path, filename):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename + ".txt"
    open(path, "w+")


def string_list_save(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename + ".txt"
    with open(path, "a+") as fp:
        for s in slist:
            fp.write("%s\t\t%s\t\t%s\n" % (s[0].encode('utf8'), s[1].encode('utf8'), s[2].encode('utf8')))


def page_info(my_page):
    """Xpath"""
    dom = etree.HTML(my_page)
    origin_news_items = dom.xpath('//div[@class = "result"]/h3/a')
    news_urls = dom.xpath('//div[@class = "result"]/h3/a/@href')
    news_authors = dom.xpath('//p[@class = "c-author"]/text()')
    news_items = []
    for item in origin_news_items:
        news_items.append(item.xpath('string(.)'))
    assert (len(news_items) == len(news_urls) and len(news_urls) == len(news_authors))
    return zip(news_items, news_urls, news_authors)


def next_page(my_page):
    """Xpath"""
    dom = etree.HTML(my_page)
    dom_name = "http://news.baidu.com"
    next_page_url_sfx = dom.xpath('//p[@id = "page"]/a[@class = "n"]/@href')
    next_page_url_sfx = next_page_url_sfx + next_page_url_sfx
    next_page_url = dom_name + next_page_url_sfx[1]
    return next_page_url


def crawler(url, name):
    page_cnt = 0
    content_cnt = 0
    print "downloading ", url
    my_page = requests.get(url).content.decode("utf8")
    my_page_results = page_info(my_page)
    content_cnt += len(my_page_results)
    save_path = u"News Collection"
    filename = unicode(name)
    create_file(save_path, filename)
    string_list_save(save_path, filename, my_page_results)
    new_page = my_page
    while page_cnt < 30:
        page_cnt += 1
        new_page_url = next_page(new_page)
        print "downloading ", name,  new_page_url
        new_page = requests.get(new_page_url).content.decode("utf8")
        new_page_results = page_info(new_page)
        filename = unicode(name)
        string_list_save(save_path, filename, new_page_results)
        content_cnt += len(new_page_results)
    print "all " + str(content_cnt) + " news about " + name + " have been downloaded."


if __name__ == '__main__':

    my_collector = NewsCollector(["万科", "恒大", "保利"], '2013-01-01', '2013-04-01')

    threads = []
    for ind in range(my_collector.size()):
        threads.append(threading.Thread(target=crawler,
                                        args=(my_collector.get_start_url(ind), my_collector.get_keyword(ind))))
    for thr in threads:
        thr.setDaemon(True)
        thr.start()
    for thr in threads:
        thr.join()

    print "Done!\ntell YRZ if there's something wrong."
