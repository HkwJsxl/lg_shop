REDIS_PASSWORD = "root123456"
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

# 任务队列的链接地址
broker_url = 'redis://:%s@%s:%s/14' % (
    REDIS_PASSWORD, REDIS_HOST, REDIS_PORT
)
# 结果队列的链接地址
result_backend = 'redis://:%s@%s:%s/15' % (
    REDIS_PASSWORD, REDIS_HOST, REDIS_PORT
)
