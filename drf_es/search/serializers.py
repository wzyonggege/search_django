from .models import Stackoverflow
from .search_indexes import StackoverflowType

from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer


class ElasticSOFSerializer(ElasticModelSerializer):
    class Meta:
        model = Stackoverflow
        es_model = StackoverflowType
        fields = ('question', 'tags', 'votes', 'views', 'answers', 'link')