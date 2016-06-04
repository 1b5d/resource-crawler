from link import Link


class Generator(object):
    def __init__(self, links):
        self.links = links

    def get_children(self, link=None):
        for key in self.links:
            if self.links[key].is_parent(link):
                yield self.links[key]

    def get_html(self, link=None):
        parts = ['<ul>']
        for item in self.get_children(link):
            parts.append('<li>')
            if item.link_type == Link.TYPE_HYPERLINK:
                parts.append('<a href="%s">' % item.link)
                parts.append(item.link)
                parts.append('</a>')
            elif item.link_type == Link.TYPE_RESOURCE:
                parts.append('Resource(%s): %s' % (item.tag, item.link))
            parts.append(self.get_html(item))
            parts.append('</li>')
        parts.append('</ul>')

        return ''.join(parts)
