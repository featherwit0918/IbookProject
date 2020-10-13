const app = new Vue({

    el: '#app',
    data() {
        return {
            sex: '',
        }
    },

    methods: {
        onSexClick(sex) {
            this.sex = sex
        },
        on_submit() {
          if (this.sex == '') {
               window.event.returnValue = false
          }
        }
    },

});