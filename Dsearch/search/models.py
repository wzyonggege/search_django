from django.db import models

from elasticsearch_dsl import DocType, Text, Integer, Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer

from elasticsearch_dsl.connections import connections


# analyzer
class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}

ik_analyzer = CustomAnalyzer("ik_max_word", filter=["lowercase"])
connections.create_connection(hosts=["http://127.0.0.1:9200/"])

class StackoverflowType(DocType):
    suggests = Completion(analyzer=ik_analyzer)
    question = Text(analyzer=ik_analyzer)
    tags = Text(analyzer=ik_analyzer)
    link = Integer()
    views = Integer()
    answers = Integer()
    votes = Integer()

    class Meta:
        index = 'stackoverflow'
        doc_type = 'question'

StackoverflowType.init()
