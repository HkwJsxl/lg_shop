import random
import json
import re

from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings

from django_redis import get_redis_connection

from users.models import UserInfo
from captcha import captcha, captcha2
from response_code import RETCODE, err_msg
from constants import SMS_CODE_EXPIRES, IMAGE_CODE_EXPIRES, SMS_FLAG_EXPIRES
# from celeryapp.sms.tasks import send_sms_code
from verifications.tasks import send_sms_code, send_email_verify
from authenticate import LoginRequiredJSONMixin
from authlib_jwt import validate_token


class CheckUserView(View):
    """检查用户是否存在"""

    def get(self, request, username):
        count = UserInfo.objects.filter(username=username).count()
        return JsonResponse({"code": 0, "messages": "成功", "count": count})


class CheckMobileView(View):
    """检查手机号是否存在"""

    def get(self, request, mobile):
        count = UserInfo.objects.filter(mobile=mobile).count()
        return JsonResponse({"code": 0, "messages": "成功", "count": count})


class VerifyCodeView(View):
    """生成图片验证码"""

    def get(self, request, uuid):
        # 生成图片
        text, image = captcha.generate_captcha()
        # text, image = captcha2.create_image_code()
        # 获取redis链接
        redis_conn = get_redis_connection("verifications")
        # 设置redis缓存
        redis_conn.setex(f"img_{uuid}", IMAGE_CODE_EXPIRES, text)  # name time value
        # 返回图片
        return HttpResponse(image, content_type="image/png")


class SMSCodeView(View):
    """校验验证码"""

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
        response = send_sms_code.delay(tid=settings.RONGLIANYUN.get("reg_tid"), mobile=mobile,
                                       datas=(sms_code, SMS_CODE_EXPIRES // 60))
        if response:
            # response返回的是任务id
            # 只有短信发送成功的时候才保存短信验证码
            pipe = redis_conn.pipeline()
            pipe.multi()  # 开启事务
            pipe.setex(f"sms_code_{mobile}", SMS_CODE_EXPIRES, sms_code)  # name time value
            pipe.setex(f"sms_flag_{mobile}", SMS_FLAG_EXPIRES, 1)
            pipe.execute()  # 提交事务，同时把暂存在pipeline的数据一次性提交给redis
            return JsonResponse({"code": RETCODE.OK, "msg": err_msg.get(f"{RETCODE.OK}")})
        return JsonResponse({"code": RETCODE.SMSCODESENDRR, "msg": err_msg.get(f"{RETCODE.SMSCODESENDRR}")})


class EmailView(LoginRequiredJSONMixin, View):
    """邮箱验证"""

    def put(self, request):
        # 获取数据
        request_body = request.body.decode()
        request_body_json = json.loads(request_body)
        email = request_body_json.get("email")
        # 校验邮箱格式
        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            return HttpResponseForbidden("邮箱格式错误.")
        # 发送邮箱(异步)
        send_email_verify.delay(email, request.user.id)
        # 保存数据
        try:
            request.user.email = email
            request.user.save()
        except:
            return JsonResponse({"code": RETCODE.DBERR, "msg": "邮箱保存失败."})
        # 返回数据
        return JsonResponse({"code": RETCODE.OK, "msg": err_msg.get(f"{RETCODE.OK}")})


class EmailVerifyView(View):
    """邮箱激活链接校验"""

    def get(self, request):
        # 获取数据
        token = request.GET.get("token")
        if not token:
            return HttpResponseForbidden("缺少参数token.")
        # 解密
        user = validate_token(token)
        if not user:
            return JsonResponse({"code": RETCODE.DBERR, "msg": "参数校验失败."})
        # 查看邮箱激活状态
        if user.email_actived:
            return JsonResponse({"code": RETCODE.DBERR, "msg": "邮箱已激活，请勿重复操作."})
        # 设置邮箱已激活
        user.email_actived = True
        user.save(update_fields=["email_actived"])
        return JsonResponse({"code": RETCODE.OK, "msg": "成功."})
