from jijcloud.modeling.term import Term
import pyqubo as pyq


def Constraint(term, label, condition='== 0'):
    return Term([term], operator=ConstraintOperator(label, condition))


class ConstraintOperator():
    name = 'Constraint'

    def __init__(self, label, condition='== 0'):
        self.label = label
        self.condition = condition
        self.index_labels = {}

    def to_pyqubo(self, term, **kwargs):
        pyq_model = term._poly_to_pyqubo(**kwargs)
        return pyq.Constraint(pyq_model, label=self.label)

    def to_serializable(self):
        return [self.name, self.label, self.condition]
