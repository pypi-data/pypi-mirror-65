from jijcloud.modeling.term import Term
from jijcloud.modeling.index_set import IndexSet, SetSize
import numpy as np


def Sum(indices, term):
    return Term([term], operator=SumOperator(indices))


class SumOperator():
    name = 'Sum'

    def __init__(self, indices):
        self.indices = indices
        self.depend_ind = {}
        self._V = {}
        sum_ind = []
        for ind, V in indices.items():
            _ind = ind.split(' ')
            sum_ind.append(_ind[0])
            # validation ----------------
            if not isinstance(V, (int, tuple, list)):
                _msg = 'Sum indices should be "int" or "tuple" or "list"'
                raise TypeError(_msg + ', not {}'.format(type(V)))
            # ---------------- validation
            self._V[_ind[0]] = V
            if len(_ind) > 1:
                self.depend_ind[_ind[0]] = (_ind[2], _ind[1])
        self.index_labels = list(self._V.keys())

    def to_pyqubo(self, term, fixed_variables: dict = {}, **kwargs):
        # 添字に依存するsumの足がある場合は依存性に基づいて計算
        for j, (i, cond) in self.depend_ind.items():
            iv = kwargs[i]
            Vi = self._convert_to_index_set(self._V[j], kwargs)
            Vi = [jv for jv in Vi if eval('jv {} {}'.format(cond, iv))]
            self._V[j] = Vi

        t = 0.0
        num_terms = self._num_terms(self._V, kwargs)
        for i in range(num_terms):
            new_args = kwargs.copy()
            new_args.update({k: self._convert_to_index_set(v, kwargs)[i]
                             for k, v in self._V.items()})
            t += term._poly_to_pyqubo(fixed_variables, **new_args)
        return (term.coeff*t + term.offset)**term.exponent

    def _convert_to_index_set(self, indices, kwargs: dict):
        if isinstance(indices, int):
            return list(range(indices))
        if isinstance(indices, tuple):
            a, b = indices
            if isinstance(a, SetSize):
                a = len(kwargs[a.label])
            if isinstance(b, SetSize):
                b = len(kwargs[b.label])
            return list(range(a, b))
        if isinstance(indices, list):
            return indices
        if isinstance(indices, IndexSet):
            return kwargs[indices.label]

    def _num_terms(self, indices, kwargs):
        ind_size = []
        for ind in indices.values():
            v = self._convert_to_index_set(ind, kwargs)
            ind_size.append(len(v))
        if not np.all(np.array(ind_size) == ind_size[0]):
            raise ValueError('indices should be same length.')
        return ind_size[0]

    def to_serializable(self):
        indices = {}
        for k, v in self.indices.items():
            if isinstance(v, tuple):
                indices_type = 'tuple'
            elif isinstance(v, list):
                indices_type = 'list'
            elif isinstance(v, int):
                indices_type = 'int'
            indices[k] = [v, indices_type]
        return [self.name, indices]

    @classmethod
    def from_serializable(cls, obj):
        if len(obj) == 0:
            return None
        indices = {}
        for k, v in obj[1].items():
            if v[1] == 'tuple':
                indices[k] = tuple(v[0])
            else:
                indices[k] = v[0]
        sum_ope = cls(indices=indices)
        return sum_ope
