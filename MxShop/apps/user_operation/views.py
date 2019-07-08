from django.shortcuts import render, redirect
from trade.models import OrderInfo, OrderGoods, Aftersale
from goods.models import Goods
from user_operation.models import UserAddress, UserComment
from django.db.models import Q
from django.http import JsonResponse
import random
from datetime import datetime
from django.core.mail import send_mail
from goods.goods_form import UserRegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
# Create your views here.


def userCenter(request, pk):
    return render(request, 'user_operation/usercenter.html')




def userCenterOrder(request):
    user = request.user
    ordergoods = OrderGoods.objects.filter(Q(user_id=user.id) & Q(comment="undone"))
    return render(request, 'user_operation/userCenterOrder.html', {'ordergoods': ordergoods})



def userCenterInfo(request):

    return render(request, 'user_operation/userCenterInfo.html')


def userCenterAddress(request):
    user = request.user
    address = UserAddress.objects.filter(user_id=user.id)
    temp = list(address)
    result = len(temp)
    return render(request, 'user_operation/userCenterAddress.html', {'address': address, 'result': result})

def toAddAddress(request):
    return render(request, 'user_operation/addAddress.html')

def addAddress(request):
    user = request.user
    username = request.POST['username']
    mobile = request.POST['mobile']
    address = request.POST['address']
    newaddress = UserAddress.objects.create(signer_name=username, signer_mobile=mobile, user_id=user.id, address=address)
    newaddress.save()
    return redirect('user_operation:userCenterAddress')

def userCenterHistory(request):
    user = request.user
    ordergoods = OrderGoods.objects.filter(user=user).order_by('-add_time')
    return render(request, 'user_operation/userCenterHistory.html', {'ordergoods': ordergoods})


def toUpdateAddress(request, pk):
    address = UserAddress.objects.get(id=pk)
    return render(request, 'user_operation/updateAddress.html', {'address': address})

def updateAddress(request):
    addressId = request.POST['addressId']
    signer_name = request.POST['username']
    signer_mobile = request.POST['mobile']
    addr = request.POST['address']
    address = UserAddress.objects.get(id=addressId)
    address.signer_name = signer_name
    address.signer_mobile = signer_mobile
    address.address = addr
    address.save()
    return redirect('user_operation:userCenterAddress')



def setDefaultAddress(request):
    id = request.POST.get('addressId')
    id = int(id)
    user = request.user
    default = UserAddress.objects.get(id=id)
    default.is_default = True
    default.save()
    address = UserAddress.objects.filter(Q(user=user.id) & ~Q(id=id))
    for address in address:
        address.is_default = False
        address.save()
    return JsonResponse({'status': 5, 'msg': '设置成功'})

def deleteAddress(request):
    addressId = request.POST.get('addressId')
    address = UserAddress.objects.get(id=addressId)
    address.delete()
    return JsonResponse({'status': 5, 'msg': '删除成功'})

def updateUser(request):
    requestuser = request.user
    username = request.POST.get('username')
    email = request.POST.get('email')
    alluser = User.objects.all()
    #  确定有修改信息
    if(username == requestuser.username and email == requestuser.email):
        # 没有修改则刷新页面
        return JsonResponse({'status': 3})
    else:
        # 有修改，只改了用户名
        if(email == requestuser.email and username != requestuser.username):
            for user in alluser:
                # 检验新用户名是否重复
                if(user.username == username):
                    return JsonResponse({'status': 1, 'msg': "用户名已存在"})
            requestuser.username = username
            requestuser.save()
            return JsonResponse({'status': 5, 'msg': '用户名修改成功'})
        # 有修改，只改了邮箱
        elif(username == requestuser.username and email != requestuser.email):
            for user in alluser:
                # 检验新邮箱是否重复
                if(user.email == email):
                    return JsonResponse({'status': 2, 'msg': "邮箱已存在"})
            requestuser.email = email
            requestuser.save()
            return JsonResponse({'status': 5, 'msg': '邮箱修改成功'})

def findPassword(request):
    return render(request, 'user_operation/findPassword.html')

def getCode(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email)
        if user:
            char = '0123456789'
            length = len(char) - 1
            checkword = ''
            for x in range(6):
                checkword += char[random.randint(1, length)]
            reply = send_mail(
                '验证码',
                checkword,
                '1925387431@qq.com',
                [email]
            )
            if reply == 1:
                return render(request, 'user_operation/checkcode.html', {'checkword': checkword, 'email': email})
            else:
                messages.error(request, '发送异常，请重试')
                return render(request, 'user_operation/findPassword.html')

        else:
            messages.error(request, '该邮箱未注册')
            return render(request, 'user_operation/findPassword.html')


def checkCode(request):
    if request.method == 'POST':
        checkword = request.POST['checkword']
        email = request.POST['email']
        code = request.POST['code']
        if(checkword == code):
            return render(request, 'user_operation/setnewpw.html', {'email': email})
        else:
            messages.error(request, '验证码错误')
            return render(request, 'user_operation/checkcode.html')
def tosetnewpw(request):
    return render(request, 'user_operation/setnewpw.html')


def setNewPassword(request):
    if request.method == 'POST':
        newpw = request.POST.get('newpw')
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        user.set_password(newpw)
        user.save()
        return JsonResponse({'res': 1, 'msg': '密码重置成功'})



def toComment(request, pk):
    goods = Goods.objects.get(id=pk)
    recommend_goods = Goods.objects.filter(category=goods.category).order_by("sold_num")[:5]
    return render(request, 'user_operation/comment.html', {'goods': goods, 'recommend_goods': recommend_goods})


def Comment(request):
    user = request.user
    pk = request.POST.get('goodsId')
    service = request.POST.get('service')
    quality = request.POST.get('quality')
    express = request.POST.get('express')
    comment = request.POST.get('comment')
    goods = Goods.objects.get(id=pk)
    newComment = UserComment.objects.create(user=user, goods=goods, service=service, quality=quality, express=express,
                                            comment=comment)
    newComment.save
    return JsonResponse({'res': 5, 'msg': '评论成功'})

def toAftersale(request):
    return render(request, 'user_operation/aftersale.html')


def aftersale(request):
    return render(request, 'user_operation/userCenterOrder.html')




def toLogin(request):
    request.session['login_from'] = request.META.get('HTTP_REFERER', '/')
    requestfrom = request.session['login_from']
    return render(request, 'user_operation/login.html', {'requestfrom': requestfrom})

def toRegister(request):

    return render(request, 'user_operation/register.html')

def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        requesturl = request.POST.get('requesturl')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if requesturl == 'http://localhost:8000/toRegister/':
                return redirect('/')
            else:
                return HttpResponseRedirect(requesturl)
        else:
            messages.error(request, '请输入正确的用户名和密码！')
            return render(request, 'user_operation/login.html')



def userLogout(request):
    logout(request)
    return redirect('/')


def userRegister(request):
    if request.method == 'POST':
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            same_name_user = User.objects.filter(username=username)
            if same_name_user:
                messages.error(request, '用户名已存在，请重新输入用户名！')
                return render(request, 'user_operation/register.html')
            same_email_user = User.objects.filter(email=email)
            if same_email_user:
                messages.error(request, '该邮箱已经注册，快去找回密码吧！')
                return render(request, 'user_operation/register.html')
            new_user = User.objects.create_user(username=username, password=password, email=email)
            new_user.save()
            login(request, new_user)
            return redirect('/')
        else:
            messages.error(request, '用户名已存在！')
            return render(request, 'user_operation/register.html')


def tochangegoods(request):
    return render(request, 'user_operation/logisticsInfo.html')

def toreturngoods(request):
    return render(request, 'user_operation/logisticsInfo.html')

def changegoods(request):
    user = request.user
    logistics = request.POST.get("logistics")
    number = request.POST.get("number")
    reason = request.POST.get("reason")
    event = "换货"
    newgoods = Aftersale.objects.create(logistics=logistics, number=number, reason=reason, create_time=datetime.now(),
                                        user=user, event=event)
    newgoods.save()
    return JsonResponse({'res': 5, 'msg': '换货申请成功'})

def returngoods(request):
    user = request.user
    logistics = request.POST.get("logistics")
    number = request.POST.get("number")
    reason = request.POST.get("reason")
    event = "退货"
    newgoods = Aftersale.objects.create(logistics=logistics, number=number, reason=reason, create_time=datetime.now(),
                                        user=user, event=event)
    newgoods.save()
    return JsonResponse({'res': 5, 'msg': '退货申请成功'})
