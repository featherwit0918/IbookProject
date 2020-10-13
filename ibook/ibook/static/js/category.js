const app = new Vue({
    el: "#app",
    delimiters: ['[[', ']]'],
    data: {
        isActive: true,
        category_info: [],
    },
    methods: {
        clickMan() {
            this.isActive = true;
            let url = 'http://192.168.38.20:8000/category/1';
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    this.category_info = response.data.data
                })
                .catch(error => {
                    console.log(error)
                })
        },
        clickWoman() {
            this.isActive = false;
            let url = 'http://192.168.38.20:8000/category/2';
            axios.get(url, {
                responseType: 'json'
            })
                .then(response => {
                    this.category_info = response.data.data
                })
                .catch(error => {
                    console.log(error)
                })
        }
    },
    created() {
        let url = 'http://192.168.38.20:8000/category/1';
        axios.get(url, {
            responseType: 'json'
        })
            .then(response => {
                this.category_info = response.data.data
            })
            .catch(error => {
                console.log(error)
            })
    }

});