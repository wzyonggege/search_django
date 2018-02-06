# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from twisted.enterprise import adbapi
from scrapy import log

import uuid


class SpiderPipeline(object):
    def __init__(self):
        self.MYSQL_HOST = '127.0.0.1'
        self.MYSQL_DBNAME = 'spider'
        self.MYSQL_USER = 'root'
        self.MYSQL_PASSWD = ''
        self.MYSQL_PORT = 3306
        self.TABLE = 'stackoverflow'
        self.dbpool = adbapi.ConnectionPool('pymysql',
                                            host=self.MYSQL_HOST,
                                            db=self.MYSQL_DBNAME,
                                            user=self.MYSQL_USER,
                                            passwd=self.MYSQL_PASSWD,
                                            port=self.MYSQL_PORT,
                                            charset='utf8',
                                            cursorclass=pymysql.cursors.DictCursor,
                                            use_unicode=True,)

    def process_item(self, item, spider):
        d = self.dbpool.runInteraction(self._conditional_insert, item, spider)
        log.msg('connect to mysql worked')
        d.addErrback(self._handle_error, item, spider) # 调用异常处理方法
        d.addBoth(lambda  _:item)
        return d

    def _conditional_insert(self, conn, item, spider):
        db_key = 'question,link,answers,votes,views,tags'
        db_value = "\"{}\", {}, {}, {}, {}, \"{}\"".format(*[item[k] for k in db_key.split(',')])
        sql = "insert INTO {} (_id, {}) VALUES (\"{}\", {})".format(
            self.TABLE, db_key, uuid.uuid3(uuid.NAMESPACE_DNS, item['link']), db_value
        )
        print(sql)
        conn.execute(sql)

    def _handle_error(self, failure, item, spider):
        print(failure)
