from django import forms

from .models import UserInfo


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True, label="用户名", error_messages={
        "max_length": "用户名最大长度为20",
        "min_length": "用户名最小长度为5",
        "required": "用户名不能为空"
    })
    password = forms.CharField(max_length=20, min_length=8, required=True, label="密码", error_messages={
        "max_length": "密码最大长度为20",
        "min_length": "密码最小长度为8",
        "required": "密码不能为空"
    })
    confirm_password = forms.CharField(max_length=20, min_length=8, required=True, label="确认密码", error_messages={
        "max_length": "密码最大长度为20",
        "min_length": "密码最小长度为8",
        "required": "密码不能为空"
    })
    mobile = forms.CharField(max_length=11, min_length=11, required=True, label="手机号", error_messages={
        "max_length": "手机号格式为11位",
        "min_length": "手机号格式为11位",
        "required": "手机号不能为空"
    })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = UserInfo.objects.get(username=username)
            if user:
                self.add_error("username", "用户名已存在.")
        except Exception as e:
            return username

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("password", "两次密码输入不同.")
        return self.cleaned_data
