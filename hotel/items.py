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


class ElongHotelItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    city_code = scrapy.Field()
    city_pinyin = scrapy.Field()
    district = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    cbd = scrapy.Field()
    star = scrapy.Field()
    detail_url = scrapy.Field()
    pic_url = scrapy.Field()
    price = scrapy.Field()
    point = scrapy.Field()
    score = scrapy.Field()
    comment_count = scrapy.Field()
    create_time = scrapy.Field()


class ElongRoomItem(scrapy.Item):
    name = scrapy.Field()
    size = scrapy.Field()
    bed = scrapy.Field()
    price = scrapy.Field()

class ZhaopinItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    city = scrapy.Field()
    xingzhi = scrapy.Field()
    guimo = scrapy.Field()
    web = scrapy.Field()
    site = scrapy.Field()
    hangye = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()