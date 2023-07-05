;
var common_ops ={
    bulidUrl:function(path,params){
        var  url = "" + path;
        var _params_url = "";
        if(params){
            _params_url = object.keys(params).map(function (k){
                return [encodeURIComponent(k),encodeURIComponent(params[k])].join("=");
            }).join("&");
            _params_url ="?"+_params_url;
        }
        return url + _params_url;
    },

     alert:function (msg,cb){
        layer.alert(msg,{
            yes:function (index){
                if (typeof cb === "function"){
                    cb();
                }
                layer.close(index);
            }
        });
    }
};