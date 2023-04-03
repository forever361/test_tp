;
var member_login_ops = {

    init: function () {
        this.eventBind();
    },

    eventBind: function () {
        $(".login_wrap .do-login").click(function () {
//             alert('1');
            var btn_target = $(this);
            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理");
                return;
            }
            var login_name = $(".login_wrap input[name=login_name]").val();
            var login_pwd = $(".login_wrap input[name=login_pwd]").val();

            if (login_name == undefined || login_name.length < 1) {
                common_ops.alert("请输入正确的用户名");
                return;
            }

            if (login_pwd == undefined || login_pwd.length < 6) {
                common_ops.alert("密码不小于6位");
//                alert("密码不小于6位");
                return;
            }

            // 突破了上面两条限制，才能发ajax的post请求

            btn_target.addClass("disabled");
            $.ajax({
                // url:"/member/reg",
                url:common_ops.bulidUrl("/login"),
                type:"POST",
                data:{
                    login_name:login_name,
                    login_pwd:login_pwd,
                },
                dataType:'json',
                success:function (login){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (login.code === 200){

                        callback = function (){
                            window.location.href =common_ops.bulidUrl("/");
                        };

                    }
                     common_ops.alert(login.msg,callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    member_login_ops.init();
});