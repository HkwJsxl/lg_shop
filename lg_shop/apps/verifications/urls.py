from django.urls import path, re_path
from . import views

urlpatterns = [
    # 检查用户是否存在
    path("check/<str:username>/", views.CheckUserView.as_view()),
    # 检查手机号是否存在
    path("mobile/<str:mobile>/", views.CheckMobileView.as_view()),
    # 生成图形验证码
    re_path(r"^code/(?P<uuid>[\w-]+)/$", views.VerifyCodeView.as_view()),
    # 校验验证码
    re_path(r"^sms/(?P<mobile>1[3-9]\d{9})/$", views.SMSCodeView.as_view()),
    # 发送邮箱
    path("email/", views.EmailView.as_view()),
    # 激活邮箱
    path("email/verification/", views.EmailVerifyView.as_view()),
]
