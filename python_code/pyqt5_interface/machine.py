
class Machine():
    def __init__(self, purpose=None, site=None, category=None, components=[], humanOperation=False):
        self.purpose = purpose
        self.site = site
        self.category = category
        self.components = components
        self.humanOperation = humanOperation