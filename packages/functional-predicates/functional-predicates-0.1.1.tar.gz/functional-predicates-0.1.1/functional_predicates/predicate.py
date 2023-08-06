from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any

from functional_predicates.colors import green
from functional_predicates.colors import red


class Predicate(ABC):
    def __init__(self: Predicate, value: Any) -> None:
        self.value = value

    @abstractmethod
    def __bool__(self: Predicate) -> bool:
        raise NotImplementedError

    def __repr__(self: Predicate) -> str:
        return self._colored(self._get_repr_text())

    @abstractmethod
    def _get_repr_text(self: Predicate) -> str:
        raise NotImplementedError

    def __str__(self: Predicate) -> str:
        return self._colored(self._get_str_text())

    @abstractmethod
    def _get_str_text(self: Predicate) -> str:
        raise NotImplementedError

    def _colored(self: Predicate, x: str) -> str:
        if self:
            return green(x)
        else:
            return red(x)
