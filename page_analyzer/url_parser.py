from urllib.parse import urlparse


def parse(url):
    url_parsed = (
        urlparse(url)
        ._replace(fragment="", params="", query="", path="")
        .geturl()
    )
    url_parsed = url_parsed.replace("www.", "")
    return url_parsed
