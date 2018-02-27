from django.conf.urls import url

from . import views
from . import api

app_name = 'search'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^result$', views.result, name='result'),
    url(r'^search/$', views.search, name='search'),
    url(r'^suggest/$', views.suggest, name='suggest'),

    # api
    url(r'^api/list/$', api.StackoverflowView.as_view(), name='search_list'),
]