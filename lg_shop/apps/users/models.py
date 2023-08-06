from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    email_actived = models.BooleanField(default=False, verbose_name="邮箱验证")

    class Meta:
        db_table = "lg_userinfo"
        verbose_name = "账户"
        verbose_name_plural = verbose_name
