import os
from celery import Celery

# 必须在实例化celery应用对象之前执行(Django项目manage.py里面的)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lg_shop.settings.dev')

# 实例化celery应用，参数一般为项目应用名
app = Celery("lg_shop")
# 指定任务的队列名称
app.conf.task_default_queue = 'Celery'
# 可以把配置写在django的项目配置中
# 设置django中配置信息以 "CELERY_"开头为celery的配置信息
app.config_from_object('django.conf:settings', namespace='CELERY')
# 注册任务，自动搜索并加载任务
app.autodiscover_tasks()

# 启动Celery的终端命令
# celery -A lg_shop worker --loglevel=info  # windows不好使，能接收到任务，但不执行
# celery -A lg_shop worker --loglevel=info --pool=solo  # windows加上这个参数
# celery -A lg_shop worker --loglevel=info -P eventlet -c 10  # 或者使用eventlet，-c是协程的数量，生产环境可以用1000
