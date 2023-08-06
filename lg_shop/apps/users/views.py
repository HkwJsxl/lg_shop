from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from django_redis import get_redis_connection

from .forms import RegisterForm, LoginForm
from .models import UserInfo
from response_code import RETCODE, err_msg


class RegisterView(View):
    """注册视图"""

    def get(self, request, *args, **kwargs):
        return render(request, "register.html")

    def post(self, request, *args, **kwargs):
        form_obj = RegisterForm(request.POST)
        if not form_obj.is_valid():
            return render(request, "register.html", {"return_msg": f"数据校验失败-{form_obj.errors}"})
        form_obj.cleaned_data.pop("confirm_password")
        sms_code = form_obj.cleaned_data.pop("sms_code")
        mobile = form_obj.cleaned_data.get("mobile")

        # 校验短信验证码
        redis_conn = get_redis_connection("verifications")
        sms_code_redis = redis_conn.get(f"sms_code_{mobile}")
        if not sms_code_redis:
            return HttpResponseForbidden("短信验证码失效.")
        if sms_code != sms_code_redis.decode():
            return render(request, "register.html", {"return_msg": err_msg.get(f"{RETCODE.SMSCODESENDRR}")})
        # 写入数据库
        try:
            user = UserInfo.objects.create_user(**form_obj.cleaned_data)
            # 保持登录状态
            login(request, user)
            # 删除短信验证码
            redis_conn.delete(f"sms_code_{mobile}")
            return redirect(reverse("contents:index"))
        except Exception as e:
            return render(request, "register.html", {"return_msg": f"注册失败-{e}"})


class LoginView(View):
    """登录视图"""

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        form_obj = LoginForm(request.POST)
        if not form_obj.is_valid():
            return render(request, "login.html", {"return_msg": "数据校验失败."})
        username = form_obj.cleaned_data.get("username")
        password = form_obj.cleaned_data.get("password")
        remembered = form_obj.cleaned_data.get("remembered")
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, "login.html", {"return_msg": "用户名或密码错误."})
        login(request, user)
        # 设置失效时间
        if not remembered:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        # 跳转到未登录前的页面
        next_url = request.GET.get("next")
        if next_url:
            response = redirect(next_url)
        else:
            response = redirect(reverse("contents:index"))
        # 迎合前端，首页获取cookie展示用户名
        response.set_cookie("username", user.username, settings.SESSION_COOKIE_AGE)
        return response


class LogoutView(View):
    """退出登录"""

    def get(self, request):
        logout(request)
        response = redirect(reverse("users:login"))
        response.delete_cookie("username")
        return response


class UserInfoView(LoginRequiredMixin, View):
    """
    用户中心
    LoginRequiredMixin: 校验是否登录，全局配置变量LOGIN_URL
    """

    def get(self, request):
        contents = {
            "username": request.user.username,
            "mobile": request.user.mobile,
            "email": request.user.email,
            "email_actived": request.user.email_actived,
        }
        return render(request, "user_center_info.html", contents)
