from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

from sms import sms_sington
from authenticate import generate_email_verify


@shared_task(name="send_sms_code")
def send_sms_code(tid, mobile, datas):
    response = sms_sington.send_sms(tid=tid, mobile=mobile, datas=datas)
    return response


@shared_task(name="send_email_verify")
def send_email_verify(email, user_id):
    # 生成邮箱激活链接
    email_verify_url = generate_email_verify(email, user_id)
    # 发送邮箱
    subject = "lg商城邮箱验证"
    html_message = "<p>尊敬的用户您好，感谢您使用商城。</p>" \
                   "<p>您的邮箱为：%s，请点击链接激活您的邮箱：</p>" \
                   "<p><a href='%s'>%s<a></p>" % (email, email_verify_url, email_verify_url)
    response = send_mail(subject, "", from_email=settings.EMAIL_FROM, recipient_list=[email], html_message=html_message)
    return response
