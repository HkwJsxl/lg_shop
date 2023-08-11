from django.db import models

from models import BaseModel


class OAuthQQ(BaseModel):
    user = models.ForeignKey("users.UserInfo", verbose_name="用户", on_delete=models.CASCADE)
    openid = models.CharField(verbose_name="openid", max_length=64, db_index=True)

    class Meta:
        db_table = "lg_oauth_qq"
        verbose_name = "请求登录"
        verbose_name_plural = verbose_name
