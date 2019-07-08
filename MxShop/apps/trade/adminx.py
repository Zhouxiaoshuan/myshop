#!/usr/bin/env python
# -*- coding: utf-8 -*-



import xadmin
from .models import ShoppingCart, OrderInfo, OrderGoods, Aftersale


class ShoppingCartAdmin(object):
    list_display = ["user", "goods", "nums", ]


class OrderInfoAdmin(object):
    list_display = ["user", "order_sn", "pay_status", "order_mount", "address", "create_time"]

    class OrderGoodsInline(object):
        model = OrderGoods
        exclude = ['add_time', ]
        extra = 1
        style = 'tab'

    inlines = [OrderGoodsInline, ]

class AftersaleAdmin(object):
    list_display = ["user", "logistics", "number", "reason", "create_time"]


xadmin.site.register(ShoppingCart, ShoppingCartAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(Aftersale, AftersaleAdmin)


