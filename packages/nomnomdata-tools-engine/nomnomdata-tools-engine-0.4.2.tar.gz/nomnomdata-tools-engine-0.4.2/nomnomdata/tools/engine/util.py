import hashlib
import hmac
from calendar import timegm
from datetime import datetime, timedelta
from urllib.parse import urlencode

from requests.auth import AuthBase


class KeyAuth(AuthBase):
    def __init__(self, secret: str):
        self.secret = secret.encode("utf-8")

    def __call__(self, request):
        body = request.body or b""
        if not isinstance(body, bytes):
            body = body.encode("utf-8")
        url = request.url.encode("utf-8")
        ts = str(generate_request_timestamp())
        data = b"".join([ts.encode("utf-8"), body, url])
        signer = hmac.new(self.secret, data, hashlib.sha512)

        request.headers["X-NomNom-Signature"] = signer.hexdigest()
        request.headers["X-NomNom-SigTimestamp"] = ts
        return request


def generate_request_timestamp():
    return timegm(datetime.utcnow().utctimetuple())
