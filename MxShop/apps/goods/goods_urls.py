
from django.conf.urls import url
from . import views

app_name = 'goods'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.detail, name='details'),
    url(r'^goodsList/(?P<pk>[0-9]+)/$', views.goodsList, name='goodsList'),

]