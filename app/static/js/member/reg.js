;
var member_reg_ops = {

    init: function () {
        this.eventBind();
    },

    eventBind: function () {
        $(".reg_wrap .do-reg").click(function () {
            // alert('1');
            var btn_target = $(this);
            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理");
                return;
            }
            var login_name = $(".reg_wrap input[name=login_name]").val();
            var login_pwd = $(".reg_wrap input[name=login_pwd]").val();
            var login_pwd2 = $(".reg_wrap input[name=login_pwd2]").val();
            if (login_name == undefined || login_name.length < 1) {
                common_ops.alert("请输入正确的用户名");
                return;
            }

            if (login_pwd == undefined || login_pwd.length < 6) {
                common_ops.alert("密码不小于6位");
                return;
            }

            if (login_pwd2 == undefined || login_pwd2 != login_pwd) {
                common_ops.alert("两次密码输入不一致");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                // url:"/member/reg",
                url:common_ops.bulidUrl("/reg"),
                type:"POST",
                data:{
                    login_name:login_name,
                    login_pwd:login_pwd,
                    login_pwd2:login_pwd2
                },
                dataType:'json',
                success:function (res){
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code === 200){

                        callback = function (){
                            window.location.href =common_ops.bulidUrl("/");
                        };

                    }
                    common_ops.alert(res.msg,callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    member_reg_ops.init();
});