import urlparse
import utils


class Link(object):

    TYPE_HYPERLINK = 1
    TYPE_RESOURCE = 2

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        # construct a full url in case its a relative link
        self.link = urlparse.urljoin(val.link, self.link)
        self.link = utils.prepend_http(self.link)
        self._parent = val

    def __init__(self, link, link_type=TYPE_HYPERLINK, tag='a'):
        self.link = link
        self.link_type = link_type
        self.tag = tag
        self._parent = None

    def is_parent(self, parent):
        if self.parent is None:
            return parent is None
        if isinstance(parent, Link):
            return self.parent.link == parent.link
        return self.parent.link == parent
