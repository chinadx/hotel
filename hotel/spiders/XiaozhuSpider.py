# -*- coding:utf-8 -*-
__author__ = 'Shaun'

import scrapy
import pymysql
import re


class ElongSpider(scrapy.Spider):
    name = "xiaozhu"
    start_urls = [
        'http://sh.xiaozhu.com/pudongxinqu-duanzufang-8/',
    ]
    allowed_domains = [
        'xiaozhu.com',
    ]
    HEADER = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'www.xiaozhu.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    def start_requests(self):
        return [scrapy.Request('http://www.xiaozhu.com/', headers=self.HEADER, callback=self.parse)]

    def parse(self, response):
        url = response.url
        print '--------------------', url

        regx = re.compile('^http://[a-z]*.xiaozhu.com/fangzi/[0-9]{1,12}.html$')
        if regx.match(url) is not None and url.find('landmark') == -1:
            try:
                conn = pymysql.connect(host='192.168.1.10', user='root',
                            passwd='rootroot', db='spider', charset='utf8')
                cur = conn.cursor()
                cur.execute("insert into xiaozhu_link(link) values(%s)", (url))
                cur.connection.commit()
            except Exception as e:
                print e
            finally:
                cur.close()
                conn.close()
        for link in response.xpath('//a/@href'):
            next_page = link.extract()

            if next_page is not None:
                next_page = response.urljoin(next_page)
                if next_page[0:4] == 'http':
                    #print '************', next_page
                    yield scrapy.Request(next_page, headers=self.HEADER, callback=self.parse)
        return

