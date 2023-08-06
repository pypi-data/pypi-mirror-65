from flask import request
from flask import _app_ctx_stack as ctx_stack
import time
from datetime import datetime
import hashlib
from functools import wraps
from ..app import db, log, Dict, settings
from flask_jwt_extended import (
    verify_jwt_in_request,
    verify_jwt_in_request_optional,
    get_jwt_identity
)
from flask_jwt_extended.exceptions import (
    InvalidHeaderError, NoAuthorizationError
)

MISS_REQUIRED_PARAMS = "是必须的"
SIGN_EXPIRED = "timestamp时间戳失效"
SIGN_ERROR = "签名错误"
KEY_ERROR = "apiKey 无效"  # 不存在这个 appKey
KEY_EXPIRED = "apiKey 已过期"
KEY_NOT_ACTIVE = "apiKey 未激活"
ERROR_MESSAGE = ""

open_api_settings = settings.get('open_api', {})


class api_required(object):

    def __init__(self, params=None):
        if params is None:
            params = []
        self.params = params

    def __call__(self, func):

        @wraps(func)
        def inner(view, *args, **kwargs):   # TODO
            # 如果jwt已经登录允许直接访问， swagger可以直接测试
            try:
                verify_jwt_in_request()
            except (NoAuthorizationError, InvalidHeaderError) as e:
                args = request.json
                if not args:
                    raise e
                is_api_auth = True
                for c in ['timestamp', 'apiKey', 'sign']:
                    if c not in args:
                        is_api_auth = False
                        break
                if not is_api_auth:
                    raise e

            u = get_jwt_identity()
            if u:
                res = func(view)
                return res
            try:
                args = self.get_args(request)
            except Exception as e:
                log.warning(e)
                return self.error_message(ERROR_MESSAGE, params=str(e)), 400

            log.info(args)
            for c in ['timestamp', 'apiKey', 'sign']:
                if c not in args.keys():
                    return self.error_message(MISS_REQUIRED_PARAMS, params=c), 400

            timestamp = int(time.time() * 1000)

            t = int(args.timestamp)

            if abs(timestamp - t) >= open_api_settings.get('timestamp_expire', 60000):
                return self.error_message(SIGN_EXPIRED), 600

            with db.session() as s:
                sql = """
                select _user.id, _user.username, isActive, _user.mobile, _user.orgId ,_org.defaultPage,
                apiKey, apiSecret, expireDate, status 
                from _acl_api left join _user on _acl_api.userId = _user.id left join _org on _user.orgId=_org.id 
                where apiKey =:apiKey
                """
                user = s.query_one(sql, apiKey=args.apiKey)
                if not user:
                    return self.error_message(KEY_ERROR), 600

            if user.expireDate < datetime.now():
                return self.error_message(KEY_EXPIRED), 600

            if not user.status:
                return self.error_message(KEY_NOT_ACTIVE), 600

            user_sign = args.sign
            args.pop('sign')
            user_params = args

            # 删除空参数
            for key in list(user_params.keys()):
                if not user_params.get(key):
                    del user_params[key]

            sign = self.get_sign(user_params, user.apiSecret)

            if sign != user_sign:
                return self.error_message(SIGN_ERROR), 600

            if isinstance(self.params, (list, tuple)):
                for item in self.params:
                    if item not in args.keys():
                        return self.error_message(MISS_REQUIRED_PARAMS, params=item), 400
            elif isinstance(self.params, str):
                if self.params not in args.keys():
                    return self.error_message(MISS_REQUIRED_PARAMS, params=self.params), 400

            del user.apiSecret
            del user.expireDate
            del user.status

            self.verify_api_in_request(user)
            res = func(view)
            log.info(res)
            return res

        return inner

    @classmethod
    def get_args(cls, r):
        method = r.method
        args = None
        if method == "POST":
            try:
                args = Dict(r.json)
            except Exception:
                raise Exception("Content-Type 必须为 application/json")
        elif method == "GET":
            try:
                args = Dict(r.args)
                print(args)
            except Exception:
                raise Exception("错误，请求参数有误")
        elif method == "DELETE":
            try:
                args = Dict(r.json)
            except Exception:
                raise Exception("Content-Type 必须为 application/json")
        return args

    @classmethod
    def error_message(cls, error, params=None):
        message = error
        if params:
            message = f"{params} {error}"
        return {"message": message}

    @classmethod
    def get_sign(cls, params, api_secret):
        params_sorted = sorted(params.items(), key=lambda _: _[0])
        params_str = ""
        for k, v in params_sorted:
            params_str = f"{params_str}{k}={v}&"
        params_str = params_str + f"apiSecret={api_secret}"
        sign = hashlib.sha1(params_str.encode('utf8')).hexdigest()
        return sign

    @classmethod
    def verify_api_in_request(cls, user):
        ctx_stack.top.api_user = user

