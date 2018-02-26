from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/list$', views.StackoverflowView.as_view(), name='questions_list'),
    url(r'^$', views.index, name='index')
]