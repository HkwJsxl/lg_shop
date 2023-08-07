from django.db import models
from django.contrib.auth.models import AbstractUser

from models import BaseModel


class UserInfo(AbstractUser):
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    email_actived = models.BooleanField(default=False, verbose_name="邮箱验证")

    default_address = models.ForeignKey("Address", related_name="users", null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name="默认地址")

    class Meta:
        db_table = "lg_userinfo"
        verbose_name = "账户"
        verbose_name_plural = verbose_name


class Address(BaseModel):
    """用户地址"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    province = models.ForeignKey('areas.Areas', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Areas', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Areas', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')

    receiver = models.CharField(max_length=32, verbose_name='收货人')
    place = models.CharField(max_length=64, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=32, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=32, null=True, blank=True, default='', verbose_name='电子邮箱')

    class Meta:
        db_table = 'lg_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-updated_time']
