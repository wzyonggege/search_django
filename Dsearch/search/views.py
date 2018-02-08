import json
import redis
from datetime import datetime

from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from elasticsearch import Elasticsearch

from .models import StackoverflowType
redis_cli = redis.StrictRedis()
client = Elasticsearch(hosts=["127.0.0.1"])

def index(request):
    return render(request, 'index.html')


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get("s", "")
        re_datas = []
        if key_words:
            s = StackoverflowType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest",
                "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
            suggestions = s.execute_suggest()
            for match in suggestions.my_suggest[0].options:
                source = match._source
                re_datas.append(source["question"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    def get(self, request):
        key_words = request.GET.get("q", "")
        s_type = request.GET.get("s_type", "question")

        redis_cli.zincrby("search_keywords_set", key_words)

        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

        so_count = redis_cli.get("so_count")
        start_time = datetime.now()
        response = client.search(
            index="stackoverflow",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["tags", "question"]
                    }
                },
                "from": (page - 1) * 10,
                "size": 10,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "question": {},
                        "tags": {},
                    }
                }
            }
        )

        end_time = datetime.now()
        last_seconds = (end_time - start_time).total_seconds()
        total_nums = response["hits"]["total"]
        if (page % 10) > 0:
            page_nums = int(total_nums / 10) + 1
        else:
            page_nums = int(total_nums / 10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "question" in hit["highlight"]:
                hit_dict["question"] = "".join(hit["highlight"]["question"])
            else:
                hit_dict["question"] = hit["_source"]["question"]
            if "tags" in hit["highlight"]:
                hit_dict["content"] = "".join(hit["highlight"]["tags"])[:500]
            else:
                hit_dict["content"] = hit["highlight"]["tags"]


            hit_dict["answers"] = hit["_source"]["answers"]
            hit_dict["url"] = 'https://stackoverflow.com/questions/' + hit["_source"]["link"]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)

        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                               "so_count": so_count,
                                               "topn_search": topn_search})