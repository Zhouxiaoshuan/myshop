from django.conf.urls import url
from . import views

app_name = 'user_operation'

urlpatterns = [
    url('^userCenter/(?P<pk>[0-9]+)/$', views.userCenter, name='userCenter'),
    url('^userCenterOrder/$', views.userCenterOrder, name='userCenterOrder'),
    url('^userCenterInfo/$', views.userCenterInfo, name='userCenterInfo'),
    url('^userCenterAddress/$', views.userCenterAddress, name='userCenterAddress'),
    url('^userCenterHistory/$', views.userCenterHistory, name='userCenterHistory'),
    url('^setDefaultAddress/$', views.setDefaultAddress, name='setDefaultAddress'),
    url('^deleteAddress/$', views.deleteAddress, name='deleteAddress'),
    url('^updateAddress/$', views.updateAddress, name='updateAddress'),
    url('^toAddAddress/$', views.toAddAddress, name='toAddAddress'),
    url('^addAddress/$', views.addAddress, name='addAddress'),
    url('^updateAddress/$', views.updateAddress, name='updateAddress'),
    url('^toUpdateAddress/(?P<pk>[0-9]+)/$', views.toUpdateAddress, name='toUpdateAddress'),
    url('^updateUser/$', views.updateUser, name='updateUser'),
    url('^findPassword/$', views.findPassword, name='findPassword'),
    url('^getCode/$', views.getCode, name='getCode'),
    url('^checkCode/$', views.checkCode, name='checkCode'),
    url('^setNewPassword/$', views.setNewPassword, name='setNewPassword'),
    url('^tosetnewpw/$', views.tosetnewpw, name='tosetnewpw'),
    url('^toComment/(?P<pk>[0-9]+)/$', views.toComment, name='toComment'),
    url('^Comment/$', views.Comment, name='Comment'),
    url('^toAftersale/$', views.toAftersale, name='toAftersale'),
    url('^aftersale/$', views.aftersale, name='aftersale'),
    url('^toLogin/$', views.toLogin, name='toLogin'),
    url('^toRegister/$', views.toRegister, name='toRegister'),
    url('^userLogin/$', views.userLogin, name='userLogin'),
    url('^userLogout/$', views.userLogout, name='userLogout'),
    url('^userRegister/$', views.userRegister, name='userRegister'),
    url('^tochangegoods/$', views.tochangegoods, name='tochangegoods'),
    url('^toreturngoods/$', views.toreturngoods, name='toreturngoods'),
    url('^changegoods/$', views.changegoods, name='changegoods'),
    url('^returngoods/$', views.returngoods, name='returngoods'),
]
