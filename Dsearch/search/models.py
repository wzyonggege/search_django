from django.db import models

from elasticsearch_dsl import DocType, Keyword, Text, Integer, Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])

# analyzer
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])

class Stackoverflow(DocType):
    suggests = Completion(analyzer=ik_analyzer)
    question = Text(analyzer=ik_analyzer)
    tags = Text(analyzer=ik_analyzer)

    link = Keyword()
    views_nums = Integer()
    answers_nums = Integer()
    votes_nums = Integer()

    class Meta:
        index = 'stackoverflow'
        doc_type = 'question'

if __name__ == "__main__":
    Stackoverflow.init()      # 避免import时误执行初始化