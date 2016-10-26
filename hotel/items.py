# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ElongItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    detail_url = scrapy.Field()


class ZhaopinItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    xingzhi = scrapy.Field()
    guimo = scrapy.Field()
    site = scrapy.Field()
    hangye = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()