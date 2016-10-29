# -*- coding: utf-8 -*-
from scrapy import log
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from hotel.items import ZhaopinItem, ElongHotelItem, ElongRoomItem, ChinahrItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HotelPipeline(object):
    def process_item(self, item, spider):
        return item


# 记录item数据到mysql的管道
class MySQLPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        db = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        db_pool = adbapi.ConnectionPool('MySQLdb', **db)
        return cls(db_pool)

    # pipeline默认调用
    def process_item(self, item, spider):
        if isinstance(item, ZhaopinItem):
            d = self.db_pool.runInteraction(self._do_insert_company, item, spider)
            d.addErrback(self._handle_error, item, spider)
            d.addBoth(lambda _: item)
            return d
        if isinstance(item, ElongHotelItem):
            pass
        if isinstance(item, ElongRoomItem):
            pass
        if isinstance(item, ChinahrItem):
            d = self.db_pool.runInteraction(self._do_insert_chinahr_company, item, spider)
            d.addErrback(self._handle_error, item, spider)
            d.addBoth(lambda _: item)
            return d
        return item

    # 处理招聘公司名录
    def _do_insert_company(self, conn, item, spider):
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from zhaopin where id = %s
        """, (item['id'], ))
        ret = conn.fetchone()

        if ret:
            print 'compay id = [', item['id'], ']has already been stored.'
        else:
            conn.execute("""
                insert into zhaopin
                      (id,name,xingzhi,guimo,hangye,site,web,address)
                values(%s,%s,%s,%s,%s,%s,%s,%s)
                     """,(item['id'], item['name'], item['xingzhi'], item['guimo'], item['hangye'],
                              item['site'], item['web'], item['address'])
                        )

    # 处理中华英才网公司名录
    def _do_insert_chinahr_company(self, conn, item, spider):
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from chinahr_company where id = %s
        """, (item['id'],))
        ret = conn.fetchone()

        if ret:
            print 'compay id = [', item['id'], ']has already been stored.'
        else:
            conn.execute("""
                insert into chinahr_company
                      (id,name,url,attributes,benefits,contact,intro)
                values(%s,%s,%s,%s,%s,%s,%s)
                     """, (item['id'], item['name'], item['url'], item['attributes'], item['benefits'],
                           item['contact'], item['intro'])
                        )

    # 处理艺龙酒店信息
    def _do_insert_hotel(self, conn, item, spider):
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from hotel_elong where id = %s
        """, (item['id'], ))
        ret = conn.fetchone()

        if ret:
            print 'hotel id = [', item['id'], ']has already been stored.'
        else:
            conn.execute("""
                insert into zhaopin
                      (id,name,xingzhi,guimo,hangye,site,web,address)
                values(%s,%s,%s,%s,%s,%s,%s,%s)
                     """,(item['id'], item['name'], item['xingzhi'], item['guimo'], item['hangye'],
                              item['site'], item['web'], item['address'])
                        )
    # 异常处理
    def _handle_error(self, failure, item, spider):
        log.err(failure)
