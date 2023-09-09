from django.urls import path, re_path
from . import views

# /list/(?P<category_id>\d+)/(?P<page_num>\d+)/?sort=排序方式
# # http://127.0.0.1:8000/list/115/3/?sort=default
urlpatterns = [
    # 商品列表页面
    re_path(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.GoodsListView.as_view(), name='list'),
    # 商品热销排行
    re_path(r'^hot/(?P<category_id>\d+)/$', views.HotGoodsView.as_view())
]
