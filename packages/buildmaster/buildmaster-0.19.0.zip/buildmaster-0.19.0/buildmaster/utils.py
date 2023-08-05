import shutil
import sys
import os
from datetime import datetime
from .app import settings

if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile

UPLOAD_BASE_DIR = settings.upload['base_dir']
UPLOAD_SUB_DIRS = settings.upload['sub_dirs']
UPLOAD_URL_PREFIX = settings.upload['url']
UPLOAD_FILE_EXT = settings.upload['file_ext']
UPLOAD_IMAGE_EXT = settings.upload.get('image_ext', ['jpg', 'jpeg', 'png'])
IMAGE_RESIZE = settings.upload.get('image_resize', (640, 480))


def upload_file(file, tag=None):
    ext = file.filename.rsplit('.')

    if len(ext) <= 1 or (ext[-1] not in UPLOAD_FILE_EXT):
        return {"message": f"文件类型（{ext[-1]}）不支持"}, 600

    time_str = datetime.now().strftime('%Y%m%d%H%M%S%f')
    filename = str(time_str) + '.' + ext[-1]

    if not os.path.exists(UPLOAD_BASE_DIR):
        os.mkdir(UPLOAD_BASE_DIR)

    storage_path = UPLOAD_BASE_DIR
    relative_url = filename
    if tag and tag in UPLOAD_SUB_DIRS:
        storage_path = os.path.join(storage_path, tag)
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
        relative_url = tag + "/" + filename

    filepath = os.path.join(storage_path, filename)
    if ext in UPLOAD_IMAGE_EXT:     # 针对Image处理
        blob = file.read()
        resize_image(blob, filepath)
    else:
        file.save(filepath)

    url = UPLOAD_URL_PREFIX + "/" + relative_url

    return {"url": url, "relativeUrl": relative_url}


def upload_zip(records, column, file, tag):
    """
    对上传的zip文件解压缩，根据记录集合中指定的列（可多个）的值，查找确认文件、图片是否存在，未找到records中设置为None
    zip解压缩后每个文件重新命名（图片预处理），并更新records对应的值，以便最终入库记录
    :param records: 上传的业务表记录集合
    :param column: 关注的列或者列数组
    :param file: zip文件流
    :param tag: 文件存储标签，用于提示子文件夹
    :return:
    """
    try:
        z_file = zipfile.ZipFile(file)
    except:
        return {"message": "压缩文件无法识别"}, 400
    base_path = UPLOAD_BASE_DIR
    if tag not in UPLOAD_SUB_DIRS:
        tag = None

    sub_path = datetime.now().strftime('%Y%m%d%H%M%S')  # 临时文件子目录，防止多人同时操作，数据覆盖。
    tmp_path = f"/tmp/{sub_path}"

    if not os.path.exists(base_path):
        os.mkdir(base_path)

    if not os.path.exists(tmp_path):
        os.mkdir(tmp_path)

    file_path_list = []
    for item in z_file.namelist():
        if not item.startswith('_'):
            file_path_list.append(item)
            z_file.extract(item, tmp_path)
    z_file.close()

    if not isinstance(column, (tuple, list)):
        column = [column]

    for c in column:
        for r in records:
            upload_file_item = r.get(c)
            if not upload_file_item:
                continue

            ext = upload_file_item.rsplit('.')[-1]
            time_str = datetime.now().strftime('%Y%m%d%H%M%S%f')
            filename = str(time_str) + '.' + ext
            storage_path = UPLOAD_BASE_DIR
            relative_url = filename
            if tag and tag in UPLOAD_SUB_DIRS:
                storage_path = os.path.join(storage_path, tag)
                if not os.path.exists(storage_path):
                    os.mkdir(storage_path)
                relative_url = tag + "/" + filename

            filepath = os.path.join(storage_path, filename)
            from_file_path = f"{tmp_path}/{upload_file_item}"
            if not os.path.exists(from_file_path):
                r[c] = None
                continue

            if ext in UPLOAD_IMAGE_EXT:  # 针对Image处理
                file = open(from_file_path, "rb")
                blob = file.read()
                resize_image(blob, filepath)
                file.close()
            else:
                try:
                    shutil.copyfile(from_file_path, filepath)
                except:
                    pass
            r[c] = relative_url
    shutil.rmtree(tmp_path)


def resize_image(blob, file_name):
    from wand.image import Image
    with Image(blob=blob) as img:
        h, w = IMAGE_RESIZE
        if img.width > w:
            r = w/img.width*1.0
            h = img.height*r
        else:
            w = img.width
            h = img.height

        img.resize(int(w), int(h))
        img.save(filename=file_name)