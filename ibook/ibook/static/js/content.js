const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        show_sort: true,
        book_id: book_id,
        base_url: 'http://192.168.38.20:8000/directory/',
        sort_field: "id",
        chapter_list: [],
        show_above: false,
        chapter_id: chapter_id,
    },
    methods: {
        changeSort() {
            var _this = this;
            this.show_sort = !this.show_sort;
            if (this.show_sort) {
                this.sort_field = 'id'
            } else {
                this.sort_field = '-id'
            }
            let url = this.base_url + this.book_id + '/' + this.sort_field;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    _this.chapter_list = response.data.data
                })
                .catch(error => {
                    console.log(error.response);
                })
        },
        clickFollow () {
            this.show_above = !this.show_above
        }
    },
    created() {
        var _this = this;
        let url = this.base_url + this.book_id + '/' + this.sort_field;
        axios.get(url, {
            responseType: 'json'
        })
            .then(response => {
                _this.chapter_list = response.data.data
            })
            .catch(error => {
                console.log(error.response);
            });
        let readschedule_url = 'http://192.168.38.20:8000/readschedule/' + this.book_id + '/';
        axios.post(readschedule_url, {
            responseType: 'json',
            chapter_id: this.chapter_id,
        })
            .then(response => {
                console.log(response.data)
            })
            .catch(error => {
                console.log(error)
            })
    }
});