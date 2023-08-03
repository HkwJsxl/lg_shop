import random

from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse
from django.conf import settings

from django_redis import get_redis_connection

from users.models import UserInfo
from captcha import captcha
from sms.ronglianyunapi import send_sms


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


class SMSCodeView(View):
    def get(self, request, mobile):
        # 生成验证码
        sms_code = f"{random.randint(0, 9999):04d}"
        # 获取redis链接
        redis_conn = get_redis_connection("sms")
        # 设置redis缓存
        redis_conn.setex(f"sms_code_{mobile}", 60, sms_code)  # name time value

        # 发送验证码
        response = send_sms(tid=settings.RONGLIANYUN.get("reg_tid"), mobile=mobile, datas=(sms_code, 1))
        return response
