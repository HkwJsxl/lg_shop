import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lg_shop.settings.dev')

from django.test import TestCase

from django.conf import settings
from fdfs_client.client import Fdfs_client

# 加载配置文件
client = Fdfs_client(settings.FASTDFS_CONF)
# 上传文件
rets = client.upload_by_filename(r"C:\Users\Administrator\Pictures\icon.jpg")
print(rets)

'''
	上传成功后的返回值
    {
        "Group name": "group1",  # 组名
        "Remote file_id": "group1/M00/00/00/rBEAA2TsEjKAfxYVAAAP8lLos1M446.jpg",  # 文件索引，可用于下载
        "Status": "Upload successed.",  # 文件上传结果反馈
        "Local file name": "C:\\Users\\Administrator\\Pictures\\icon.jpg",  # 文件上传全路径
        "Uploaded size": "3.99KB",  # 文件大小
        "Storage IP": "47.120.38.34"  # Storage地址
    }

'''
