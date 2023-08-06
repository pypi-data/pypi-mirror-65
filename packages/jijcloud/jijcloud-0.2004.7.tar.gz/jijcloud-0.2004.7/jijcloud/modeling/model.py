from typing import Dict, Any
from jijcloud.modeling import Term, Expression


class Model():
    def __init__(self, expression,
                 fixed_vars: dict = {},
                 multipliers: dict = None):
        # QUBO Model (Expression or Term class)
        self.expression = expression

        # fixed variables
        # Ex.
        # {'x': {(0, 1): 1, ...}}
        # {'y': {1: 0, 2: 1, ...}}
        self.fixed_vars = fixed_vars

        # lagrange multiplier
        # key: multiplier's name
        # value: constraint's name
        self.multipliers = multipliers

        self.variables = {}
        self.placeholders = {}
        for k, var in expression.variables.items():
            if var['var_type'] == 'variable':
                self.variables[k] = var
            elif var['var_type'] == 'placeholder':
                self.placeholders[k] = var

    def to_pyqubo(self, fixed_vars: dict = None):
        if fixed_vars is not None:
            _fixed_vars = fixed_vars
            self.fixed_vars = fixed_vars
        elif self.fixed_vars is not None:
            _fixed_vars = self.fixed_vars
        else:
            raise ValueError('need fixed_vars.')
        expression = self.expression.to_pyqubo(_fixed_vars)
        return expression

    def to_serializable(self) -> Dict[str, Any]:
        expression = self.expression.to_serializable()
        return {
            'model': expression,
            'fixed_vars': self.fixed_vars,
            'variables': self.variables,
            'multipliers': self.multipliers
        }

    @classmethod
    def from_serializable(cls, obj: dict):
        if obj['model']['class'] == 'Term':
            qubo_eq = Term.from_serializable(obj['model'])
        elif obj['model']['class'] == 'Expression':
            qubo_eq = Expression.from_serializable(obj['model'])

        model = cls(
            qubo_eq,
            fixed_vars=obj['fixed_vars'],
            multipliers=obj['multipliers'])

        return model

    def decode_solution(self, sample: dict):
        sol = {}

        def put_value_with_keys(dict_body, keys, value):
            for key in keys[:-1]:
                if key not in dict_body:
                    dict_body[key] = {}
                dict_body = dict_body[key]
            dict_body[keys[-1]] = value

        for k, v in sample.items():
            name = k.split('[')[0]
            ind_key = k[len(name):]
            indices = [name]+[int(k[1:]) for k in ind_key.split(']')[:-1]]
            put_value_with_keys(sol, indices, v)

        for var, v in self.fixed_vars.items():
            for k, s in v.items():
                if isinstance(k, int):
                    k = [k]
                keys = [var] + list(k)
                put_value_with_keys(sol, keys, s)

        return sol
