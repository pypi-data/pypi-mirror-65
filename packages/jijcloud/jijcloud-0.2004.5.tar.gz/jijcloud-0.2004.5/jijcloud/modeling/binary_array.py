from jijcloud.modeling.tensor import Tensor
import pyqubo as pyq


class BinaryArray(Tensor):
    var_type = 'variable'

    def to_pyqubo(self, fixed_variables: dict = {}, **kwargs):
        if len(kwargs) == 0:
            return pyq.Array.create(self.name, self.shape, 'BINARY')
        else:
            var_label = self.name
            indices = []
            for i, k in enumerate(self._index_labels):
                if k is None:
                    var_label += '[{}]'.format(self._fixed_index[i])
                    indices.append(self._fixed_index[i])
                else:
                    var_label += '[{}]'.format(kwargs[k])
                    indices.append(kwargs[k])
            indices = indices[0] if len(indices) == 1 else tuple(indices)
            if indices in fixed_variables.get(self.name, {}):
                return fixed_variables[self.name][indices]
            return pyq.Binary(var_label)
