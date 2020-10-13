const app = new Vue({
    el: "#app",  // 通过ID选择器找到绑定的HTML内容
    delimiters: ['[[', ']]'], // 修改Vue读取变量的语法
    data: { // 数据对象
        // v-model
        username: '',
        password: '',
        password2: '',
        mobile: '',
        sms_code_tip: '获取短信验证码',
        sms_code: '',
        send_flag: false,

        // v-show
        error_name: false,
        error_password: false,
        error_password2: false,
        error_mobile: false,
        error_sms_code: false,


        // error_message
        error_name_message: "",
        error_mobile_message: '',
        error_sms_code_message: "",
    },
    methods: { // 定义和实现事件的方法
        // 发送短信验证码
        send_sms_code() {
            // 避免恶意用户频繁的点击获取短信验证码的标签
            if (this.send_flag == true) { // 如果为true, 则证明已经获取过一次, 且没有超过60秒
                return;
            }
            this.send_flag = true; // 如果在60秒内被点击, 则设置为true

            // 校验数据
            this.check_mobile();
            if (this.error_mobile == true) {
                this.send_flag = false;
                return;
            }

            let url = '/sms_codes/' + this.mobile;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    if (response.data.err_code == '0') {
                        // 展示60秒倒计时效果
                        let num = 60;
                        let t = setInterval(() => {
                            if (num == 1) { // 倒计时即将结束
                                clearInterval(t); // 停止回调函数执行
                                this.sms_code_tip = '获取短信验证码'  // 还原sms_code_tip的提示文字
                                this.send_flag = false;
                            } else { // 正在倒计时
                                num -= 1;
                                this.sms_code_tip = num + '秒';
                            }
                        }, 1000)
                    } else {
                        this.error_sms_code_message = response.data.errmsg;
                        this.error_sms_code = true;
                        this.send_flag = false;
                    }
                })
        },
        // 校验用户名
        check_username() {
            // 用户名是5-20个字符, [a-zA-Z0-9]
            // 定义正则
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            // 使用正则匹配用户名数据
            if (re.test(this.username)) {
                // 匹配成功, 不展示错误信息
                this.error_name = false;
            } else {
                // 匹配失败, 展示错误提示信息
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }

            // 判断用户名是否重复
            if (this.error_name == false) { // 只有当用户输入的用户名满足条件时才会去判断
                let url = '/usernames/' + this.username + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            // 用户名已存在
                            this.error_name_message = '用户名已存在';
                            this.error_name = true
                        } else {
                            // 用户名不存在
                            this.error_name = false
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        // 校验密码
        check_password() {
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        // 校验确认密码
        check_password2() {
            if (this.password != this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },
        // 校验手机号
        check_mobile() {
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }

            // 判断手机号是否重复注册
            if (this.error_mobile == false) {
                let url = '/mobiles/' + this.mobile + '/count/';
                axios.get(url, {
                    responseType: 'json'
                })
                    .then(response => {
                        if (response.data.count == 1) {
                            this.error_mobile_message = '手机号已存在';
                            this.error_mobile = true
                        } else {
                            this.error_mobile = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response);
                    })
            }
        },
        // 校验短信验证码
        check_sms_code() {
            if (this.sms_code.length != 6) {
                this.error_sms_code_message = '请填写短信验证码';
                this.error_sms_code = true
            } else {
                this.error_sms_code = false;
            }
        },
        // 监听表单提交事件
        on_submit() {
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_sms_code();

            // 在校验之后, 注册数据中, 只要有错误, 就禁用掉表单的提交事件
            if (this.error_name == true || this.error_password == true || this.error_password2 == true || this.error_mobile == true || this.error_sms_code == true) {
                // 禁用掉表单提交事件
                window.event.returnValue = false;
            }
        }
    }
});