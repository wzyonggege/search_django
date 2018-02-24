from django.conf.urls import url

from .views import StackoverflowView

urlpatterns = [
    url(r'^api/list$', StackoverflowView.as_view(), name='questions_list')
]