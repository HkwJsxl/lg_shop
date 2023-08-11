from django.urls import path
from . import views

urlpatterns = [
    # qq登录地址
    path("qq/login/", views.OAuthQQUrlView.as_view()),
    # qq回调地址
    path("qq/callback/", views.OAuthQQCallbacklView.as_view()),

]
