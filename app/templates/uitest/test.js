


function getPublicFunctions2(){
     var cases = []
     $.ajax(
        {
          url: "/runtest_tanos",
          type: "post",
          dataType:"json",
          data:{"code":"code", "code1":"code1"},
          async : true,
          beforeSend:function()
          {
            $('#Report').hide();
            return true;
          },
          success:function(data)
          {
            if (data.msg == "run success!"){
                layer.msg(data.msg,{time:2000,
                        area:['380px','66px'],
                        offset:'rt',
                        anim:1,
                        skin:'lay-msg-bg-gr'
                                 });
            } else {
                    layer.msg(data.msg,{time:2000,
                        area:['380px','66px'],
                        offset:'rt',
                        anim:1,
                        skin:'lay-msg-bg'
                                 });
            }
            if(data.returncode==0){
                $('#Report').show();
            }
            cases= data.msg;

          },
          error:function()
          {
           layer.msg(data.msg,{time:2000,
                    area:['380px','66px'],
                    offset:'rt',
                    anim:1,
                    skin:'lay-msg-bg'
                             });
            setTimeout(stoptimer(),5000);
          },
          complete:function()
          {
            setTimeout(stoptimer(),5000);
          }
    });

    return cases;
}