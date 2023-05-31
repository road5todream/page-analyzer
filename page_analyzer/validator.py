import validators
from urllib.parse import urlparse


def validator(url):
    if len(url) > 255:
        return {"result": False, "message": "URL превышает 255 символов"}
    if not validators.url(url):
        return {"result": False, "message": "Некорректный URL"}
    return {"result": True}


def normalize(url):
    out = urlparse(url)
    return f'{out.scheme}://{out.netloc}'
