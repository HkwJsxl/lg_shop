from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.contrib.auth import login
from django.http import JsonResponse

from .forms import RegisterForm
from .models import UserInfo


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "register.html")

    def post(self, request, *args, **kwargs):
        form_obj = RegisterForm(request.POST)
        if not form_obj.is_valid():
            return render(request, "register.html", {"return_msg": f"数据校验失败-{form_obj.errors}"})
        form_obj.cleaned_data.pop("confirm_password")
        try:
            user = UserInfo.objects.create_user(**form_obj.cleaned_data)
            # 保持登录状态
            login(request, user)
            return redirect(reverse("contents:index"))
        except Exception as e:
            return render(request, "register.html", {"return_msg": f"注册失败-{e}"})


class CheckUserView(View):
    def get(self, request, username):
        count = UserInfo.objects.filter(username=username).count()
        return JsonResponse({"code": 0, "messages": "成功", "count": count})


class CheckMobileView(View):
    def get(self, request, mobile):
        count = UserInfo.objects.filter(mobile=mobile).count()
        return JsonResponse({"code": 0, "messages": "成功", "count": count})
