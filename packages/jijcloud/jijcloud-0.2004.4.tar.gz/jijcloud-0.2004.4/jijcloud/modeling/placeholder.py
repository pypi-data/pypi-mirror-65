from jijcloud.modeling.tensor import Tensor
import numpy
import pyqubo as pyq


class PlaceholderArray(Tensor):
    var_type = 'placeholder'

    def __init__(self, name: str,
                 dim: int = None, shape: tuple = None,
                 array: numpy.ndarray = None):
        if array is not None:
            self.array = array
            self.shape = array.shape
            self.dim = len(self.shape)
        elif shape is not None:
            self.array = None
            self.shape = shape
            self.dim = len(shape)
        elif dim is not None:
            self.array = None
            self.dim = dim
            self.shape = tuple(None for i in range(dim))
        else:
            raise ValueError('input "array" or "shape".')
        super().__init__(name, self.shape)

    def to_pyqubo(self, **kwargs):
        if self.array is not None:
            a = self.array
            for i, k in enumerate(self._index_labels):
                if k is None:
                    index = self._fixed_index[i]
                else:
                    index = kwargs[k]
                a = a[index]
            return float(a)
        else:
            var_label = self.name
            for i, k in enumerate(self._index_labels):
                if k is None:
                    var_label += '[{}]'.format(self._fixed_index[i])
                else:
                    var_label += '[{}]'.format(kwargs[k])
            return pyq.Placeholder(var_label)

    def to_serializable(self):
        obj = super().to_serializable()
        obj['name'] = self.name
        obj['array'] = self.array.tolist() if self.array is not None else None
        return obj

    @classmethod
    def from_serializable(cls, obj):
        pl = super().from_serializable(obj)
        pl.array = obj['array']
        return pl


class PlaceholderScalar(PlaceholderArray):
    def __init__(self, name, shape=(1,), dim=1):
        shape = (1,)
        super().__init__(name, shape=shape)

    def to_pyqubo(self, **kwargs):
        return pyq.Placeholder(label=self.name)


def Placeholder(name):
    ps = PlaceholderScalar(name)
    return ps['.']
