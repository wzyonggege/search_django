# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import SpiderItem

import re
import time


class StackoverflowSpider(scrapy.Spider):
    name = 'stackoverflow'
    base_url = 'https://stackoverflow.com/questions?page={}&sort=votes'
    headers = {
        'User-Agent': 'user-agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36',
    }

    def start_requests(self):
        for i in range(101, 1000001):
            yield scrapy.Request(url=self.base_url.format(i), headers=self.headers)
            if not i % 100:
                time.sleep(30)
        # return [scrapy.Request(url=self.base_url.format(i), headers=self.headers) for i in range(342, 100001)]

    def parse(self, response):
        for sel in response.xpath('//div[@class="question-summary"]'):
            item = SpiderItem()
            item['link'] = sel.xpath('div[@class="summary"]/h3/a/@href').extract()[0].split('/')[2]
            item['question'] = sel.xpath('div[@class="summary"]/h3/a/text()').extract()[0]
            item['votes'] = sel.xpath('div[1]//div[@class="vote"]//span/strong/text()').extract()[0]
            item['answers'] = sel.xpath('div[1]/div[@class="stats"]/div[2]/strong/text()').extract()[0]
            item['views'] = sel.xpath('div[1]/div[3]/@title').extract()[0].replace(',', '')
            item['views'] = item['views'].replace('views', '').strip()
            item['tags'] = ' '.join(sel.xpath('div[@class="summary"]/div[2]/a/text()').extract())
            yield item

