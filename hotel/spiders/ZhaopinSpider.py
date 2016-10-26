# -*- coding:utf-8 -*-
__author__ = 'Shaun'

import scrapy
import pymysql
import re
from scrapy.loader import ItemLoader
from hotel.items import ZhaopinItem


class ZhaopinSpider(scrapy.Spider):
    name = "zhaopin"
    start_urls = [
        'http://company.zhaopin.com/',
    ]
    allowed_domains = [
        'company.zhaopin.com',
    ]

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'company.zhaopin.com',
        'Referer':'http://company.zhaopin.com/beijing/1605001/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def parse(self, response):
        url = response.url
        regx = re.compile('^http://company.zhaopin.com/.*?CC[0-9]{8,12}\.htm$')

        if regx.match(url) is not None:
            print '-------------------hahahaha', url
            name = response.xpath('//div/h1/text()').extract()[0].encode('utf-8').strip()
            id = url.rsplit('/')[-1].split('.')[0]
            site = url
            # city = scrapy.Field()
            # xingzhi = response.xpath('//table[@class="comTinyDes"]/tr[1]/td[2]/span/text()').extract()[0].encode('utf-8').strip()
            # guimo = response.xpath('//table[@class="comTinyDes"]/tr[2]/td[2]/span/text()').extract()[0].encode('utf-8').strip()
            # site = url
            # hangye = response.xpath('//table[@class="comTinyDes"]/tr[4]/td[2]/span/text()').extract()[0].encode('utf-8').strip()
            # address = response.xpath('//table[@class="comTinyDes"]/tr[5]/td[2]/span/text()').extract()[0].encode('utf-8').strip()
            # latitude = scrapy.Field()
            # longitude = scrapy.Field()
            for tr in response.xpath('//table[@class="comTinyDes"]/tr'):
                try:
                    type = tr.xpath('./td[1]/span/text()').extract()[0].encode('utf-8').strip()
                    if type == '公司网站：':
                        continue
                    value = tr.xpath('./td[2]/span/text()').extract()[0].encode('utf-8').strip()
                    if type == '公司性质：':
                        xingzhi = value
                    if type == '公司规模：':
                        guimo = value
                    if type == '公司行业：':
                        hangye = value
                    if type == '公司地址：':
                        address = value
                except Exception as e:
                    None

            conn = pymysql.connect(host='192.168.1.7', user='root',
                        passwd='rootroot', db='spider', charset='utf8')
            cur = conn.cursor()
            cur.execute("insert into zhaopin(id,name,xingzhi,guimo,hangye,site,address) values(%s,%s,%s,%s,%s,%s,%s)",
                        (id, name, xingzhi,guimo,hangye,site,address ))
            cur.connection.commit()

        for link in response.xpath('//a/@href'):
            next_page = link.extract()

            if next_page is not None:
                next_page = response.urljoin(next_page)
                if next_page[0:14] == 'http://company':
                    yield scrapy.Request(next_page, headers=self.headers, callback=self.parse)
        return

    def get_company(self, response):
        company = ItemLoader(item=ZhaopinItem(), response=response)
        company._add_value("id", response.url.rsplit('/')[-1].split('.')[0])
        company.add_xpath("name", "//h1")
        print '++++++++++++', company.name
        yield company
