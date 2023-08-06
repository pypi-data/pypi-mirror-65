from __future__ import annotations

from typing import Any

from functional_predicates.predicate import Predicate


class Callable(Predicate):
    def __bool__(self: Callable) -> bool:
        return callable(self.value)

    def _get_repr_text(self: Callable) -> str:
        return f"callable({self.value!r})"

    def _get_str_text(self: Callable) -> str:
        return f"callable({self.value})"


class IsInstance(Predicate):
    def __init__(self: IsInstance, value: Any, cls: Any) -> None:
        super().__init__(value)
        self.cls = cls

    def __bool__(self: Callable) -> bool:
        return isinstance(self.value, self.cls)

    def _get_repr_text(self: Callable) -> str:
        return f"isinstance({self.value!r}, {self.cls!r})"

    def _get_str_text(self: Callable) -> str:
        return f"isinstance({self.value}, {self.cls})"
