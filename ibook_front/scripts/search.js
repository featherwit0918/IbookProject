const app = new Vue({
    data: {
        searchComplete: 0,
        hotSearchData: [
            {
                hot: 1,
                name: '极品群芳谱',
            },
            {
                hot: 1,
                name: '都市逍遥邪帝',
            },
            {
                hot: 0,
                name: '风落九天',
            },
            {
                hot: 0,
                name: '风落九天',
            }
        ],
        booklist: [
            {
                img: '',
                name: '疯狂农民工',
                description: '去玩儿推分工会尽快分工会尽快腿分工会尽快去玩儿推分工会尽',
                author: '谭更好健康',
                isend: 1,
                tagname: '都市小说'
            }
        ],
        recommendlist: [
            {
                img: '',
                name: '疯狂农民工',
                description: '去玩儿推分工会尽快分工会尽快腿分工会尽快去玩儿推分工会尽',
                author: '谭更好健康',
                isend: 1,
                tagname: '都市小说'
            }
        ]
    },
    methods: {
        search(keyword){
            if(keyword){
                app.searchComplete = 1

            }
            else{
                app.searchComplete = 0
            }
        },
    },
    components: {
        Ifooter,
        Isearch
    }
}).$mount('#app')