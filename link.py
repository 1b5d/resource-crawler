
class Link(object):
    def __init__(self, link, parent=None):
        self.link = link
        self.parent = parent
        self.content = None
