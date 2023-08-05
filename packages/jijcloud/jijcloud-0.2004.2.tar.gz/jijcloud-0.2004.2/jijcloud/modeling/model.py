from typing import Dict, Any


class Model():
    def __init__(self, term, fixed_vars=None):
        self.term = term
        self.fixed_vars = fixed_vars

        self.variables = {}
        self.placeholders = {}
        for k, var in term.variables.items():
            if var['var_type'] == 'variable':
                self.variables[k] = var
            elif var['var_type'] == 'placeholder':
                self.placeholders[k] = var

    def to_serializable(self) -> Dict[str, Any]:
        expression = self.term.to_serializable()
        return {
            'model': expression,
            'fixed_vars': self.fixed_vars,
            'variables': self.variables
        }
