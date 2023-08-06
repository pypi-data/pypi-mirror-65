import random
from captcha.image import ImageCaptcha
import base64
import re


def get_captcha():
    captcha_text = ''.join(random.sample("23456890", 4))
    image = ImageCaptcha()
    image_io = image.generate(captcha_text)
    base64_data = base64.b64encode(image_io.getvalue())
    s = base64_data.decode()
    return {"base64": s, 'captchaText': captcha_text, 'stream': image_io}


def check_password(password):
    pattern = re.compile('^[a-zA-Z0-9\.@\-_]{6,64}$')
    res = re.match(pattern, password)
    return res


def get_host(headers):
    origin = headers.get('Origin')
    pattern = re.compile('(?<=https://).*')
    res = re.search(pattern, origin if origin else "")
    return res.group() if res else ""

