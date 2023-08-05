import uuid
from mimetypes import guess_extension
from urllib.parse import urljoin

from qcos import Client


class COS(object):
    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        secret_id = app.config["COS_SECRET_ID"]
        secret_key = app.config["COS_SECRET_KEY"]
        region = app.config["COS_REGION"]
        bucket = app.config["COS_BUCKET"]
        scheme = app.config.get("COS_SCHEME", "http")
        self.host = app.config.get("COS_HOST")

        self.client = Client(secret_id, secret_key, region, bucket, scheme)

    def head_object(self, key):
        return self.client.head_object(key)

    def get_object(self, key):
        return self.client.get_object(key)

    def put_object(self, key, data, **kwargs):
        return self.client.put_object(key, data, **kwargs)

    def get_url(self, key):
        if self.host:
            return urljoin(self.host, key)
        else:
            return self.client.get_url(key)


def gen_filename(mimetype=""):
    """使用uuid生成随机文件名
    :params mimetype: 用于生成文件扩展名
    """
    ext = guess_extension(mimetype)
    if ext == ".jpe":
        ext = ".jpg"
    elif ext is None:
        ext = ""

    return uuid.uuid4().hex + ext
