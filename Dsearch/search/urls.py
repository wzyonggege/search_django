from django.conf.urls import url

from . import views

app_name = 'search'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^suggest/$', views.SearchSuggest.as_view(), name='suggest'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
]