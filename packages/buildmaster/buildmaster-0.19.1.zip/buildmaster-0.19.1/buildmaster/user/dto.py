# encoding=utf8
from flask_restplus import fields
from ..app import api, app

USER_CAPTCHA_ENABLED = app.config['USER_CAPTCHA_ENABLED']

user_create = api.model('User to create', {
    'username': fields.String(description=r"指定用户名，最多包含64个字符。格式：^[a-zA-Z0-9\.@\-_]+$", required=True),
    'email': fields.String(description=r"用户电子邮箱"),
    'password': fields.String(description="账号密码"),
    'mobile': fields.String(description=r"用户手机号。格式：国际区号-号码"),
    'displayName': fields.String(description=r"显示名称，最多包含128个字符或汉字。格式：^[a-zA-Z0-9\.@\-\u4e00-\u9fa5]+$"),
    'comments': fields.String(description=r"备注，最大长度128个字符"),
})

user_update = api.model('User to update', {
    'username': fields.String(description=r"指定用户名，最多包含64个字符。格式：^[a-zA-Z0-9\.@\-_]+$", required=True),
    'email': fields.String(description=r"用户电子邮箱"),
    'mobile': fields.String(description=r"用户手机号。格式：国际区号-号码"),
    'displayName': fields.String(description=r"显示名称，最多包含128个字符或汉字。格式：^[a-zA-Z0-9\.@\-\u4e00-\u9fa5]+$"),
    'comments': fields.String(description=r"备注，最大长度128个字符"),
    'isActive': fields.Integer(description='启用/禁用账号')
})

user_login_dict = {
    'username': fields.String(description=r"指定用户名，最多包含64个字符。格式：^[a-zA-Z0-9\.@\-_]+$", required=True),
    'password': fields.String(description="用户密码")
}
if USER_CAPTCHA_ENABLED:
    user_login_dict['captcha'] = fields.String(description="图片验证码")
user_login = api.model('User login', user_login_dict)


user_register = api.model('User register', {
    'username': fields.String(description=r"指定用户名，最多包含64个字符。格式：^[a-zA-Z0-9\.@\-_]+$", required=True),
    'password': fields.String(description="用户密码"),
    'mobile': fields.String(description="手机号码"),
    'email': fields.String(description="邮箱地址"),
    'sms_captcha': fields.String(description="短信验证码"),
    'org_code': fields.String(description="组织 code，可选"),
})

user_login_by_mobile = api.model('User login by mobile', {
    'mobile': fields.String(description=r"手机号 格式：^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$",
                            required=True),
    'sms_captcha': fields.String(description="短信验证码"),
    'org_code': fields.String(description="组织code，可选"),
})

verify_captcha = api.model('Verify img captcha', {
    'captcha': fields.String(description="图片验证码")
})

reset_password = api.model('reset_password', {
    'mobile': fields.String(description=r"手机号 格式：^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$",
                            required=True),
    'password': fields.String(description="用户密码"),
    'sms_captcha': fields.String(description="短信验证码")
})

recover_password = api.model("recover_password", {
    'password': fields.String(description="密码", required=True),
    'id': fields.String(description="用户id")
})

delete_user = api.model("delete_user", {
    'id': fields.String(description="用户id")
})
