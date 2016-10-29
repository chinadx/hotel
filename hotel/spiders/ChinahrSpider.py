# -*- coding:utf-8 -*-
__author__ = 'Shaun'

import scrapy
import pymysql
import re
from scrapy.loader import ItemLoader
from hotel.items import ChinahrItem


class ZhaopinSpider(scrapy.Spider):
    name = "chinahr"
    start_urls = [
        'http://www.chinahr.com/company/',
    ]
    allowed_domains = [
        'www.chinahr.com',
    ]

    custom_settings = {
        "DOWNLOAD_DELAY": 0
    }

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'www.chinahr.com',
        'Referer':'http://www.chinahr.com/beijing/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def parse(self, response):
        url = response.url
        regx = re.compile('^http://www.chinahr.com/company/.*?\.html$')

        if regx.match(url) is not None:
            id = url.rsplit('/')[-1].split('.')[0]
            baseinfo = response.xpath('//div[@class="mc-company"]')
            name = baseinfo.xpath('//h1/text()').extract()[0].strip()

            attrs = ''
            for attr in baseinfo.xpath('//div[@class="wrap-mc"]/em/text()'):
                attrs = attrs\
                      + attr.extract().strip()\
                      + '|'

            benefits = ''
            for bene in baseinfo.xpath('//div[@class="treat-company"]/ul/li/text()'):
                benefits = benefits \
                        + bene.extract().strip() \
                        + '|'

            contacts = ''
            for con in baseinfo.xpath('//div[@class="address"]/p/text()'):
                contacts = contacts\
                         + con.extract().strip()\
                         + '|'

            intro = response.xpath('//div[@class="art-company"]/div[1]/text()').extract()[0].strip()

            item = ChinahrItem()
            item['id'] = id
            item['name'] = name
            item['url'] = url
            item['benefits'] = benefits
            item['attributes'] = attrs
            item['intro'] = intro
            item['contact'] = contacts
            yield item

        for link in response.xpath('//a/@href'):
            next_page = link.extract()

            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, headers=self.headers, callback=self.parse)
