from flask import request
from functools import wraps
from .app import auth_user, Dict, db, settings
import time
from datetime import datetime

log_enabled = settings.get('flask_app', {}).get('LOG_ACTION', True)

class log_action(object):
    def __init__(self, action='post', with_secret=False):
        self.action = action
        self.with_secret = with_secret

    def _do_log(self, username, org_id, body, time_cost):
        if self.with_secret:
            body = '内容带敏感数据'
            if not username and request.json:  # 没有登录用户的时候尝试从提交信息中找username
                username = request.json.get('username')
                user = None
                if username:
                    user = db.query_one('select username, orgId from _user where username=:username', username=username)
                mobile = request.json.get('mobile')
                if not user and mobile:
                    user = db.query_one('select username, orgId from _user where mobile=:mobile', mobile=mobile)
                if user:
                    username = user['username']
                    org_id = user['orgId']

        headers = Dict(request.headers)
        record = Dict()
        record.method = request.method
        record.url = request.url
        record.data = body
        record.opUser = username
        record.ip = headers['X-Real-Ip'] if headers.get('X-Real-Ip') else request.remote_addr
        record.timeCost = time_cost
        record.opAction = self.action
        record.createTime = datetime.now()
        record.orgId = org_id
        db.add('_log', record)

    def __call__(self, func):
        @wraps(func)
        def inner(view, *a, **k):
            """
            当请求方法被多个装饰器修饰，为了得到访问的用户，当前装饰器需放在最下面。
            :param view:
            :param a:
            :param k:
            :return:
            """
            if not log_enabled:
                return func(view, *a, **k)

            u = auth_user()
            username = None
            org_id = None
            if u:
                username = u.username
                org_id = u.orgId

            body = str(request.json) if request.json else ''
            start_time = time.time() * 1000
            response = func(view, *a, **k)
            time_cost = time.time() * 1000 - start_time

            try:
                self._do_log(username, org_id, body, time_cost)
            except:
                pass

            return response

        return inner
