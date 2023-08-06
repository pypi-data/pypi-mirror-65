from jijcloud.modeling.term import Term
import pyqubo as pyq


def Constraint(term, label, condition='== 0', multiplier=None):
    return Term([term], operator=ConstraintOperator(
        label, condition, multiplier))


class ConstraintOperator():
    name = 'Constraint'

    def __init__(self, label, condition='== 0', multiplier=None):
        self.label = label
        self.condition = condition
        self.index_labels = {}
        self.multiplier = multiplier
        self.info = {label: {'class': __class__.__name__,
                             'condition': condition,
                             'multiplier': multiplier}}

    def to_pyqubo(self, term, fixed_variables, **kwargs):
        # 添字が付いている状態に制約をつけた場合、
        # PyQUBOにするときにラベルに添字を追加する。
        key_str = '_' if len(kwargs) > 0 else ''
        for k, v in kwargs.items():
            key_str += k + str(v)
        pyq_model = term._poly_to_pyqubo(fixed_variables, **kwargs)
        return pyq.Constraint(pyq_model, label=self.label+key_str)

    def to_serializable(self):
        return [self.name, self.label, self.condition, self.multiplier]
