from __future__ import annotations

from re import escape

from pytest import raises

from functional_predicates import Check
from functional_predicates.colors import red


def test_callable() -> None:
    def func() -> None:
        pass

    assert Check(func).callable()
    assert Check(lambda x: x).callable()
    with raises(AssertionError, match=escape(red("callable(0)"))):
        assert Check(0).callable()


def test_isinstance() -> None:
    assert Check(0).isinstance(int)
    with raises(AssertionError, match=escape(red("isinstance(0, <class 'float'>)"))):
        assert Check(0).isinstance(float)
