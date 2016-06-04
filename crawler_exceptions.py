"""
module that contains all the exceptions used by the crawler app.
"""


class CrawlerException(Exception):
    """
    A general exception that all the crawler exception should inherit from.
    """
    pass


class CrawlerRuntimeError(CrawlerException):
    """
    An exception that represents an error happened during the crawler execution.
    """
    pass


class ParserNotSetException(CrawlerException):
    """
    An exception thrown when the parser was not set in the crawler.
    """
    pass
