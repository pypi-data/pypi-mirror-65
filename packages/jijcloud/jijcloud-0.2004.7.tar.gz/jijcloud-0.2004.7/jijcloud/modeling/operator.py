from jijcloud.modeling.constraint import ConstraintOperator
from jijcloud.modeling.sum import SumOperator
from jijcloud.modeling import Term


class Operator():

    @classmethod
    def from_serializable(cls, obj):
        if len(obj) == 0:
            return None
        class_name = obj[0]
        if class_name == 'Constraint':
            return ConstraintOperator(*obj[1:])
        elif class_name == 'Sum':
            return SumOperator.from_serializable(obj)
        else:
            raise ValueError("Operator: '{}' is unavailable.".format(obj[0]))
