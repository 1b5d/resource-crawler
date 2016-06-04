"""
Module that has a sitemap generator.
"""

from link import Link


class Generator(object):
    """
    Class Generator represents a sitemap generator
    taking a dict of links as an input.
    """
    def __init__(self, links):
        """
        initialize the generator.

        :param dict links: a dictionary that contains all the links
        to be shown in the sitemap
        :return: None.
        """
        self.links = links

    def get_children(self, link=None):
        """
        returns the children of a link

        :param Link or str link: a link whose children are to be returned.
        :return: a generator of links.
        """
        for key in self.links:
            if self.links[key].is_parent(link):
                yield self.links[key]

    def get_html(self, link=None):
        """
        returns the links as sitemap written in HTML.

        :param Link link: the entry point the links.
        by default, None is passed to choose the ultimate parents of the links
        as an entry point.
        :return: str the HTML string that contains the sitemap.
        """
        parts = ['<ul>']
        for item in self.get_children(link):
            parts.append('<li>')
            if item.link_type == Link.TYPE_HYPERLINK:
                # in case the link represents a hyperlink
                parts.append('<a href="%s">' % item.link)
                parts.append(item.link)
                parts.append('</a>')
            elif item.link_type == Link.TYPE_RESOURCE:
                # in case the link represents a resource in a page
                parts.append('Resource(%s): %s' % (item.tag, item.link))
            parts.append(self.get_html(item))
            parts.append('</li>')
        parts.append('</ul>')

        return ''.join(parts)
