import re

from django.contrib.auth.backends import ModelBackend

from users.models import UserInfo


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
