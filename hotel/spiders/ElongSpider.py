# -*- coding:utf-8 -*-
__author__ = 'Shaun'

import scrapy
import pymysql
import re


class ElongSpider(scrapy.Spider):
    name = "elong"
    start_urls = [
        'http://hotel.elong.com/beijing/',
    ]
    allowed_domains = [
        'hotel.elong.com',
    ]

    def parse(self, response):
        url = response.url
        print '--------------------', url

        regx = re.compile('^http://hotel.elong.com/[a-z]*/*[0-9]{8}/$')
        if regx.match(url) is not None and url.find('landmark') == -1:
            try:
                conn = pymysql.connect(host='192.168.1.10', user='root',
                            passwd='rootroot', db='spider', charset='utf8')
                cur = conn.cursor()
                cur.execute("insert into elong_link(link) values(%s)", (url))
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
                    yield scrapy.Request(next_page, callback=self.parse)
        return

