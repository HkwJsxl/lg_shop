import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lg_shop.settings.dev')

from django.test import TestCase

from django.conf import settings

from fdfs_client.client import Fdfs_client

# 加载配置文件
client = Fdfs_client(settings.FASTDFS_CONF)
# 批量上传文件（ps:项目跟目录下的static/images）
images_path = os.path.join(settings.BASE_DIR.parent, "static\images")
for line in os.listdir(images_path):
    file_path = os.path.join(images_path, line)
    print(file_path)
    # 上传文件
    # rets = client.upload_by_filename(file_path)
    # print(rets)
    # 返回的`Remote file_id`写入数据库
    ...
