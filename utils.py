import urlparse
import re

http_remover_regex = re.compile(ur'http(?:s?):\/\/')
last_slash_remover_regex = re.compile(ur'/$')


def prepend_http(url):
    if url is None:
        return None
    if not url.startswith('http'):
        url = 'http://' + url
    return url


def strip_http(url):
    if url is None:
        return None
    if url.startswith('http'):
        url = http_remover_regex.sub('', url)
    if url.endswith('/'):
        url = last_slash_remover_regex.sub('', url)
    return url


def get_url_domain(url):
    if url is None:
        return None
    parsed_url = urlparse.urlparse(url)
    return parsed_url.netloc