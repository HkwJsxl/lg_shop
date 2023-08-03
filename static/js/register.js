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

        // v-show
        error_username: false,
        error_password: false,
        error_confirm_password: false,
        error_mobile: false,
        error_allow: false,

        // error-message
        error_username_msg: "",
        error_password_msg: "",
        error_confirm_password_msg: "",
        error_mobile_msg: "",
        error_allow_msg: "",
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
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (!re.test(this.confirm_password) || this.password != this.confirm_password) {
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
        },
        check_allow() {
            if (this.error_allow !== true) {
                this.error_allow = true;
                this.error_allow_msg = "请勾选用户协议";
            }else{
                this.error_allow = false;
            }
        },
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_confirm_password();
            this.check_mobile();
            this.check_allow();
            if (this.error_username === true || this.error_password === true || this.error_confirm_password === true || this.error_mobile === true || this.error_allow === true) {
                // 禁止默认表单提交
                window.event.returnValue = false;
            }
        },
    }
})