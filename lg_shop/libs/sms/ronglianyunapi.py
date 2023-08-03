import json

from django.conf import settings
from django.http import JsonResponse

from ronglian_sms_sdk import SmsSDK
from logger import log


def send_sms(mobile, datas, tid=1):
    """
    发送短信
    @params tid: 模板ID，默认测试使用1
    @params mobile: 接收短信的手机号，多个手机号使用逗号隔开
            单个号码： mobile="13312345678"
            多个号码： mobile="13312345678,13312345679,...."
    @params datas: 短信模板的参数列表(测试只能发四位验证码)
            例如短信模板为： 【云通讯】您的验证码是{1}，请于{2}分钟内正确输入。
            则datas=("1234",5,)
    """
    ronglianyun = settings.RONGLIANYUN
    sdk = SmsSDK(ronglianyun.get("accId"), ronglianyun.get("accToken"), ronglianyun.get("appId"))
    resp = sdk.sendMessage(tid, mobile, datas)
    response = json.loads(resp)
    if response.get("statusCode") == "000000":
        return JsonResponse({"code": 0, "messages": f"{mobile}验证码发送成功"})
    msg = {"code": 1002, "messages": f"{mobile}验证码发送失败-{response.get('statusMsg')}"}
    log.error(msg)
    return JsonResponse(msg)
