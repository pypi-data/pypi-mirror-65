from flask.sessions import SecureCookieSessionInterface, total_seconds, BadSignature
import json


class SecureCookieSession(SecureCookieSessionInterface):
    # 自定义 session ，同时把 session 放入 verify 字段
    def save_session(self, app, session, response):
        if session is None:
            return

        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        # If the session is modified to be empty, remove the cookie.
        if session.modified:
            response.delete_cookie(
                app.session_cookie_name, domain=domain, path=path
            )

        # Add a "Vary: Cookie" header if the session was accessed at all.
        if session.accessed:
            response.vary.add("Cookie")

        if not self.should_set_cookie(app, session):
            return

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        samesite = self.get_cookie_samesite(app)
        expires = self.get_expiration_time(app, session)
        val = self.get_signing_serializer(app).dumps(dict(session))
        response.set_cookie(
            app.session_cookie_name,
            val,
            expires=expires,
            httponly=httponly,
            domain=domain,
            path=path,
            secure=secure,
            samesite=samesite,
        )

        if response.headers.get("Content-Type") == "application/json":
            data = json.loads(response.data.decode('utf8'))
            data["Verify"] = response.headers['Set-Cookie']
            response.data = json.dumps(data).encode('utf8')

    def open_session(self, app, request):
        s = self.get_signing_serializer(app)
        if s is None:
            return None
        val = request.cookies.get(app.session_cookie_name)
        if not val:
            verify = request.headers.get("Verify")
            if not verify:
                return self.session_class()
            verify = cookie2dict(verify)
            val = verify.get(app.session_cookie_name)
        if not val:
            return self.session_class()
        max_age = total_seconds(app.permanent_session_lifetime)
        try:
            data = s.loads(val, max_age=max_age)
            return self.session_class(data)
        except BadSignature:
            return self.session_class()


def cookie2dict(cookie_str):
    res = {}
    for kv in cookie_str.split("; "):
        bb = kv.split('=')
        if len(bb) != 2:
            continue
        res[bb[0]] = bb[1]
    return res
