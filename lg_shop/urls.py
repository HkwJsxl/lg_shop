from django.contrib import admin
from django.urls import path, include, re_path

# from django.views.static import serve
# from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include(('users.urls', 'users'), namespace='users')),
    path('api/contents/', include(('contents.urls', 'contents'), namespace='contents')),
    path('api/verify/', include(('verifications.urls', 'verifications'), namespace='verify')),
    path('api/areas/', include(('areas.urls', 'areas'), namespace='areas')),
    path('api/oauth/', include(('oauth.urls', 'oauth'), namespace='oauth')),
    path('api/goods/', include(('goods.urls', 'goods'), namespace='goods')),

    # 开放静态文件
    # re_path(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT})

]
