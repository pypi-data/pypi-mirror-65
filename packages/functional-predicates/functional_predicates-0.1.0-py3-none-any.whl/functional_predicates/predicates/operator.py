from __future__ import annotations

from operator import eq
from operator import ge
from operator import gt
from operator import le
from operator import lt
from operator import ne
from typing import Any
from typing import Callable

from functional_predicates.predicate import Predicate


class Comparison(Predicate):
    def __init__(self: LT, value: Any, other: Any, operator: Callable[[Any, Any], bool]) -> None:
        super().__init__(value)
        self.operator = operator
        self.infix = {lt: "<", le: "<=", eq: "==", ne: "!=", ge: ">=", gt: ">"}[self.operator]
        self.other = other

    def __bool__(self: Comparison) -> bool:
        return self.operator(self.value, self.other)

    def _get_repr_text(self: Comparison) -> str:
        return f"{self.value!r} {self.infix} {self.other!r}"

    def _get_str_text(self: Comparison) -> str:
        return f"{self.value} {self.infix} {self.other}"


class LT(Comparison):
    def __init__(self: LT, value: Any, other: Any) -> None:
        super().__init__(value, other, lt)


class LE(Comparison):
    def __init__(self: LE, value: Any, other: Any) -> None:
        super().__init__(value, other, le)


class Eq(Comparison):
    def __init__(self: Eq, value: Any, other: Any) -> None:
        super().__init__(value, other, eq)


class NE(Comparison):
    def __init__(self: NE, value: Any, other: Any) -> None:
        super().__init__(value, other, ne)


class GE(Comparison):
    def __init__(self: GE, value: Any, other: Any) -> None:
        super().__init__(value, other, ge)


class GT(Comparison):
    def __init__(self: GT, value: Any, other: Any) -> None:
        super().__init__(value, other, gt)
