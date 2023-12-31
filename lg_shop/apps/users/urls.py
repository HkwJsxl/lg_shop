from django.urls import path, re_path
from . import views

urlpatterns = [
    # 注册
    path("register/", views.RegisterView.as_view(), name="register"),
    # 登录
    path("login/", views.LoginView.as_view(), name="login"),
    # 退出登录
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # 个人中心
    path("info/", views.UserInfoView.as_view(), name="info"),
    # 收货地址
    path("addresses/", views.AddressView.as_view(), name="address"),
    # 创建地址
    path("addresses/create/", views.AddressCreateView.as_view(), name="address_create"),
    # 修改，删除
    path("addresses/<str:address_pk>/", views.AddressUpdateDestoryView.as_view(), name="address_update"),
    # 修改默认收获地址
    path("addresses/<str:default_id>/default/", views.AddressDefaultView.as_view(), name="address_default"),
    # 修改密码
    path("password/change/", views.ChangePasswordView.as_view(), name="pass"),
]
