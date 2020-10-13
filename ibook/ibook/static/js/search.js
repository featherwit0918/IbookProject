const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
    },
    methods: {
        addBookcase(book_id) {
            let url = '/addbookcase/' + book_id;
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
});