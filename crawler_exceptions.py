class CrawlerException(Exception):
    pass


class CrawlerRuntimeError(CrawlerException):
    pass


class ParserNotSetException(CrawlerException):
    pass
