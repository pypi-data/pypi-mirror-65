import numpy as np


class Term():
    """Term class
    Structure:
        (a * (Σ_i x_ij)_j + b)^r
        a: self.coeff (float)
        x: self.poly (list of Term or Tensor object)
        b: self.offset (float)
        r: self.exponent (int)
        j: self.index (list of str)
        Σ_i: self.operator (list)
        self.poly = [x, y, ...] represents products of each element.
        x_ij = x*y*...
    """

    def __init__(self, xlist,
                 coeff=1.0, offset=0.0, exponent=1,
                 operator=None):

        self.poly = xlist
        self.coeff = coeff
        self.offset = offset
        self.exponent = exponent
        self.index = set([])
        self.variables = {}
        self.num_elements = {}
        for x in xlist:
            self.index = self.index | x.index
            self.variables.update(x.variables)
            self.num_elements.update(x.num_elements)
        # for operator -------------------
        self.operator = operator
        if operator is not None:
            self.index = self.index-set(operator.index_labels)
        # ------------------- for operator

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __ladd__(self, other):
        return self.__add__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            self.offset += other
            return self
        else:
            return Expression([self, other])

    def __lmul__(self, other):
        return self.__mul__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            self.coeff *= other
            self.offset *= other
            return self
        else:
            return Term([self, other])

    def __pow__(self, other):
        self.exponent = other
        return self

    def __repr__(self):
        _vars = ''
        for t in self.poly:
            _vars += t.__str__()
        term = '{}'
        if self.operator is not None:
            term = self.operator.name + '(' + term + ')'
        if self.coeff != 1:
            repr_str = term.format('{}{}'.format(self.coeff, _vars))
        else:
            repr_str = term.format('{}'.format(_vars))
        if self.offset != 0.0:
            repr_str += '+' + str(self.offset)
        if self.exponent != 1:
            return '({})^{}'.format(repr_str, self.exponent)
        else:
            return repr_str

    def to_pyqubo(self, **kwargs):
        if self.operator is not None:
            return self.operator.to_pyqubo(self, **kwargs)

        poly = self._poly_to_pyqubo(**kwargs)
        if self.coeff != 1:
            return (self.coeff*poly + self.offset)**self.exponent
        else:
            return (poly + self.offset)**self.exponent

    def _poly_to_pyqubo(self, **kwargs):
        t = self.poly[0].to_pyqubo(**kwargs)
        for p in self.poly[1:]:
            t = t * p.to_pyqubo(**kwargs)
        return t

    def to_serializable(self):
        poly_seri = []
        for p in self.poly:
            p_seri = p.to_serializable()
            p_seri.pop('variables', None)
            p_seri.pop('num_elements', None)
            poly_seri.append(p_seri)
        express = [self.coeff,
                   {} if self.operator is None else self.operator.to_serializable(),
                   poly_seri, self.offset, self.exponent]
        return {'class': self.__class__.__name__,
                'model': express, 'index': list(self.index),
                'variables': self.variables, 'num_elements': self.num_elements}

    @classmethod
    def from_serializable(cls, obj):
        import jijcloud.modeling
        # model = [coeff, operator, poly, offset, exponent]
        model = obj['model']
        xlist = []
        for p in model[2]:
            if p['class'] == 'Term':
                x = Term.from_serializable(p)
            elif p['class'] == 'Expression':
                x = Expression.from_serializable(p)
            else:
                x = eval(
                    'jijcloud.modeling.{}.from_serializable(p)'.format(p['class']))
            xlist.append(x)
        operator = jijcloud.modeling.operator.Operator.from_serializable(
            model[1]
        )
        term = cls(xlist,
                   coeff=model[0],
                   operator=operator,
                   offset=model[3],
                   exponent=int(model[4]))
        return term


class Expression(Term):
    def __init__(self, terms, coeff=1.0, offset=0.0, exponent=1,
                 operator=None):
        super().__init__(terms, coeff=coeff, offset=offset,
                         exponent=exponent, operator=operator)

    def __repr__(self):
        repr_str = ''
        for p in self.poly:
            s = p.__str__()
            repr_str += s + '+'
        return repr_str[:-1]

    def _poly_to_pyqubo(self, **kwargs):
        t = self.poly[0].to_pyqubo(**kwargs)
        for p in self.poly[1:]:
            t = t + p.to_pyqubo(**kwargs)
        return t
