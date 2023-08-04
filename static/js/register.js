let vm = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],// 修改vue的模板语法
    data: {
        // v-model
        username: "",
        password: "",
        confirm_password: "",
        mobile: "",
        allow: "",
        image_code_url: "",
        image_code: "",
        uuid: "",
        sms_code: "",
        sms_code_tip: "获取短信验证码",

        // v-show
        error_username: false,
        error_password: false,
        error_confirm_password: false,
        error_mobile: false,
        error_allow: false,
        error_code: false,
        error_sms_code: false,

        // error-message
        error_username_msg: "",
        error_password_msg: "",
        error_confirm_password_msg: "",
        error_mobile_msg: "",
        error_allow_msg: "",
        error_code_msg: "",
        error_sms_code_msg: "",
    },
    methods: {
        check_username() {
            let re = /^[0-9a-zA-Z_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username = true;
                this.error_username_msg = "请输入5-20个字符的用户";
            }

            if (this.error_username === false) {
                let url = `/api/users/check/${this.username}/`;
                axios.get(url, {
                    responseType: "json"
                }).then(response => {
                    if (response.data.count === 0) {
                        this.error_username = false;
                        this.error_username_msg = "";
                    } else {
                        this.error_username = true;
                        this.error_username_msg = "用户名已存在.";
                    }
                })
            }

        },
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
                this.error_password_msg = "请输入8-20位的密码"
            }
        },
        check_confirm_password() {
            if (this.password !== this.confirm_password) {
                this.error_confirm_password = true;
                this.error_confirm_password_msg = "两次输入的密码不一致"
            } else {
                this.error_confirm_password = false;
            }
        },
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile = true;
                this.error_mobile_msg = "请输入正确的手机号码";
            }

            if (this.error_mobile === false) {
                let url = `/api/verify/mobile/${this.mobile}/`;
                axios.get(url, {
                    responseType: "json"
                }).then(response => {
                    if (response.data.count === 0) {
                        this.error_mobile = false;
                        this.error_mobile_msg = "";
                    } else {
                        this.error_mobile = true;
                        this.error_mobile_msg = "手机号已注册.";
                    }
                })
            }
        },
        check_allow() {
            if (this.error_allow === true) {
                this.error_allow = false;
                this.error_allow_msg = "";
            } else {
                this.error_allow = true;
                this.error_allow_msg = "请勾选用户协议";
            }
        },
        generate_verify_code() {
            this.uuid = generateUUID();
            this.image_code_url = `/api/verify/code/${this.uuid}/`;
        },
        check_image_code() {
            if (this.image_code.length === 4) {
                this.error_code = false;
                this.error_code_msg = "";
            } else {
                this.error_code = true;
                this.error_code_msg = "请正确填写图形验证码";
            }
        },
        check_sms_code() {
            if (this.sms_code.length === 4) {
                this.error_sms_code = false;
                this.error_sms_code_msg = "";
            } else {
                this.error_sms_code = true;
                this.error_sms_code_msg = "请正确填写短信验证码";
            }
        },
        send_sms_code() {
            this.check_mobile();
            this.check_sms_code();
            let url = `/api/verify/sms/${this.mobile}/?uuid=${this.uuid}&image_code=${this.image_code}`;
            axios.get(url, {}).then(response => {
                if (response.data.code === 0) {
                    let num = 60;
                    let t = setInterval(() => {
                        if (num === 1) {
                            clearInterval(t);
                            this.sms_code_tip = `获取短信验证码`;
                        } else {
                            num -= 1;
                            this.sms_code_tip = `${num}秒`;
                        }
                    }, 1000)
                } else {
                    this.error_sms_code = true;
                    this.error_sms_code_msg = response.data.msg;
                }
            }).catch(errors => {
                console.log(errors);
            })
        },
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_confirm_password();
            this.check_mobile();
            this.check_allow();
            this.check_image_code();
            this.check_sms_code();
            if (this.error_username === true || this.error_password === true || this.error_confirm_password === true || this.error_mobile === true || this.error_allow === true) {
                // 禁止默认表单提交
                window.event.returnValue = false;
            }
        },
    },
    // 页面加载之后执行的方法
    mounted() {
        this.generate_verify_code();
    }
})