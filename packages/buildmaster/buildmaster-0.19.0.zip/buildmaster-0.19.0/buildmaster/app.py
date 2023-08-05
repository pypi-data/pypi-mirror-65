import os.path
from flask import Flask
from flask import _app_ctx_stack as ctx_stack
import logging.config

import traceback
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_csrf_token
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended.config import config
from jwt.exceptions import ExpiredSignatureError
from decimal import Decimal
from .db import Db, DbPlus, Dict, AlchemyEncoder
from .session import SecureCookieSession
import re
import functools

from importlib.machinery import SourceFileLoader

# load from directory where python script starts
path = os.path.join(os.getcwd(), 'settings.py')

settings = SourceFileLoader("settings", path).load_module()

settings = Dict({name: getattr(settings, name) for name in dir(settings)})

logging_conf_path = os.path.join(os.getcwd(), 'log.conf')
if not os.path.exists(logging_conf_path):
    print('Missing log.conf in start directory, using console instead')
else:
    logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

db_settings = settings.get('db', {})

engine = create_engine(db_settings.get('url'), **db_settings.get('engine_options', {}))
db = Db(engine, force_escape_sql=db_settings.get('force_escape_sql', False))
dbplus = DbPlus(db)

app = Flask(__name__)

cors_settings = settings.get('cors', {})
if len(cors_settings) > 0:
    CORS(app, **cors_settings)  # 跨域支持

# JWT配置
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)


class ExtendEncoder(AlchemyEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        else:
            return super().default(obj)


# 配置默认的JSON序列化
app.config['RESTPLUS_JSON'] = {
    'cls': ExtendEncoder,
    'check_circular': False,
    'indent': 2,
    'separators': (', ', ': ')
}

jwt_settings = settings.get('jwt', {})
JWT_ACCESS_COOKIE_NAME = jwt_settings.get('JWT_ACCESS_COOKIE_NAME', 'accessToken')
JWT_REFRESH_COOKIE_NAME = jwt_settings.get('JWT_REFRESH_COOKIE_NAME', 'refreshToken')

app.config.update(jwt_settings)
flask_app_settings = settings.get('flask_app', {})
app.config.update(flask_app_settings)

jwt = JWTManager(app)

auth_required = jwt_required

app.session_interface = SecureCookieSession()


def get_api_identity():
    return getattr(ctx_stack.top, 'api_user', None)


def auth_user():
    u = get_jwt_identity()
    if u is None:
        u = get_api_identity()
    if u is None:
        return
    return Dict(u)


api_settings = settings.get('api', {
    'version': '1.0.0',
    'prefix': '/api',
    'doc': '/api/doc',
    'title': 'BuildMaster API',
    'description': 'Powered by BuildMaster'
})

api = Api(**api_settings)

api.app = app
api.init_app(app)


def handle_expection(func):
    @functools.wraps(func)
    def inner(e):
        response = _handle(e)
        if response:
            return response
        return func(e)

    return inner


def _handle(e):
    track = str(e)
    if 'IntegrityError' in track and "1062" in track:
        pattern = re.compile("(?<=entry ').*(?=' for)")
        res = re.search(pattern, track)
        if res:
            return {"message": f"{res.group()} 已经存在"}

    if 'IntegrityError' in track and "1451" in track:
        pattern = re.compile("(?<=`.`).*(?=`, CONSTRAINT)")
        res = re.search(pattern, track)

        if res:
            message = res.group()

            if '_user_role' in track:
                message = "用户角色"
            elif "_org_owner" in track:
                message = "可管理组织"

            return {"message": f"请先删除 {message} 关联关系"}

    if "InternalError" in track and "1366" in track:
        col_type = re.compile('(?<=Incorrect ).*(?= value)')
        col_type = re.search(col_type, track)

        col = re.compile("(?<=column ').*(?=' at)")
        col = re.search(col, track)

        if col_type and col:
            return {"message": f"{col.group()} 数据类型不正确，要求 {col_type.group()}"}

    if 'invalid literal for' in track:
        col_type = re.compile("(?<=for ).*(?= with)")
        col_type = re.search(col_type, track)
        value = re.compile("(?<=: ').*(?=')")
        value = re.search(value, track)
        if col_type and value:
            return {"message": f"{value.group()} to {col_type.group()} 转换失败"}


@api.errorhandler
@handle_expection
def default_error_handler(e):
    error_fullstack = settings.get('server', {}).get('error_fullstack', True)
    log.exception(e)
    if not error_fullstack:
        message = 'An unhandled exception occurred.'
    else:
        message = traceback.format_exc()
    return {'message': message}, 500


@api.errorhandler(NoAuthorizationError)
def jwt_error_handler(e):
    return {'message': '%s' % e}, 403


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': '%s' % e}, 404


@api.errorhandler(ExpiredSignatureError)
def jwt_expired_signature_error_handler(e):
    return {'message': '%s' % e}, 422


def set_access_cookies(response, encoded_access_token, max_age=None):
    if not config.jwt_in_cookies:
        raise RuntimeWarning("set_access_cookies() called without "
                             "'JWT_TOKEN_LOCATION' configured to use cookies")

    # Set the access JWT in the cookie
    response.set_cookie(config.access_cookie_name,
                        value=encoded_access_token,
                        max_age=max_age or config.cookie_max_age,
                        secure=config.cookie_secure,
                        httponly=False,
                        domain=config.cookie_domain,
                        path=config.access_cookie_path,
                        samesite=config.cookie_samesite)

    # If enabled, set the csrf double submit access cookie
    if config.csrf_protect and config.csrf_in_cookies:
        response.set_cookie(config.access_csrf_cookie_name,
                            value=get_csrf_token(encoded_access_token),
                            max_age=max_age or config.cookie_max_age,
                            secure=config.cookie_secure,
                            httponly=False,
                            domain=config.cookie_domain,
                            path=config.access_csrf_cookie_path,
                            samesite=config.cookie_samesite)


def set_refresh_cookies(response, encoded_refresh_token, max_age=None):
    if not config.jwt_in_cookies:
        raise RuntimeWarning("set_refresh_cookies() called without "
                             "'JWT_TOKEN_LOCATION' configured to use cookies")

    # Set the refresh JWT in the cookie
    response.set_cookie(config.refresh_cookie_name,
                        value=encoded_refresh_token,
                        max_age=max_age or config.cookie_max_age,
                        secure=config.cookie_secure,
                        httponly=False,
                        domain=config.cookie_domain,
                        path=config.refresh_cookie_path,
                        samesite=config.cookie_samesite)

    # If enabled, set the csrf double submit refresh cookie
    if config.csrf_protect and config.csrf_in_cookies:
        response.set_cookie(config.refresh_csrf_cookie_name,
                            value=get_csrf_token(encoded_refresh_token),
                            max_age=max_age or config.cookie_max_age,
                            secure=config.cookie_secure,
                            httponly=False,
                            domain=config.cookie_domain,
                            path=config.refresh_csrf_cookie_path,
                            samesite=config.cookie_samesite)
