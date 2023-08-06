

class IndexSet():
    def __init__(self, label: str):
        self.label = label
        self._list = None

    def size(self):
        if self._list is not None:
            return len(self._list)
        else:
            return SetSize(self.label)

    def __len__(self):
        if self._list is not None:
            return len(self._list)
        raise TypeError('IndexSet: "{}" has not elements.'.format(self.label))

    def set(self, ordered_set):
        self._list = ordered_set

    def to_serializable(self):
        obj = {'class': self.__class__.__name__,
               'label': self.label}
        if self._list:
            obj['list'] = self._list
        return obj

    @classmethod
    def from_serializable(cls, obj):
        v = cls(obj['label'])
        v.set(obj.get('list', None))
        return v


class SetSize():
    def __init__(self, label: str):
        self.label = label
        self.offset = 0
        self.coeff = 1.0
        self.exponent = 1.0

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __ladd__(self, other):
        return self.__add__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        self.offset = other + self.offset
        return self

    def __lmul__(self, other):
        return self.__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        self.coeff = self.coeff * other
        self.offset = self.offset * other
        return self

    def __pow__(self, other):
        self.exponent = other
        return self
