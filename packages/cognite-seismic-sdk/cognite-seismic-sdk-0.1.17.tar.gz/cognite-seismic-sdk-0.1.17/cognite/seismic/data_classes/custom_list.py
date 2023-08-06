class CustomList(object):
    def __init__(self, iterable):
        self.iterable = iterable

    def __iter__(self):
        return iter(self.iterable)

    def to_list(self):
        self.load()
        return self.iterable

    def load(self):
        self.iterable = list(self.iterable)
