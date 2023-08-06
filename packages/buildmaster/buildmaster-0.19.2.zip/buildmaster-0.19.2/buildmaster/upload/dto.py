# encoding=utf8


from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

upload_file = reqparse.RequestParser()
upload_file.add_argument('file', location='files', type=FileStorage, help="用户上传文件", required=True)
upload_file.add_argument('tag', location='form', help="文件归类标记（扩展使用）", required=False)
