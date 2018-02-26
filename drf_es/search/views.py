from django.shortcuts import render

from elasticsearch import Elasticsearch, RequestsHttpConnection

from rest_framework_elasticsearch import es_views, es_pagination, es_filters
from .search_indexes import StackoverflowType

class StackoverflowView(es_views.ListElasticAPIView):
    es_client = Elasticsearch(hosts=["localhost:9200/"],
                              connection_class=RequestsHttpConnection)
    # pagination
    es_pagination_class = es_pagination.ElasticLimitOffsetPagination

    es_model = StackoverflowType
    es_filter_backends = (
        es_filters.ElasticFieldsFilter,
        es_filters.ElasticSearchFilter,
    )
    es_filters_fields = (
        es_filters.ESFieldFilter('tag', 'tags')
    )
    es_search_fields = (
        'question',
        'tags'
    )

def index(request):
    return render(request, 'index.html')