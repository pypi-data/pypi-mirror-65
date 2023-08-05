from tornado import web

from ..app import settings

UPLOAD_FILE_EXT = settings.upload['file_ext']


class SmartStaticHandler(web.StaticFileHandler):
    async def get(self, path: str, include_body: bool = True):
        target = 'index.html'
        bb = path.split('/')
        prefix = bb[0].lower()
        if prefix == '' and len(bb) > 1:
            prefix = bb[1].lower()

        if prefix in ['css', 'js', 'assets', 'loading', 'swaggerui']:
            target = path

        bb = path.split('.')
        suffix = bb[len(bb)-1].lower()
        if suffix in UPLOAD_FILE_EXT:
            target = path

        return await super(SmartStaticHandler, self).get(target, include_body)
