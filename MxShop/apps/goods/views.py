from django.shortcuts import render, redirect
# Create your views here.
from goods.models import GoodsCategory, Goods, Banner
from django.db.models import Q



def index(request):
    latest_goods = Goods.objects.filter(~Q(category_id=44)).order_by("-add_time")[:3]
    mostpopular_goods = Goods.objects.filter(~Q(category_id=44)).order_by("sold_num")[:3]
    recommend = Goods.objects.filter(~Q(category_id=44)).order_by("click_num")[:4]
    carousel_goods = Banner.objects.all().order_by("index")[:3]
    return render(request, 'goods/index.html', {'mostpopular_goods': mostpopular_goods,
                                        'latest_goods': latest_goods,
                                        'recommend':recommend,
                                        'carousel_goods':carousel_goods,
                                                }
                  )

def detail(request, pk):
    goods = Goods.objects.get(pk=pk)
    recommend_goods = Goods.objects.filter(category=goods.category).order_by("sold_num")[:5]
    return render(request, 'goods/details.html', {
        'goods': goods,
        'recommend_goods': recommend_goods,
    })

def goodsList(request, pk):
    category = GoodsCategory.objects.get(pk=pk)
    list = Goods.objects.filter(category=category).order_by('sold_num')
    print(len(list))

    return render(request, 'goods/goodslist.html', {'list': list})


