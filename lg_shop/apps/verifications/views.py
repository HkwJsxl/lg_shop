from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse

from django_redis import get_redis_connection

from users.models import UserInfo
from captcha import captcha


class CheckUserView(View):
    def get(self, request, username):
        count = UserInfo.objects.filter(username=username).count()
        return JsonResponse({"code": 0, "messages": "成功", "count": count})


class CheckMobileView(View):
    def get(self, request, mobile):
        count = UserInfo.objects.filter(mobile=mobile).count()
        return JsonResponse({"code": 0, "messages": "成功", "count": count})


class VerifyCodeView(View):
    def get(self, request, uuid):
        # 生成图片
        text, image = captcha.generate_captcha()
        # 获取redis链接
        redis_conn = get_redis_connection("verifications")
        # 设置redis缓存
        redis_conn.setex(f"img_{uuid}", 60, text)  # name time value
        # 返回图片
        return HttpResponse(image, content_type="image/png")
