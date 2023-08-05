from jijcloud.modeling.term import Term
from jijcloud.modeling.sum import Sum


class Tensor():
    var_type = 'tensor'

    def __init__(self, name: str, shape: (tuple, int) = None, dim: int = None):
        if not isinstance(name, str):
            raise TypeError('name is str.')

        if shape is not None and isinstance(shape, (tuple, int)):
            if isinstance(shape, int):
                self.shape = (shape, )
            else:
                self.shape = shape
            self.dim = len(self.shape)
        elif dim is not None and isinstance(dim, int):
            self.dim = dim
            self.shape = tuple(None for i in range(dim))
        else:
            raise ValueError('set "shape (tuple)" or "dim (int)".')

        self.name = name
        self._index_labels = [None for i in range(self.dim)]
        self._fixed_index = [None for i in range(self.dim)]
        self._index = set([])

    @property
    def variables(self):
        return {self.name: {'dimension': self.dim, 'var_type': self.var_type}}

    @property
    def index(self):
        return self._index

    def copy(self):
        import copy
        return copy.deepcopy(self)

    def __str__(self):
        myname = self.name
        for i, s in enumerate(self._index_labels):
            if s is None:
                myname += '[{}]'.format('.')
            else:
                myname += '[{}]'.format(s)
        return myname

    def __repr__(self):
        return self.__class__.__name__ + ':' + self.__str__()

    def _add_index(self, key):
        array = self.copy()
        if isinstance(key, (str, int, slice)):
            key = (key, )
        elif not isinstance(key, tuple) and not isinstance(key[0], str):
            raise KeyError(self.__class__.__name__ +
                           ' has not {} key.'.format(type(key)))
        for i, k in enumerate(key):
            if isinstance(k, str):
                array._index_labels[i] = k
                array._index.add(k)
            elif isinstance(k, slice):
                array._index_labels[i] = '{}.{}'.format(self.name, i)
                array._index.add('{}.{}'.format(self.name, i))
            elif isinstance(k, int):
                array._fixed_index[i] = k
        return array

    def __getitem__(self, key: str):
        """make tensor which has indices (key)
        """
        array = self._add_index(key)
        term = Term([array])
        for i, sl in enumerate(array._index_labels):
            # if index 'sl' is contracted by syntax sugar x[:]
            if '{}.{}'.format(self.name, i) == sl:
                sh_i = self.shape[i]
                v = list(range(sh_i)) if isinstance(sh_i, int) else sh_i
                term = Sum({sl: v}, term)
        return term

    def to_serializable(self):
        return {
            'class': self.__class__.__name__,
            'shape': list(self.shape),
            'dim': self.dim,
            'name': self.name,
            'index': [i if i is not None else '' for i in self._index_labels],
            'fixed_index': [i if i is not None else '' for i in self._fixed_index]
        }

    @classmethod
    def from_serializable(cls, obj):
        term = cls(
            name=obj['name'],
            shape=tuple(obj['shape']),
            dim=obj['dim']
        )
        term._index = set(obj['index']) - set([''])
        term._index_labels = [s if s != '' else None for s in obj['index']]
        term._fixed_index = [
            s if s != '' else None for s in obj['fixed_index']]
        return term
