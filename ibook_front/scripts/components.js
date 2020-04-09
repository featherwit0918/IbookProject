const Iheader = {
    data: function () {
        return {

        }
    },
    template: `
        
    `
}

const Ifooter = {
    data: function () {
        return {
            list: [
                {
                    url: 'index.html',
                    icon: 'fa-home',
                    title: '首页'
                },

                {
                    url: 'bookshelf.html',
                    icon: 'fa-book',
                    title: '书架'
                },
                {
                    url: 'category.html',
                    icon: 'fa-bars',
                    title: '分类'
                },
                {
                    url: 'mine.html',
                    icon: 'fa-user',
                    title: '我的'
                }
            ]
        }
    },
    methods: {
        navToPage(url = null){
            if(url)
                location.href = url
        }
    },
    template: `
        <div class="footer-items">
            <div class="item" v-for="item in list" @click="navToPage(item.url)">
                <span class="icon fa" :class="[item.icon]"></span>
                <div class="title">
                    {{item.title}}
                </div>
            </div>
        </div>
    `
}

const Isearch = {
    template: `
        <div class="search">
            <input class="inputSearch" placeholder="请输入书名或作者名" v-model="keyword" />
            <span class="cancel" @click="search">搜索</span>
        </div>
    `,
    data: function () {
        return {
            keyword: ''
        }
    },
    methods: {
        search(){
            this.$emit('search', this.keyword)
        }
    },

}