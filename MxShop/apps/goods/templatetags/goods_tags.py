
from goods.models import Goods, GoodsCategory, GoodsImage

from django import template

from django.db.models.aggregates import Count

register = template.Library()

#获取一级分类
@register.simple_tag
def get_firstcategory():
    return GoodsCategory.objects.filter(category_type=1)

#获取二级分类
@register.simple_tag
def get_secondcategory():
    return GoodsCategory.objects.filter(category_type=2)

#获取三个配件商品
@register.simple_tag
def get_others():
    return Goods.objects.filter(category_id=44).order_by('sold_num')[:3]