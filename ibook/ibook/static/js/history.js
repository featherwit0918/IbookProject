const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        books: [],
        show_books: false,
    },
    methods: {
        clearBook() {
            let url = '/book_histories/';
            axios.delete(url, {
                responseType: 'json'
            })
                .then(response => {
                    this.show_books = false
                })
        },
        addToBookShelf(id) {
            axios('/addbookcase/' + id).then(res => {
                alert(res.data.errmsg)
            })
        }
    },
    created() {
        let url = '/book_histories/';
        axios.get(url, {
            responseType: 'json'
        })
            .then(response => {
                if (response.data.code) {
                    this.show_books = false
                } else {
                    console.log(response.data);
                    this.books = response.data.data;
                    this.show_books = true
                }
            })
            .catch(error => {
                console.log(error)
            })
    }
});