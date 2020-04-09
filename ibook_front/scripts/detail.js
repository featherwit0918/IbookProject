const app = new Vue({
    data: {
        isShowMenu: 0,
        isShowContents: 0,
        isNight: 0,
        isShowScreenBg: 0,
        isShowSetting: 0,
        setting: {
            fontSize: 18,
            backgroundColor: 'default',
            colorList: ['brown', 'cyan-blue', 'default', 'pink', 'night']
        },
        contents: [
            
        ]
    },
    methods: {
        switchMenu(){
            app.isShowMenu = 1 - app.isShowMenu
        },
        switchMode(){
            app.isNight = 1 - app.isNight
            app.isShowMenu = 0
        },
        showContents(){
            app.isShowContents = 1
            app.isShowScreenBg = 1
            app.isShowMenu = 0
        },
        switchBackgroundColor(color){
            if(color){
                app.setting.backgroundColor = color
            }
        },
        incFontSize(){
            if(app.setting.fontSize < 30)
                app.setting.fontSize = app.setting.fontSize + 1
        },
        redFontSize(){
            if(app.setting.fontSize > 10)
                app.setting.fontSize = app.setting.fontSize - 1
        },
        showSetting(){
            app.isShowSetting = 1
            app.isShowMenu = 0
        },
        closeSetting(){
            app.isShowSetting = 0
        },
        close(){
            app.isShowMenu = 0
            app.isShowContents = 0
            app.isShowScreenBg = 0
        }
    },
    components: {

    }
}).$mount('#app')
// document.getElementById("contents").addEventListener('DOMMouseScroll',function(event){console.log(event)
//     event.stopPropagation();
// },false);