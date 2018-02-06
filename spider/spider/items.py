# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import pymysql


class SpiderItem(scrapy.Item):
    links = scrapy.Field()
    question = scrapy.Field()
    answers = scrapy.Field()
    views = scrapy.Field()
    votes = scrapy.Field()
    tags = scrapy.Field()

    def get_insert_sql(self):
        insert_sql =

