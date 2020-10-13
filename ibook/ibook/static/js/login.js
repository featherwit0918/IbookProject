const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: "",
        password: "",

        error_username: false,
        error_password: false,
        remembered: false,
    },
    methods: {
        // 检查账号
        check_username() {
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if (re.test(this.username)) {
                this.error_username = false;
            } else {
                this.error_username = true;
            }
        },
        // 检查密码
        check_password() {
            let re = /^[0-9a-zA-Z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 表单提交
        on_submit() {
            this.check_username();
            this.check_password();

            if (this.error_username == true || this.error_password == true) {
                // 不满足登录条件: 禁用表单
                window.event.returnValue = false
            }
        }
    }
});