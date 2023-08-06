import re
import operator
import itertools

# TODO: Switch


class ConditionEvaluationResult(object):
    def __init__(self, name, result):
        self.name = name
        self.result = result

    def __repr__(self):
        return "%s: %s" % (self.name, self.result)

    def __eq__(self, other):
        return other.name == self.name and other.result == self.result


class Condition(object):
    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __xor__(self, other):
        return Xor(self, other)

    def __invert__(self):
        return Invert(self)

    def __call__(self, *args, **kwargs):
        return self.is_satisfied(*args, **kwargs)

    def __repr__(self):
        return self.__class__.__name__

    def is_satisfied(self, *args, **kwargs):
        pass

    def evaluate(self, *args, **kwargs):
        return [ConditionEvaluationResult(repr(self), self.is_satisfied(*args, **kwargs))]


class Composite(Condition):
    logic_operator = None

    def __init__(self, *args):
        self.conditions = args

    def __repr__(self):
            nested_conditions_reprs = [repr(condition) for condition in self.conditions]
            joiner = " %s " % self._logic_operator_str
            if len(nested_conditions_reprs) > 1:
                r = "(%s)" % joiner.join(nested_conditions_reprs)
                return self._repr_fix(r)
            else:
                r = "(%s %s)" % (joiner, nested_conditions_reprs[0])
                return self._repr_fix(r)

    def _repr_fix(self, repr_str):
        return re.sub('\s+', ' ', repr_str).replace("( ", "(")

    def is_satisfied(self, *args, **kwargs):
        partial_results = [condition(*args, **kwargs) for condition in self.conditions]
        return self.logic_operator(*partial_results)

    @property
    def _logic_operator_str(self):
        return self.logic_operator.__name__.replace("_", "")

    def evaluate(self, *args, **kwargs):
        nested_results = [condition.evaluate(*args, **kwargs) for condition in self.conditions]
        flat_results = list(itertools.chain.from_iterable(nested_results))
        return flat_results + [ConditionEvaluationResult(repr(self), self.is_satisfied(*args, **kwargs))]


class And(Composite):
    logic_operator = operator.and_


class Or(Composite):
    logic_operator = operator.or_


class Xor(Composite):
    logic_operator = operator.xor


class Invert(Composite):
    logic_operator = operator.not_


