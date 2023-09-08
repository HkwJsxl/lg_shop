from django.shortcuts import render
from django.views import View
from contents.utlis import get_categories
from .models import GoodsCategory, SKU
from django import http
from .utils import get_breadcrumb


class GoodsListView(View):
    """商量列表页面"""

    def get(self, request, category_id, page_num):

        # category_id 参数校验
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except Exception as e:
            return http.HttpResponseForbidden('参数category_id不存在')

        # 获取sort排序 ?sort=juran
        sort = request.GET.get('sort', 'default')
        if sort == 'price':
            sort_field = 'price'
        elif sort == 'hot':
            sort_field = 'sales'
        else:
            sort = 'default'
            sort_field = 'create_time'

        # 查询商品分类
        categories = get_categories()
        # 查询面包屑
        # category_id
        breadcrumb = get_breadcrumb(category)

        # 分页和排序
        skus = SKU.objects.filter(is_launched=True, category_id=category.id).order_by(sort_field)
        print(skus)

        # breadcrumb = {
        #     'cat1': category.parent.parent,
        #     'cat2': category.parent,
        #     'cat3': category
        # }

        context = {
            'categories': categories,
            'breadcrumb': breadcrumb,
        }
        return render(request, 'list.html', context=context)


"""
# 按照商品创建时间排序
http://www.meiduo.site:8000/list/115/1/?sort=default
# 按照商品价格由低到高排序
http://www.meiduo.site:8000/list/115/1/?sort=price
# 按照商品销量由高到低排序
http://www.meiduo.site:8000/list/115/1/?sort=hot
# 用户随意传排序
http://www.meiduo.site:8000/list/115/1/?sort=juran
"""
