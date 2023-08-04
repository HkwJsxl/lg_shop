from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseForbidden

from django_redis import get_redis_connection

from .forms import RegisterForm
from .models import UserInfo
from response_code import RETCODE, err_msg


class RegisterView(View):
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
