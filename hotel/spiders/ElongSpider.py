# -*- coding:utf-8 -*-
__author__ = 'Shaun'

import scrapy
import time
import datetime
import json
from hotel.items import ElongHotelItem, ElongRoomItem


class ElongSpider(scrapy.Spider):
    name = "elong"
    allowed_domains = [
        'm.elong.com',
    ]

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'m.elong.com',
        'Cookie': 'H5CookieId=3d0e0644-02f8-456e-9c19-160b50175220; H5SessionId=404D272F81A5E8D0E662219BE4B6AE44; H5Channel=norefer-seo%2CSEO; indate=2016-10-29; outdate=2016-10-30; cityid=0101; route=0f07db7686b6b4eaf290911b85d8581f; CookieGuid=0e938606-241f-4242-8a50-096e8d9f6523; SessionGuid=f68feeb8-cc47-4c5e-bb01-c01088b2b2f7; Esid=8e1abcb5-c3c6-4cfd-9fc5-e0a78118719a; CitySearchHistory=0101%23%E5%8C%97%E4%BA%AC%E5%B8%82%23Beijing%23; com.eLong.CommonService.OrderFromCookieInfo=Status=1&Orderfromtype=2&Isusefparam=0&Pkid=0&Parentid=1000001&Coefficient=0.0&Makecomefrom=0&Cookiesdays=0&Savecookies=0&Priority=9000; ShHotel=CityID=0101&CityNameCN=%E5%8C%97%E4%BA%AC%E5%B8%82&CityName=%E5%8C%97%E4%BA%AC%E5%B8%82&OutDate=2016-10-31&CityNameEN=Beijing&InDate=2016-10-30; s_cc=true; s_visit=1; s_sq=%5B%5BB%5D%5D; _jzqco=%7C%7C%7C%7C%7C1.416803720.1477709610648.1477709613984.1477709620813.1477709613984.1477709620813.0.0.0.3.3; SHBrowseHotel=cn=91348508%2C%2C%2C%2C%2C%2C%3B; _pk_id.2624.9f06=d5a72b29382d08c4.1477709611.1.1477709621.1477709611.; _pk_ses.2624.9f06=*',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36',
    }

    interface_url = ''
    page_idx = 1

    # 定义城市列表
    cities = {
        'bj': '北京|Beijing|0101',
        'hz': '杭州|Hangzhou|1201',
        'sh': '上海|Shanghai|0201',
        'nj': '南京|Nanjing|1101',
        'tj': '天津|Tianjin|0301',
        'wh': '武汉|Wuhan|1801',
        'cd': '成都|Chengdu|2301',
        'cq': '重庆|Chongqing|0401',
        'xa': '西安|Xian|2701',
        'gz': '广州|Guangzhou|2001',
        'sz': '深圳|Shenzhen|2003',
        'cs': '长沙|Changsha|1901',
        'qd': '青岛|Qingdao|1601',
        'su': '苏州|Soochow|1102',
        'zz': '郑州|Zhengzhou|1701',
    }

    # 用以获取接口所需的城市参数
    city_attr = []
    city_name = ''
    city_code = ''
    city_code_en = ''

    # 入住时间和离店时间
    in_date = ''
    out_date = ''

    # 接收城市代码作为参数。调用示例
    # scrapy crawl elong -a city=bj
    def __init__(self, city=None, *args, **kwargs):
        super(ElongSpider, self).__init__(*args, **kwargs)
        self.city_attr = self.cities.get(city).split("|")
        self.city_name = self.city_attr[0]
        self.city_name_en = self.city_attr[1]
        self.city_code = self.city_attr[2]

        # 使用时间：明天入住，后天离店
        today = datetime.date.today()
        # in_date = '2016-09-10'
        # out_date = '2016-09-11'
        self.in_date = today + datetime.timedelta(days=1)
        self.out_date = today + datetime.timedelta(days=2)

    # 构造接口url
    def build_url(self, page):
        timestamps = datetime.datetime.now().microsecond
        self.interface_url = "http://m.elong.com/hotel/api/list/?_rt=" \
              + str(int(time.time())) + str(timestamps) \
              + "&indate=" + str(self.in_date) \
              + "&outdate=" + str(self.out_date) \
              + "&pageindex=" + str(page) \
              + "&placename=&city=" + self.city_code + "#19"

    def start_requests(self):
        self.build_url(self.page_idx)
        yield scrapy.Request(self.interface_url, callback=self.parse_hotel_list)

    # 解析酒店接口返回json列表
    def parse_hotel_list(self, response):
        m = json.loads(response.body, encoding='utf-8')
        page_ret = json.dumps(m, ensure_ascii=False)
        doc = json.loads(page_ret, encoding='utf-8')
        hotel_list = doc.get("hotelList")
        if(len(hotel_list) == 0):
            return
        for hotel in hotel_list:
            hotel_item = ElongHotelItem()
            hotel_item['name'] = hotel.get("hotelName")
            hotel_item['pic_url'] = hotel.get("picUrl")
            hotel_item['point'] = hotel.get("commentPoint")
            hotel_item['score'] = hotel.get("commentScore")
            hotel_item['star'] = hotel.get("starLevel")
            facilityList = hotel.get("facilityList")
            facilities = len(facilityList)
            hotel_item['cbd'] = hotel.get("businessAreaName")
            hotel_item['price'] = hotel.get("lowestPrice")
            detailPageUrl = hotel.get("detailPageUrl")
            hotel_item['detail_url'] = detailPageUrl
            #详细地址是这种格式的http://m.elong.com/hotel/90893715/#indate=2016-09-13&outdate=2016-09-14
            #从中截取出酒店编码
            hotel_item['id'] = detailPageUrl[detailPageUrl.index("/hotel/")+7:detailPageUrl.index("/#")]
            hotel_item['district'] = hotel.get("districtName")
            hotel_item['comment_count'] = hotel.get("totalCommentCount")
            hotel_item['latitude'] = hotel.get("baiduLatitude")
            hotel_item['longitude'] = hotel.get("baiduLongitude")

            yield hotel_item
            yield scrapy.Request(hotel_item['detail_url'], headers=self.headers, callback=self.parse_hotel_detail)

        self.page_idx += 1
        self.build_url(self.page_idx)

        yield scrapy.Request(self.interface_url, callback=self.parse_hotel_list)


    # 解析酒店详情页，获取价格信息
    def parse_hotel_detail(self, response):
        description = response.xpath('//meta[@name="description"]/@content').extract()[0].encode('utf-8').strip()
        phone = response.xpath('//div[@class="facilities"]/dl/dd/a[@class="tel"]/text()').extract()[0].encode('utf-8').strip()
        address = response.xpath('//div[@class="posi"]/div[@class="addr"]/text()').extract()[0].encode('utf-8').strip()
        # 获取房型信息
        # names = response.xpath('//div[@class="type"]/ul/li[contains(@class, "rooms")]//div[@class="room"]/text()')
        # sizes = response.xpath('//div[@class="type"]/ul/li[contains(@class, "rooms")]//div[@class="room-info"]/span[1]/text()')
        # beds = response.xpath('//div[@class="type"]/ul/li[contains(@class, "rooms")]//div[@class="room-info"]/span[2]/text()')
        # prices = response.find('//div[@class="type"]/ul/li[contains(@class, "rooms")]//div[@class="price"]/span[@class="num"]/text()')
        # rooms = response.xpath('//div[@class="type"]/ul/li[contains(@class, "rooms")]')
        # i = 0
        # for room in rooms:
        #     room_item = ElongRoomItem()
        #     room_item['name'] = room.xpath('//div[@class="room"]/text()').extract()[i].strip()
        #     room_item['size'] = room.xpath('//div[@class="room-info"]/span[1]/text()').extract()[i].strip()
        #     room_item['bed'] = room.xpath('//div[@class="room-info"]/span[2]/text()').extract()[i].strip()
        #     room_item['price'] = room.xpath('//div[@class="price"]/span[@class="num"]/text()').extract()[i].strip()
        #     # 获取房态
        #     if rooms.xpath('../li[contains(@class, "no")]'):
        #         print 'full'
        #     yield room_item
        #     i += 1
        rooms = response.xpath('//*[@id="uniq22"]/div[2]/section[1]/div[3]/ul/li')
        i = 0
        for room in rooms:
            name = room.xpath('/div[1]/div[1]/div[2]/div[1]').extract()[i].strip()
            size = room.xpath('/div[1]/div[1]/div[2]/div[2]/span[1]').extract()[i].strip()
            bed = room.xpath('/div[1]/div[1]/div[2]/div[2]/span[2]').extract()[i].strip()
            price = room.xpath('/div[1]/div[2]/div/span[2]').extract()[i].strip()
            print name,size,bed,price

