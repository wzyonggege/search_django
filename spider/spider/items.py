# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from drf_es.search.search_indexes import StackoverflowType
from elasticsearch_dsl.connections import connections

es = connections.create_connection(StackoverflowType._doc_type.using)


# 根据字符串生成搜索建议数组
def gen_suggests(es, index, info_tuple):
    used_words = set()
    suggests = []
    for text, weight in info_tuple:
        if text:
            # 调用es的analyze接口分析字符串
            words = es.indices.analyze(index=index, analyzer="ik_max_word", params={'filter': ["lowercase"]}, body=text)
            anylyzed_words = set([r["token"] for r in words["tokens"] if len(r["token"]) > 1])
            new_words = anylyzed_words - used_words
        else:
            new_words = set()
        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})

    return suggests


class StackoverflowItem(scrapy.Item):
    link = scrapy.Field()
    question = scrapy.Field()
    answers = scrapy.Field()
    views = scrapy.Field()
    votes = scrapy.Field()
    tags = scrapy.Field()

    def save_to_es(self):
        so = StackoverflowType()
        so.question = self["question"]
        so.answers = self["answers"]
        so.votes = self["votes"]
        so.views = self["views"]
        so.link = self["link"]
        so.tags = self["tags"]
        so.suggests = gen_suggests(es, StackoverflowType._doc_type.index, ((so.question, 10), (so.tags, 7)))
        so.save()
        return


