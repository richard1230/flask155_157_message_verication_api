
 $(function(){
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = zlparam.setParam(src,'xx',Math.random());
        self.attr('src',newsrc);
    });
});


$(function () {
    $("#sms-captcha-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);//self代表这个按钮
        var telephone = $("input[name='telephone']").val();
        if(!(/^1[345879]\d{9}$/.test(telephone))){
            zlalert.alertInfoToast('请输入正确的手机号码！');
            return;
        }


        zlajax.get(
            {
                // 'url':'/front/sms_captcha?telephone='+telephone,
                'url': '/sms_captcha?telephone=' + telephone,

                'success': function (data) {
                    console.log(data);
                    if (data['code'] == 200) {
                        zlalert.alertSuccessToast('短信验证码发送成功！');
                        self.attr("disabled", 'disabled');
                        var timeCount = 60;
                        var timer = setInterval(function () {
                            timeCount--;
                            self.text(timeCount);
                            if (timeCount <= 0) {
                                self.removeAttr('disabled');
                                clearInterval(timer)
                                self.text('发送验证码 ')
                            }
                        }, 1000);
                    } else {
                        zlalert.alertInfoToast(data['message']);
                    }
                }

            });

        // var timestamp = (new Date).getTime();
        // var sign = md5(timestamp+telephone+"q3423805gdflvbdfvhsdoa`#$%");
        // zlajax.post({
        //     // 'url': '/c/sms_captcha/',
        //
        //     'url': '/sms_captcha/',
        //     'data':{
        //         'telephone': telephone,
        //         'timestamp': timestamp,
        //         'sign': sign
        //     },
        //     'success': function (data) {
        //         if(data['code'] == 200){
        //             zlalert.alertSuccessToast('短信验证码发送成功！');
        //             self.attr("disabled",'disabled');
        //             var timeCount = 60;
        //             var timer = setInterval(function () {
        //                 timeCount--;
        //                 self.text(timeCount);
        //                 if(timeCount <= 0){
        //                     self.removeAttr('disabled');
        //                     clearInterval(timer);
        //                     self.text('发送验证码');
        //                 }
        //             },1000);
        //         }else{
        //             zlalert.alertInfoToast(data['message']);
        //         }
        //     }
        // });
    });
});