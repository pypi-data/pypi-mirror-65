# encoding=utf8

from flask_restplus import Resource
from ..utils import upload_file
from ..app import (
    api,
    auth_required
)

from . import dto
ns = api.namespace(name='upload', description="文件上传API")


@ns.route('/')
class UploadFile(Resource):
    @auth_required
    @api.expect(dto.upload_file)
    def post(self):
        """文件上传"""
        args = dto.upload_file.parse_args()
        return upload_file(args.file, args.tag)

