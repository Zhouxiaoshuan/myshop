


from django.shortcuts import render, redirect, get_object_or_404

from goods.models import Goods, GoodsCategory
from trade.models import ShoppingCart, OrderInfo, OrderGoods
from django.http import HttpResponseRedirect, JsonResponse
from user_operation.models import UserAddress
from datetime import datetime
from django.db.models import Q
from MxShop.settings import BASE_DIR
from alipay import AliPay
from django.contrib import messages
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from trade.models import OrderInfo
# Create your views here.

# 添加购物车
def addToCart(request):
    user = request.user
    id = user.id
    count = request.POST['count']
    count = int(count)
    goods_id = request.POST['sku_id']
    goods = Goods.objects.get(id=goods_id)
    price = goods.shop_price
    goods_num = goods.goods_num
    if goods_num < count:
        messages.error(request, "库存不足")
        return reverse('goods:index')
    totalPrice = price*count
    cart = ShoppingCart.objects.create(nums=count, goods_id=goods_id, totalPrice=totalPrice, user_id=id)
    cart.save()
    goods.goods_num = goods_num - count
    goods.save()
    return JsonResponse({'status': 5, 'msg': "添加成功"})
# 更改购物车
def updateCart(request):
    sku_id = request.POST['sku_id']
    count = request.POST['count']
    count = int(count)
    shoppingCart = ShoppingCart.objects.get(id=sku_id)
    goods = Goods.objects.get(id=shoppingCart.goods_id)
    shoppingCart.nums = count
    shoppingCart.totalPrice = goods.shop_price*count
    shoppingCart.save()
    return JsonResponse({'status': 5, 'msg': '添加成功'})

# 删除购物车商品
def delete(request):
    sku_id = request.POST['sku_id']
    shoppingCart = ShoppingCart.objects.get(id=sku_id)
    shoppingCart.delete()
    return JsonResponse({'status': 5, 'msg': '删除成功'})

# 查看购物车
def shoppingCart(request, pk):
    trade = ShoppingCart.objects.filter(user_id=pk)
    temp = list(trade)
    result = len(temp)
    return render(request, 'trade/shoppingCart.html', {'trade': trade, 'result': result})


def order(request, id):
    goods = ShoppingCart.objects.filter(user_id=id)

    # orderInfo = OrderInfo.objects.create()
    totalPrice = 0
    for goods in goods:
        goodsPrice = Goods.objects.get(id=goods.goods_id).shop_price

        # order_goods = OrderGoods.objects.create(order_id=123, goods=goods.goods, goods_num=1)

        #print(type(order_goods))
        #order_goods.save()

        totalPrice =totalPrice + goodsPrice

    return render(request, 'trade/order.html', {'totlePrice': totalPrice})

# 添加购物车
def order_addToCart(request):
    user = request.user
    address = UserAddress.objects.filter(Q(user_id=user.id) & Q(is_default=True))
    if len(address) == 0:
        address1 = UserAddress.objects.filter(user_id=user.id)
        if len(address1) == 1:
            for address in address1:
                address.is_default = True
                address.save()
            address = UserAddress.objects.filter(Q(user_id=user.id) & Q(is_default=True))
        if len(address1) == 0:
            messages.error(request, '请先到用户中心添加收货地址')
            return HttpResponseRedirect(reverse('user_operation:toAddAddress'))
        if len(address1) > 1:
            messages.error(request, '请先设置默认收货地址')
            return HttpResponseRedirect(reverse('user_operation:userCenterAddress'))
        messages.error(request, '请先添加收货地址')
    sku_id = request.POST.getlist('sku_id')
    totalTrade = []

    totalPrice = 0
    totalCount = 0
    for i in sku_id:
        shoppingCart = ShoppingCart.objects.filter(id=i)
        if shoppingCart:
            for j in sku_id:
                shoppingCart = ShoppingCart.objects.get(id=j)
                totalTrade.append(shoppingCart)

                totalCount += shoppingCart.nums
                totalPrice += shoppingCart.totalPrice
            return render(request, 'trade/order.html', {'totalTrade': totalTrade, 'totalPrice': totalPrice, 'totalCount': totalCount, 'address': address, 'sku_id': sku_id, })

        else:
            print(1)
            id = request.POST['sku_id']
            num = request.POST['num_show']
            goods = Goods.objects.get(id=id)
            print(id, num, goods)
            trade = ShoppingCart(nums=1, add_time=datetime.now, goods_id=goods.id, user_id=user.id, totalPrice=goods.shop_price)
            totalTrade.append(trade)
            totalCount = num
            totalPrice = goods.shop_price * totalCount
            return render(request, 'trade/order.html', {'totalTrade': totalTrade, 'totalPrice': totalPrice, 'totalCount': totalCount, 'address': address, 'sku_id': sku_id, })

# 立即购买
def order_getNow(request):
    user = request.user
    address = UserAddress.objects.filter(Q(user_id=user.id) & Q(is_default=True))
    if len(address) == 0:
        address1 = UserAddress.objects.filter(user_id=user.id)
        if len(address1) == 1:
            for address in address1:
                address.is_default = True
                address.save()
            address = UserAddress.objects.filter(Q(user_id=user.id) & Q(is_default=True))
        if len(address1) == 0:
            messages.error(request, '请先到用户中心添加收货地址')
            return HttpResponseRedirect(reverse('user_operation:toAddAddress'))
        if len(address1) > 1:
            messages.error(request, '请先设置默认收货地址')
            return HttpResponseRedirect(reverse('user_operation:userCenterAddress'))
        messages.error(request, '请先添加收货地址')
    sku_id = request.POST.getlist('sku_id')
    print(sku_id)
    totalTrade = []

    totalPrice = 0
    totalCount = 0
    num = request.POST['num_show']
    num = int(num)
    for i in sku_id:
        print(i)
        goods = Goods.objects.get(id=i)
        print(id, num, goods)
        trade = ShoppingCart(nums=num, add_time=datetime.now, goods_id=goods.id, user_id=user.id, totalPrice=goods.shop_price*num)
        print(11)
        totalTrade.append(trade)
        totalCount = num
        totalPrice = goods.shop_price*totalCount
        print(totalPrice)
    return render(request, 'trade/order.html',
                  {'totalTrade': totalTrade, 'totalPrice': totalPrice, 'totalCount': totalCount, 'address': address,
                   'sku_id': sku_id, })

# 提交订单到系统并跳转支付链接支付
def submitOrder(request):
    user = request.user
    # 支付方式（1：微信(放弃，开通微信支付需300手续费)；2：支付宝）
    pay_id = request.POST.get('pay_id')
    # 收货地址id
    addressId = request.POST.get('add_id')
    address = UserAddress.objects.get(id=addressId)
    # 购物车商品列表
    tradelist = request.POST['skus']
    # 转义购物车商品id列表
    list = eval(tradelist.replace('[', '{').replace(']', '}'))
    # 生成订单号
    orderId = datetime.now().strftime('%Y%m%d%H%M%S')+str(user.id)
    totalPrice = 0.0
    good = []
    # 遍历商品获取总价并处理库存
    for i in list:

        trade = ShoppingCart.objects.get(id=i)

        totalPrice = totalPrice + trade.totalPrice

        goods = Goods.objects.get(id=trade.goods_id)
        good.append(goods)
        goods.goods_num -= trade.nums
        goods.sold_num += trade.nums
        goods.save()

    # 创建订单实例
    orderInfo = OrderInfo.objects.create(user=user, order_sn=orderId, pay_status="TRADE_SUCCESS", order_mount=totalPrice
                                         , create_time=datetime.now(), signer_mobile=address.signer_mobile, address=
                                         address.address, signer_name=address.signer_name)


    # 存储订单
    orderInfo.save()
    # 存储订单商品
    for i in good:
        ordergoods = OrderGoods.objects.create(order=orderInfo, goods=i, goods_num=trade.nums, add_time=datetime.now(),user_id=user.id, totalprice=trade.nums*i.shop_price)
        ordergoods.save()
    if pay_id is '2':
        order_id = str(orderId)
        totalPrice = request.POST.get('total_price')
        app_private_key_string = open(BASE_DIR + '\\apps\\trade\\keys\\app_private_key.pem').read()
        alipay_public_key_string = open(BASE_DIR + '\\apps\\trade\\keys\\alipay_public_key.pem').read()
        alipay = AliPay(
            appid="2016092700609431",
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type="RSA2",
            debug=True
        )
        total_price = totalPrice
        subject = "订单{id}".format(id=order_id)
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(0.01),
            subject=subject,
            return_url="http://127.0.0.1:8000/trade/pay_result/",
            notify_url="http://127.0.0.1:8000/trade/pay_result/",
        )
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'res': 3, 'msg': pay_url})

def check_pay(params):  # 定义检查支付结果的函数
    sign = params.pop('sign', None)  # 取出签名
    params.pop('sign_type')  # 取出签名类型
    params = sorted(params.items(), key=lambda e: e[0], reverse=False)  # 取出字典元素按key的字母升序排序形成列表
    message = "&".join(u"{}={}".format(k, v) for k, v in params).encode()  # 将列表转为二进制参数字符串
    # with open(settings.ALIPAY_PUBLIC_KEY_PATH, 'rb') as public_key: # 打开公钥文件
    try:
        pass
        #     status =verify_with_rsa(public_key.read().decode(),message,sign) # 验证签名并获取结果
        # status = verify_with_rsa(settings.ALIPAY_PUBLIC_KEY.encode('utf-8').decode('utf-8'), message,
        #                          sign)  # 验证签名并获取结果
        # return status   返回验证结果
    except:
        pass
    # except:  # 如果验证失败，返回假值。
    #     return False

#验证回调函数，确认订单状态
def pay_result(request):
    print(1)
    dict1 = dict(request.query_params)
    print(dict1)
    # response = alipay.api_alipay_trade_page_pay(order_id)
    alipay_request_dict = request.query_params  # query_params是一个QueryDict对象
    print(alipay_request_dict)

    # 如果查询字符串为空，表示前端没有将支付宝回调时携带的参数传递过来
    if not alipay_request_dict:
        return Response({"message": "缺少参数"}, status=status.HTTP_400_BAD_REQUEST)

    # 将QueryDict转换成python中的字典
    data = alipay_request_dict.dict()
    print(data)
    # 用pop方法取出签名，接口文档中推荐使用的方法
    sign = data.pop("sign")
    app_private_key_string = open(BASE_DIR + '\\apps\\trade\\keys\\app_private_key.pem').read()
    alipay_public_key_string = open(BASE_DIR + '\\apps\\trade\\keys\\alipay_public_key.pem').read()

    # 校验参数，使用AliPay模块来验证前端传过来的数据是否真的是支付宝在回调时携带的参数
    alipay = AliPay(
        appid="2016092700609431",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",
        debug=True
    )

    # verify函数返回验证结果，True 或 False
    result = alipay.verify(data, sign)
    print(result)
    if result:
        # 保存支付结果数据
        # out_trade_no: 订单号，    trade_no: 交易流水号
        # total_amount: 订单总金额   seller_id: 支付宝唯一用户号

        order_id = data.get("out_trade_no")  # 订单编号
        trade_id = data.get("trade_no")  # 交易流水号
        # 将付款记录写入数据库
        OrderInfo.objects.create(
            order_id=order_id,
            trade_id=trade_id,
        )

        # 修改订单状态
        OrderInfo.objects.filter(order_id=order_id).update(status=OrderInfo.ORDER_STATUS_ENUM["UNSEND"])

        # 返回 trade_id（交易流水号）
        return Response({"trade_id": trade_id})
    else:
        # 返回参数错误
        return Response({"message": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)

def aftersale(request):
    return JsonResponse({'res': 5, 'msg': '提交成功'})
