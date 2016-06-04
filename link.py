"""
module that contains link representation.
"""

import urlparse
import utils


class Link(object):
    """
    Class Link that represents a link inside the crawled page.
    """
    TYPE_HYPERLINK = 1
    TYPE_RESOURCE = 2

    @property
    def parent(self):
        """
        getter of the parent link.
        :return: Link the parent of the current link.
        """
        return self._parent

    @parent.setter
    def parent(self, val):
        """
        setter of the parent link
        :param Link val: the parent link to be set to the current link.
        :return: None.
        """
        # construct a full url in case its a relative link
        self.link = urlparse.urljoin(val.link, self.link)
        self.link = utils.prepend_http(self.link)
        self._parent = val

    def __init__(self, link, link_type=TYPE_HYPERLINK, tag='a'):
        """
        initialize the Link class with necessary arguments.

        :param str link: the URL of the link
        :param link_type: the type of the link:
        Link.TYPE_HYPERLINK to set the link as a hyperlink navigable link.
        Link.TYPE_RESOURCE to set the link as a resource in a page.
        :param tag: the tag name of the link.
        :return: None.
        """
        self.link = link
        self.link_type = link_type
        self.tag = tag
        self._parent = None

    def is_parent(self, parent):
        """
        checks if the passed value represents a parent of the current link.
        :param Link or str parent: the parent to check with.
        :return: bool
        """
        if self.parent is None:
            return parent is None
        if isinstance(parent, Link):
            return self.parent.link == parent.link
        return self.parent.link == parent
