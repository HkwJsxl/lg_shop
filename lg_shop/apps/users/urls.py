from django.urls import path, re_path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # 个人中心
    path("info/", views.UserInfoView.as_view(), name="info"),
    # 收货地址
    path("addresses/", views.AddressView.as_view(), name="address"),
    path("addresses/create/", views.AddressCreateView.as_view(), name="address_create"),
]
