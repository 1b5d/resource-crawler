"""
module that contains helper methods for the crawler.
"""
import urlparse
import re

http_remover_regex = re.compile(ur'http(?:s?):\/\/')
last_slash_remover_regex = re.compile(ur'/$')


def prepend_http(url):
    """
    adds http to the URL when it doesn't start with 'http://' or 'https://'.
    :param str url: the URL to be prepended.
    :return: str the result URL.
    """
    if url is None:
        return None
    if not url.startswith('http'):
        url = 'http://' + url
    return url


def strip_http(url):
    """
    removes 'http://' or 'https://' from the beginning of a URL if they exist.
    this method also strips the slash char '/' from the end of the URL if exists.
    :param str url: the URL to be stripped.
    :return: str the result URL.
    """
    if url is None:
        return None
    if url.startswith('http'):
        url = http_remover_regex.sub('', url)
    if url.endswith('/'):
        url = last_slash_remover_regex.sub('', url)
    return url


def get_url_domain(url):
    """
    returns the domain host of a URL.
    :param str url: the URL to get the domain of.
    :return str: the URL domain.
    """
    if url is None:
        return None
    parsed_url = urlparse.urlparse(url)
    return parsed_url.netloc