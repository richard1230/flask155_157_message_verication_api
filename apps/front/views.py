from flask import (
    Blueprint,
    views,
    render_template,
    make_response,
    Response,
    Flask,
    request

)
from utils.captcha import Captcha
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
from utils.CCPSDK import CCPRestSDK
from utils import restful
import config

bp = Blueprint("front", __name__)  # url_prefix='cms'表示一个前缀,这里不需要


@bp.route('/')
def index():
    return 'front index'


@bp.route('/captcha/')
def graph_captcha():
    text, image = Captcha.gene_graph_captcha()
    out = BytesIO()
    # with open("{}.png".format(image),'rb') as f:
    #     image = f.read()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    # print(resp)
    # resp = Response(resp,mimetype="image/png")
    # resp.context_type = 'image/png'
    resp.headers['Content-Type'] = 'image/jpg'

    return resp

@bp.route('/sms_captcha/')
def sms_captcha():
    telephone=request.args.get('telephone')
    if not telephone:
        return restful.params_error(message='请传入手机号码')
    accountSid = "8a216da86f17653b016f3b4046b218ab"
    accountToken = "ac156972012a43dab1782f1f89995ac9"
    appId = "8a216da86f17653b016f3b40471818b2"
    rest = CCPRestSDK.REST(accountSid, accountToken, appId)
    #下面要有产生随机的验证码函数
    captcha= Captcha.gene_text(number=4)
    result = rest.sendTemplateSMS(telephone, [captcha], "1")
    if result:
        return restful.success()
    else:
        return restful.params_error(message='短信验证码发送失败')



class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')

##155课时(没有按照flask的来)，这里是测试代码
class SMSCodeView(views.MethodView):
    def get(self):
        #/smscode?tel=xxxxx
        telephone = request.args.get("tel")
        # telephone = request.values.get("tel")
        accountSid="8a216da86f17653b016f3b4046b218ab"
        accountToken = "ac156972012a43dab1782f1f89995ac9"
        appId ="8a216da86f17653b016f3b40471818b2"
        rest = CCPRestSDK.REST(accountSid,accountToken,appId)
        captcha = Captcha.gene_text(number=4)
        result = rest.sendTemplateSMS(telephone, [captcha], "1")
        # result= rest.sendTemplateSMS(telephone,["1234"],"1")
        print(result)
        return Response("success")






bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/smscode/',view_func=SMSCodeView.as_view('smscode'))
