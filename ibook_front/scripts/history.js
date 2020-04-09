const app = new Vue({
    data: {
        booklist:[
            {
                img: '',
                name: '疯狂农民工',
                description: '去玩儿推分工会尽快分工会尽快腿分工会尽快去玩儿推分工会尽',
                author: '谭更好健康',
                isend: 1,
                tagname: '都市小说',
                time: '2019年05月22日 14:25:30'
            }
        ]
    },
    methods: {

    },
    components: {
        Ifooter
    }
}).$mount('#app')