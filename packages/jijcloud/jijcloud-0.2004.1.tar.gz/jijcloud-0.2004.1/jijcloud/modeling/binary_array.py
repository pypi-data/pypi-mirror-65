from jijcloud.modeling.tensor import Tensor
import pyqubo as pyq


class BinaryArray(Tensor):
    var_type = 'variable'

    def to_pyqubo(self, **kwargs):
        if len(kwargs) == 0:
            return pyq.Array.create(self.name, self.shape, 'BINARY')
        else:
            var_label = self.name
            for i, k in enumerate(self._index_labels):
                if k is None:
                    var_label += '[{}]'.format(self._fixed_index[i])
                else:
                    var_label += '[{}]'.format(kwargs[k])

            return pyq.Binary(var_label)
