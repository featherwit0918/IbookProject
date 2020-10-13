const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        like_books: [],
        category_id: category_id,
        book_id: book_id,
    },
    methods: {
        addBookcase() {
            let url = '/addbookcase/' + this.book_id;
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    alert(response.data.errmsg);
                })
                .catch(error => {
                    console.log(error)
                })
        }
    },
    created() {
        let url = '/like/book/' + this.category_id;
        axios.get(url, {
            responseType: 'json'
        })
            .then(response => {
                this.like_books = response.data.data
            })
            .catch(error => {
                console.log(error)
            });
        let history_url = '/book_histories/';
        axios.post(history_url, {
            book_id: book_id
        })
            .then(response => {
                console.log(response.data)
            })
            .catch(error => {
                console.log(error)
            });
    }
});