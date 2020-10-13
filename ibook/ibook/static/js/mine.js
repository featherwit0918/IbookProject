// 获取cookie
function getCookie(name) {
    let r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

const app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
        username: "",
    },
    created() {
        if(getCookie('username')) {
            this.username = getCookie('username')
        }else {
            this.username = '用户未登录'
        }
    }
});
