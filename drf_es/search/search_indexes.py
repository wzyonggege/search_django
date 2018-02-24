from elasticsearch_dsl import (
    DocType,
    Text,
    Integer,
    Completion,
)

class StackoverflowType(DocType):
    question = Text()
    tags = Text()
    link = Integer()
    views = Integer()
    answers = Integer()
    votes = Integer()

    class Meta:
        index = 'stackoverflow'
        doc_type = 'question'

StackoverflowType.init()