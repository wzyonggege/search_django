from django.conf.urls import url

from . import views
from . import api

app_name = 'search'
urlpatterns = [
    url(r'list/$', api.StackoverflowView.as_view(), name='search_list'),
]