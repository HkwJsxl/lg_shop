import random

from django.shortcuts import render, HttpResponse
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings

from django_redis import get_redis_connection

from users.models import UserInfo
from captcha import captcha
from sms import sms_sington
from response_code import RETCODE, err_msg
from constants import SMS_CODE_EXPIRES, IMAGE_CODE_EXPIRES, SMS_FLAG_EXPIRES


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
        redis_conn.setex(f"img_{uuid}", IMAGE_CODE_EXPIRES, text)  # name time value
        # 返回图片
        return HttpResponse(image, content_type="image/png")


class SMSCodeView(View):
    def get(self, request, mobile):
        # 接受校验参数
        uuid = request.GET.get("uuid")
        image_code = request.GET.get("image_code")
        if not all([uuid, image_code]):
            return HttpResponseForbidden("参数校验失败.")
        redis_conn = get_redis_connection("verifications")
        # 校验短信标识符，限制用户发送验证码频率
        sms_flag_redis = redis_conn.get(f"sms_flag_{mobile}")
        if sms_flag_redis:
            return JsonResponse({"code": RETCODE.THROTTLINGERR, "msg": err_msg.get(f"{RETCODE.THROTTLINGERR}")})
        # 提取图形验证码
        image_code_redis = redis_conn.get(f"img_{uuid}")  # 取出来是bytes类型
        # 删除图形验证码
        redis_conn.delete(f"img_{uuid}")
        # 对比图形验证码
        if not image_code_redis or image_code_redis.decode().lower() != image_code.lower():
            return JsonResponse({"code": RETCODE.IMAGECODEERR, "msg": err_msg.get(f"{RETCODE.IMAGECODEERR}")})
        # 生成短信验证码
        sms_code = f"{random.randint(0, 9999):04d}"
        # 发送验证码
        response = sms_sington.send_sms(tid=settings.RONGLIANYUN.get("reg_tid"), mobile=mobile,
                                        datas=(sms_code, SMS_CODE_EXPIRES // 60))
        if response.get("statusCode") == "000000":
            # 只有短信发送成功的时候才保存短信验证码
            redis_conn.setex(f"sms_code_{mobile}", SMS_CODE_EXPIRES, sms_code)  # name time value
            redis_conn.setex(f"sms_flag_{mobile}", SMS_FLAG_EXPIRES, 1)  # name time value
            return JsonResponse({"code": RETCODE.OK, "msg": err_msg.get(f"{RETCODE.OK}")})
        return JsonResponse({"code": RETCODE.SMSCODESENDRR, "msg": err_msg.get(f"{RETCODE.SMSCODESENDRR}")})
