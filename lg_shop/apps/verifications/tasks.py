from celery import shared_task

from sms import sms_sington


@shared_task(name="send_sms_code")
def send_sms_code(tid, mobile, datas):
    response = sms_sington.send_sms(tid=tid, mobile=mobile, datas=datas)
    return response
