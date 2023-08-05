import collections


class IdenticalList(collections.MutableSequence):
    '''A list of identical objects.

    attributes and methods are exposed transparently for the entire list
    '''

    def __init__(self, *args, typeok=None):
        self.list = list()
        self.type = typeok or type(args[0])
        self.extend(list(args))

    def check(self, v):
        if not isinstance(v, self.type):
            raise TypeError('Items added to a RotatableList must be instances of {}. Got {}'.format(self.type, type(v)))

    def __len__(self): return len(self.list)

    def __getitem__(self, i): return self.list[i]

    def __delitem__(self, i): del self.list[i]

    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v

    def insert(self, i, v):
        self.check(v)
        self.list.insert(i, v)

    def __str__(self):
        return str(self.list)

    def __getattr__(self, attr):
        if attr in ['list', 'type']:
            return super().__getattr__(attr)
        else:
            try:
                if callable(getattr(self.list[0], attr)):
                    def wrapper(*args, **kw):
                        result = None
                        for n, item in enumerate(self.list):
                            if n == 0:
                                result = getattr(item, attr)(*args, **kw)
                            else:
                                getattr(item, attr)(*args, **kw)
                        return result
                    return wrapper
                else:
                    return getattr(self.list[0], attr)
            except IndexError:
                return None

    def __setattr__(self, attr, val):
        if attr in ['list', 'type']:
            super().__setattr__(attr, val)
        else:
            for item in self.list:
                setattr(item, attr, val)
