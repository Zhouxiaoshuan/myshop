
from django.conf.urls import url
from . import views

app_name = 'trade'

urlpatterns = [
    # url('^addToCart/(?P<id>[0-9]+)/(?P<pk>[0-9]+)/$', views.addToCart, name='addToCart'),
    url('^shoppingCart/(?P<pk>[0-9]+)/$', views.shoppingCart, name='shoppingCart'),
    url('^order/(?P<id>[0-9]+)/$', views.order, name='order'),
    url('^delete/$', views.delete, name='delete'),
    url('^addToCart/$', views.addToCart, name='addToCart'),
    url('^updateCart/$', views.updateCart, name='updateCart'),
    url('^order_addToCart/$', views.order_addToCart, name='order_addToCart'),
    url('^order_getNow/$', views.order_getNow, name='order_getNow'),
    url('^submitOrder/$', views.submitOrder, name='submitOrder'),
    url('^pay_result/$', views.pay_result, name='pay_result'),
    url('^aftersale/$', views.aftersale, name='aftersale'),
]


