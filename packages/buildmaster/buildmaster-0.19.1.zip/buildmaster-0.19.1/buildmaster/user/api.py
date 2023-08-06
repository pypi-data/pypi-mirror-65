# encoding=utf8

from datetime import datetime
from flask_restplus import Resource
from flask import request, after_this_request, session, send_file
from werkzeug.security import check_password_hash, generate_password_hash
import json

from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required,
    create_refresh_token,
    unset_jwt_cookies,
    decode_token
)

from ..app import (
    api, app, db, dbplus, Dict,
    auth_required, auth_user,
    set_access_cookies,
    set_refresh_cookies,
    JWT_ACCESS_COOKIE_NAME,
    JWT_REFRESH_COOKIE_NAME
)

from . import dto, utils
from ..log import log_action

ns = api.namespace(name='user', description="账户与权限管理")

escape = db.escape

USER_CAPTCHA_ENABLED = app.config['USER_CAPTCHA_ENABLED']


def login_user(user):
    del user.password  # 敏感信息不透传给客户端

    user.loginDate = datetime.now()

    with db.session() as s:
        s.execute(f"update _user set loginDate=:date where id=:id", date=datetime.now(), id=user.id)

    u = Dict({
        'id': user.id,
        'username': user.username,
        'defaultPage': user.defaultPage,
        'isActive': user.isActive,
        'mobile': user.mobile,
        'orgId': user.orgId
    })

    access_token = create_access_token(identity=u)
    refresh_token = create_refresh_token(identity=u)

    data = {
        'user': user,
        'token': {
            JWT_ACCESS_COOKIE_NAME: access_token,
            JWT_REFRESH_COOKIE_NAME: refresh_token
        }
    }

    @after_this_request
    def set_cookie(resp):
        # 设置标准cookie到响应头部，方便浏览器API直接登录验证
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    return data


@ns.route('/login')
class UserLogin(Resource):
    @log_action(action='login', with_secret=True)
    @api.expect(dto.user_login)
    def post(self):
        """用户登录"""
        data = Dict(request.json)

        if USER_CAPTCHA_ENABLED:
            if not session.get('captcha'):
                return {"message": '图片验证码已失效'}, 600

            if not session.get('captcha') == data['captcha']:
                return {'message': '图片验证码不正确'}, 600

        sql = f'''select _user.*,_org.defaultPage as "orgPage" from _user 
                left join _org on _user.orgId = _org.id where username=:username
              '''
        with db.session() as s:
            user = s.query_one(sql, username=data.username)
        if not user:
            return {'message': '用户不存在'}, 403
        if not user.password:
            return {'message': '用户密码未初始化'}, 403

        if not user.isActive:
            return {'message': '账户非激活状态，请联系管理员激活'}, 600

        if not check_password_hash(user.password, data.password):
            return {'message': '用户名或密码不正确'}, 600
        
        if not user['defaultPage']:
            user['defaultPage'] = user["orgPage"]
        return login_user(user)


@ns.route('/login_by_mobile')
class LoginByMobile(Resource):
    @log_action(action='login', with_secret=True)
    @api.expect(dto.user_login_by_mobile)
    def post(self):
        """
        手机号快捷登录同时注册
        依赖到了sms模块的中的表
        :return:
        """
        args = Dict(request.json)
        if not args.mobile:
            api.abort(400, "手机号必填")

        with db.session() as s:
            sql = f"""select * from sms_sent where 
            mobile=:mobile and captcha=:sms_captcha and template=:template and is_valid=1"""
            sms = s.query_one(sql, mobile=args.mobile, sms_captcha=args.sms_captcha, template="login")
            if not sms:
                return {'message': '短信验证码不正确'}, 600

            sms.is_valid = 0
            s.merge('sms_sent', sms)

        org = None

        domain = utils.get_host(request.headers)

        if args.org_code:
            sql = "select id from _org where code=:code "
            org = db.query_one(sql, code=args.org_code)

        if not org and domain:
            sql = "select id from _org where domain=:domain"
            org = db.query_one(sql, domain=domain)

        with db.session() as s:
            sql = """
                select * from _user where mobile=:mobile
            """
            user = s.query_one(sql, mobile=args.mobile)

        if not user:
            user = Dict({
                'username': args.mobile,
                'mobile': args.mobile,
                'displayName': args.mobile,
                'avatar': '/avatar.jpg',
                'defaultPage': 'dashboard',
                'isActive': 1,
                'createDate': datetime.now(),
                'updateDate': datetime.now(),
                'orgId': org.id if org else None
            })
            s.add('_user', user)

        return login_user(user)


@ns.route('/logout')
class UserLogout(Resource):
    def post(self):
        """用户登出"""

        @after_this_request
        def set_cookie(resp):
            unset_jwt_cookies(resp)
            return resp

        return {'logout': True}


@ns.route('/token_refresh')
class UserTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """用户TOKEN更新"""

        @after_this_request
        def set_cookie(resp):
            u = auth_user()
            access_token = create_access_token(identity=u)
            set_access_cookies(resp, access_token)
            return resp

        return {'refresh': True}


def filter_menus(menu, urls):
    if 'children' not in menu:
        if 'path' not in menu:
            return
        if menu['path'] in urls:
            return menu
        return

    children = []
    for m in menu['children']:
        res = filter_menus(m, urls)
        if res:
            children.append(res)
    if len(children) == 0:
        return
    menu['children'] = children
    return menu


def load_menu(user):
    sql = f"""
    SELECT _menu.* FROM _menu JOIN _user ON _menu.orgId=_user.orgId WHERE _user.id=:userId
    """
    res = db.query_one(sql, userId=user.id)
    if not res:
        return {'message': '用户无所属组织，请联系管理员处理'}, 404
    return json.loads(res['json']), 200


@ns.route('/info/<token>')
class UserInfo(Resource):
    @auth_required
    def get(self, token):
        """根据用户登录后的token获取用户信息"""

        t = decode_token(token)
        sql = f"""
        select _user.*, _org.defaultPage, _org.name as "orgName"
        from _user left join _org on _user.orgId = _org.id where _user.id = :id
        """
        with db.session() as s:
            user = s.query_one(sql, id=t['identity']['id'])
            if not user:
                return {'message': f"用户({t['identity']['username']})不存在"}, 404

            del user.password
            user.aclFunc = dbplus.acl_func(user.id, resource_type='func')

        menus, status = load_menu(user)
        if status != 200:
            return menus, status
        acl_func = dbplus.acl_func(user.id, resource_type='menu')
        urls = set([f['resource'] for f in acl_func if f['resource']])
        menu_list = []
        for m in menus:
            m2 = filter_menus(m, urls)
            if m2:
                menu_list.append(m2)
        user.menus = menu_list
        if not user.menus:
            return {'message': '账户无任何菜单权限，请联系管理员添加角色、菜单'}, 403
        return user


@ns.route('/create')
class UserCreate(Resource):
    @auth_required
    @log_action(with_secret=True)
    @api.expect(dto.user_create)
    def post(self):
        """创建账户"""
        u = auth_user()
        args = Dict(request.json)
        args.password = args.password if args.password else "123456"
        if not args.username:
            api.abort(400, "用户名必填")
        if not utils.check_password(args.password):
            api.abort(400, "密码长度至少为6个字符")
        args.password = generate_password_hash(args.password)
        sql = "select id from _user where username=:username"
        user_db = db.query_one(sql, username=args.username)

        if user_db:
            return {'message': f'用户名 {args.username} 已经存在'}, 600

        sql = "select id from _user where mobile=:mobile"
        user_db = db.query_one(sql, mobile=args.mobile)
        if user_db:
            return {'message': f'手机号 {args.mobile} 已经存在'}, 600

        user_db = dbplus.create(u, '_user', args)[0]
        del user_db['password']
        return user_db


@ns.route('/update')
class UserUpdate(Resource):
    @auth_required
    @log_action(with_secret=True)
    @api.expect(dto.user_update)
    def post(self):
        """
        更新账户
        :return:
        """
        u = auth_user()
        args = Dict(request.json)
        if not args.username:
            api.abort(400, "用户名必填")

        del args.password

        args.id = args.id if args.id else u.id

        with db.session() as s:
            sql = "select id from _user where username=:username and id!=:id"
            db_user = s.query_one(sql, username=args.username, id=args.id)
            if db_user:
                return {"message": "修改失败, 用户名已被使用"}, 600

            sql = "select id from _user where mobile=:mobile"
            user_db = s.query_one(sql, mobile=args.mobile)

            if user_db:
                return {'message': f'手机号 {args.mobile} 已经存在'}, 600

            user = dbplus.update(u, '_user', args, session=s)[0]
            del user['password']
            return user


@ns.route('/register')
class Register(Resource):
    @log_action(with_secret=True)
    @api.expect(dto.user_register)
    def post(self):
        """
        用户注册
        :return:
        """
        args = Dict(request.json)
        if not args.username:
            api.abort(400, "用户名必填")
        if not args.password:
            api.abort(400, "密码必填")
        if not utils.check_password(args.password):
            api.abort(400, "密码长度至少为6个字符")
        with db.session() as s:
            exists_user = s.query_one('select id from _user where mobile=:mobile', mobile=args.mobile)
            if exists_user:
                return {'message': f'手机号{args.mobile}已经被注册'}, 600

        with db.session() as s:
            exists_user = s.query_one('select id from _user where username=:username', username=args.username)
            if exists_user:
                return {'message': f'用户名{args.username}已经存在'}, 600

        if not session.get('sms_captcha') == args.sms_captcha:
            return {'message': '短信验证码不正确'}, 600

        org = None
        # domain = util.get_host(request.headers['origin'])
        if args.org_code:
            sql = "select id from _org where code=:code "
            org = db.query_one(sql, code=args.org_code)

        # if not org:
        #     sql = "select id from _org where domain=:domain"
        #     org = db.query_one(sql, domain=domain)

        with db.session() as s:
            user = {
                'username': args.username,
                'password': generate_password_hash(args.password),
                'email': args.email,
                'mobile': args.mobile,
                'displayName': args.username,
                'avatar': '/avatar.jpg',
                'isActive': 1,
                'createDate': datetime.now(),
                'updateDate': datetime.now(),
                'orgId': org.id if org else None
            }
            s.add('_user', user)
            return {'message': '注册成功'}


@ns.route('/recover_password')
class RecoverPassword(Resource):
    @auth_required
    @log_action(with_secret=True)
    @api.expect(dto.recover_password)
    def post(self):
        """
        管理员重置密码
        :return:
        """

        u = auth_user()
        args = Dict(request.json)
        if not args.password:
            api.abort(400, "密码必填")
        if not utils.check_password(args.password):
            api.abort(400, "密码长度至少为6个字符")

        args.password = generate_password_hash(args.password)

        with dbplus.session() as s:
            user, status = dbplus.update(u, '_user', args, session=s)

            if status != 200:
                return user, status

            del user['password']
            return user


@ns.route('/reset_password')
class ResetPassword(Resource):
    @auth_required
    @log_action(with_secret=True)
    @api.expect(dto.reset_password)
    def post(self):
        """
        重置密码
        :return:
        """
        u = auth_user()
        args = Dict(request.json)
        if not args.mobile:
            api.abort(400, "手机号必填")
        if not args.password:
            api.abort(400, "密码必填")
        if not utils.check_password(args.password):
            api.abort(400, "密码长度至少为6个字符")

        if session.get('sms_captcha') != args.sms_captcha:
            return {'message': '短信验证码不正确'}, 600

        sql = "select * from _user where mobile=:mobile and id=:uid"
        with db.session() as s:
            user = s.query_one(sql, mobile=args.mobile, uid=u.id)
            if not user:
                return {"message": "手机号未关联此账号"}, 600

            user['password'] = generate_password_hash(args.password)
            s.merge('_user', user)
            return {'message': '密码重置成功'}


@ns.route('/get_captcha')
class GetCaptcha(Resource):
    def get(self):
        """
        获取验证码图片 base64
        :return:
        """
        res = utils.get_captcha()
        session['captcha'] = res['captchaText']
        return {'base64': res['base64']}


@ns.route('/get_captcha_stream')
class GetCaptchaStream(Resource):
    def get(self):
        """
        获取验证码图片 数据流
        :return:
        """
        res = utils.get_captcha()
        session['captcha'] = res['captchaText']
        return send_file(res['stream'], attachment_filename='captcha.jpg', mimetype='image/jpg')


@ns.route('/delete_user')
class DeleteUser(Resource):
    @auth_required
    @log_action(action='delete')
    @api.expect(dto.delete_user)
    def delete(self):
        """
        删除用户
        :return:
        """
        user = auth_user()
        args = Dict(request.json)

        with db.session() as s:
            sql = "select id,username from _user where id=:uid"
            db_user = s.query_one(sql, uid=args.id)
            if not db_user:
                return {"message": "用户不存在"}, 404
            if db_user['username'] == user['username']:
                return {"message": "不能删除自己"}, 403

            res = dbplus.check_perm(user, '_user', 'deleteEnabled', '删除用户', session=s)
            if res.status != 200:
                return res.message, res.status

            s.execute('delete from _user_role where userId=:uid', uid=args.id)
            s.execute("delete from _user where id=:id", id=args.id)
            return {'message': 'success'}, 200
