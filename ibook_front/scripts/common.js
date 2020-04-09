document.write(`<link rel="stylesheet" href="https://meyerweb.com/eric/tools/css/reset/reset200802.css">`);
document.write(`<link rel="stylesheet" href="https://cdn.bootcss.com/twitter-bootstrap/4.3.1/css/bootstrap.min.css">`);
document.write(`<link rel="stylesheet" href="https://cdn.bootcss.com/font-awesome/4.7.0/css/font-awesome.min.css">`);

// document.write(`<script src='https://cdn.staticfile.org/popper.js/1.15.0/umd/popper.min.js'></script>`);
// document.write(`<script src='https://cdn.bootcss.com/twitter-bootstrap/4.3.1/js/bootstrap.min.js'></script>`);
document.write(`<script src='https://cdn.bootcss.com/moment.js/2.24.0/moment.min.js'></script>`);
document.write(`<script src='https://cdn.bootcss.com/vue/2.6.10/vue.min.js'></script>`);
// document.write(`<script src='https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js'></script>`);

document.write(`<script src='scripts/components.js'></script>`);

document.write(`<link rel="stylesheet" href="styles/reset.css">`);
document.write(`<link rel="stylesheet" href="styles/main.css">`);

;console.clear();

const Common = {
    type : function(v){return Object.prototype.toString.call(v).slice(8,-1).toLowerCase();},
    getParams(url = location.href){
        let res = null;
        if(this.type(url) === 'string'){
            let paramStrIdx = url.lastIndexOf('?');
            if(~paramStrIdx){
                res = {};
                let paramStr = url.slice(paramStrIdx+1);
                let paramArr = url.slice(paramStrIdx+1).split('&');
                paramArr.forEach(item => {
                    let s = item.split('=');
                    res[s[0]] = s[1];
                });
            }
        }
        return res;
    }
}
