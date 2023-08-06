from __future__ import annotations

from itertools import chain
from typing import Any
from typing import List

from functional_predicates.predicate import Predicate
from functional_predicates.predicates.operator import Eq
from functional_predicates.predicates.operator import GE
from functional_predicates.predicates.operator import GT
from functional_predicates.predicates.operator import LE
from functional_predicates.predicates.operator import LT
from functional_predicates.predicates.operator import NE
from functional_predicates.predicates.types import Callable
from functional_predicates.predicates.types import IsInstance


class Check:
    def __init__(self: Check, value: Any) -> None:
        self.value = value
        self.predicates: List[Predicate] = []

    def __bool__(self: Check) -> bool:
        return all(self.predicates)

    def __repr__(self: Check) -> str:
        return ", ".join(map(repr, self.predicates))

    def __str__(self: Check) -> str:
        return ", ".join(map(str, self.predicates))

    # operator - comparisons

    def lt(self: Check, x: Any) -> Check:
        return self._append(LT(self.value, x))

    def le(self: Check, x: Any) -> Check:
        return self._append(LE(self.value, x))

    def eq(self: Check, x: Any) -> Check:
        return self._append(Eq(self.value, x))

    def ne(self: Check, x: Any) -> Check:
        return self._append(NE(self.value, x))

    def ge(self: Check, x: Any) -> Check:
        return self._append(GE(self.value, x))

    def gt(self: Check, x: Any) -> Check:
        return self._append(GT(self.value, x))

    # types

    def callable(self: Check) -> Check:  # noqa: A003
        return self._append(Callable(self.value))

    def isinstance(self: Check, cls: Any) -> Check:  # noqa: A003
        return self._append(IsInstance(self.value, cls))

    # private

    def _append(self: Check, x: Predicate) -> Check:
        self.predicates = list(chain(self.predicates, [x]))
        return self


#
