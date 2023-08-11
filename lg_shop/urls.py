from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include(('users.urls', 'users'), namespace='users')),
    path('api/contents/', include(('contents.urls', 'contents'), namespace='contents')),
    path('api/verify/', include(('verifications.urls', 'verifications'), namespace='verify')),
    path('api/areas/', include(('areas.urls', 'areas'), namespace='areas')),
    path('api/oauth/', include(('oauth.urls', 'oauth'), namespace='oauth')),
]
