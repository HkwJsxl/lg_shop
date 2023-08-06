import re

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings

from authlib.jose import jwt, JoseError

from users.models import UserInfo
from response_code import RETCODE, err_msg
from authlib_jwt import generate_token


class ReModelBackend(ModelBackend):
    """登录多方式认证类（支持手机号和用户名登录）"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        """重写authenticate方法"""
        user = self.user_or_none(username)
        if user and user.check_password(password):
            return user
        else:
            return None

    def user_or_none(self, account):
        """
        自定义方法
        account: 用户名或手机号
        return: user对象或None
        """
        is_match = re.match(r"1[3-9]\d{9}$", account)
        try:
            if is_match:
                user = UserInfo.objects.get(mobile=account)
            else:
                user = UserInfo.objects.get(username=account)
        except:
            return None
        else:
            return user


class LoginRequiredJSONMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({"code": RETCODE.SESSIONERR, "msg": err_msg.get(f"{RETCODE.SESSIONERR}")})


def generate_email_verify(email, user_id):
    """生成邮箱验证链接"""
    token = generate_token(user_id, email)
    # 生成链接
    email_verify_url = "%s?token=%s" % (settings.EMAIL_VERIFY_URL, token.decode())
    return email_verify_url
