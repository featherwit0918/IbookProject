const app = new Vue({
    data: {
        catelist:[
            {
                img: '',
                title: '都市小说',
                detail: '生活 / 异能/ 江湖 / 热血 / 美女'
            }
        ],
        cateType: 1
    },
    methods: {
        goToSearch(){
            location.href = 'search.html'
        },
        /*
         * 根据性别获取数据
         */
        getData(cateType = 1){

            app.cateType = 1 - app.cateType

        }
    },
    components: {
        Ifooter
    }
}).$mount('#app')