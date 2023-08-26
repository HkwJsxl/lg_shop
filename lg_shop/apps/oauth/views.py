import re

from django.shortcuts import render, redirect
from django.views import View
from django import http
from django.conf import settings
from django.contrib.auth import login

from django_redis import get_redis_connection

from QQLoginTool.QQtool import OAuthQQ
from response_code import RETCODE
from logger import log
from .models import OAuthQQ as OAuthQQUser
from users.models import UserInfo
from authlib_jwt import generate_access_token, check_access_token


class OAuthQQUrlView(View):
    """QQ登录url"""

    def get(self, request):
        """Oauth2.0认证"""
        # next: 从哪个页面进入到的登录页面，登录成功后自动回到那个页面
        next_url = request.GET.get('next')
        # 获取QQ登录页面网址
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI, state=next_url)
        login_url = oauth.get_qq_url()
        return http.JsonResponse({"code": RETCODE.OK, "msg": "成功", "login_url": login_url})


class OAuthQQCallbacklView(View):
    """QQ登录回调"""

    def get(self, request):
        # 提取code请求参数
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseBadRequest('缺少code')
        # 创建oauth 对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 使用code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)
            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            log.error(e)
            return http.HttpResponseServerError('OAuth2.0认证失败')
        try:
            oauth_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果openid没有绑定用户,加密access_token
            access_token = generate_access_token(openid)
            context = {'access_token_openid': access_token.decode()}
            return render(request, 'oauth_callback.html', context)
        # 如果openid已绑定用户
        # 登录
        # log.info("user=%s" % oauth_user.user.username)
        login(request, oauth_user.user)
        # 响应结果
        next_url = request.GET.get("next")
        # 页面跳转
        response = redirect(next_url)
        # 状态保持
        response.set_cookie('username', oauth_user.user.username, settings.SESSION_COOKIE_AGE)
        return response

    def post(self, request):
        """用户绑定openid"""
        # 接收参数
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        sms_code_client = request.POST.get('sms_code')
        access_token = request.POST.get('access_token_openid')
        # 判断参数是否齐全
        if not all([mobile, password, sms_code_client, access_token]):
            # log.info("缺少必传参数")
            return http.HttpResponseBadRequest('缺少必传参数')
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            # log.info("请输入正确的手机号码")
            return http.HttpResponseBadRequest('请输入正确的手机号码')
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            # log.info("请输入8-20位的密码")
            return http.HttpResponseBadRequest('请输入8-20位的密码')
        # 判断短信验证码是否一致
        redis_conn = get_redis_connection('verifications')
        sms_code_server = redis_conn.get('sms_code_%s' % mobile)
        if sms_code_server is None:
            # log.info('无效的短信验证码.')
            return render(request, 'oauth_callback.html', {'msg': '无效的短信验证码'})
        if sms_code_client != sms_code_server.decode():
            # log.info('输入短信验证码有误.')
            return render(request, 'oauth_callback.html', {'msg': '输入短信验证码有误'})
        # 判断openid是否有效
        # log.info("access_token=%s" % access_token)
        openid = check_access_token(access_token)
        # log.info("openid=%s" % openid)
        if not openid:
            # log.info('无效的openid.')
            return render(request, 'oauth_callback.html', {'msg': '无效的openid'})
        # 保存注册数据
        try:
            user = UserInfo.objects.get(mobile=mobile)
        except UserInfo.DoesNotExist:
            # 不存在，则创建新用户
            try:
                user = UserInfo.objects.create_user(username=mobile, mobile=mobile, password=password)
            except Exception as e:
                log.error("创建用户失败%s" % e)
                return render(request, 'oauth_callback.html', {'msg': '创建用户失败.'})
        else:
            if not user.check_password(password):
                # log.info('密码错误.')
                return render(request, 'oauth_callback.html', {'msg': '密码错误.'})
        # 将用户绑定openid
        try:
            OAuthQQUser.objects.create(user=user, openid=openid)
        except Exception as e:
            log.error("QQ登录失败%s" % e)
            return render(request, 'oauth_callback.html', {'msg': 'QQ登录失败.'})
        # 实现状态保持
        login(request, user)
        # 响应绑定结果
        state = request.GET.get('state')
        # 页面跳转
        response = redirect(state)
        # 写入cookie
        response.set_cookie('username', user.username, settings.SESSION_COOKIE_AGE)
        return response
