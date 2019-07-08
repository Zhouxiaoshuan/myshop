#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xadmin
from .models import UserFav, UserLeavingMessage, UserAddress, UserComment


class UserFavAdmin(object):
    list_display = ['user', 'goods', "add_time"]


class UserLeavingMessageAdmin(object):
    list_display = ['user', 'message_type', "message", "add_time"]


class UserAddressAdmin(object):
    list_display = ["user", "signer_name", "signer_mobile", "address", "is_default"]

class UserCommentAdmin(object):
    list_display = ["user", "goods", "service", "quality", "express", "comment"]

xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)
xadmin.site.register(UserLeavingMessage, UserLeavingMessageAdmin)
xadmin.site.register(UserComment, UserCommentAdmin)