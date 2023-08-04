import os
import json

from ronglian_sms_sdk import SmsSDK

RONGLIANYUN = {
    "accId": '2c94811c86c00e9b0186f2873a040afa',
    "accToken": os.environ.get("RONGLIANYUNACCTOKEN"),
    "appId": '2c94811c86c00e9b0186f2873b0d0b01',
    "reg_tid": 1,  # 注册短信验证码的模板ID
    "sms_expire": 60,  # 短信有效期，单位：秒(s)
    "sms_interval": 60,  # 短信发送的冷却时间，单位：秒(s)
}


class SMSSington:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls, *args, **kwargs)
            ronglianyun = RONGLIANYUN
            cls._instance.sms = SmsSDK(ronglianyun.get("accId"), ronglianyun.get("accToken"), ronglianyun.get("appId"))
        return cls._instance

    def send_sms(self, mobile, datas, tid=1):
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
        sdk = self._instance.sms
        resp = sdk.sendMessage(tid, mobile, datas)
        response = json.loads(resp)
        return response
