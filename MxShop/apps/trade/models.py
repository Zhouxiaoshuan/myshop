# Create your models here.


from datetime import datetime

from django.db import models

from goods.models import Goods

from django.contrib.auth.models import User

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    nums = models.IntegerField(default=1, verbose_name="购买数量")
    totalPrice = models.FloatField(default=0.0, verbose_name="总价")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
    def __str__(self):
        return "%s(%d)".format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单
    """
    ORDER_STATUS = (
        ("TRADE_SUCCESS", "交易成功"),
        ("TRADE_CLOSED", "交易关闭"),
        ("WAIT_BUYER_PAY", "交易创建"),
        ("TRADE_FINISHED", "交易结束"),
        ("PAYING", "待支付",)
    )
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name="订单号")
    pay_status = models.CharField(choices=ORDER_STATUS, default="paying", max_length=30, verbose_name="订单状态")
    order_mount = models.FloatField(default=0.0, verbose_name="订单金额")
    create_time = models.DateTimeField(null=True, blank=True, verbose_name="创建时间")

    #用户信息
    address = models.CharField(max_length=100, default="", verbose_name="收货地址")
    signer_name = models.CharField(max_length=20, default="", verbose_name="签收人")
    signer_mobile = models.CharField(max_length=11, verbose_name="联系电话")



    class Meta:
        verbose_name = u"订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)



class OrderGoods(models.Model):
     """
     订单商品
     """
     order = models.ForeignKey(OrderInfo, verbose_name="订单信息", related_name="goods", on_delete=models.CASCADE)
     goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
     user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
     goods_num = models.IntegerField(default=0, verbose_name="商品数量")
     add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
     totalprice = models.IntegerField(default=0, verbose_name="小计")
     comment = models.CharField(default="undone", max_length=20, verbose_name="评论状态")
     class Meta:
         verbose_name = "订单详情"
         verbose_name_plural = verbose_name


     def __str__(self):
         return str(self.order.order_sn)




class FinishedOrder(models.Model):
    """
    历史订单
    """
    order = models.ForeignKey(OrderInfo, verbose_name="订单信息", on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, verbose_name="商品", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    totalprice = models.IntegerField(default=0, verbose_name="小计")

    class Meta:
        verbose_name = "历史订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods

class Aftersale(models.Model):
    """
    售后
    """
    user = models.ForeignKey(User, verbose_name="用户", on_delete=models.CASCADE)
    event = models.CharField(verbose_name="事务", max_length=10)
    logistics = models.CharField(verbose_name="物流公司", max_length=200)
    number = models.CharField(verbose_name="物流单号", max_length=20)
    reason = models.CharField(verbose_name="退换货原因", max_length=200)
    create_time = models.DateTimeField(verbose_name="发起时间", default=datetime.now)

    class Meta:
        verbose_name = "售后"
        verbose_name_plural = verbose_name
