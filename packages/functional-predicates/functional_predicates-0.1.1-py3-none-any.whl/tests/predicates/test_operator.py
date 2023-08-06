from __future__ import annotations

from re import escape

from pytest import raises

from functional_predicates import Check
from functional_predicates.colors import red


# comparisons


def test_lt() -> None:
    assert Check(0).lt(1).lt(2)
    with raises(AssertionError, match=escape(red("0 < 0"))):
        assert Check(0).lt(0)


def test_le() -> None:
    assert Check(0).le(0).le(1)
    with raises(AssertionError, match=escape(red("0 <= -1"))):
        assert Check(0).le(-1)


def test_eq() -> None:
    assert Check(0).eq(0)
    with raises(AssertionError, match=escape(red("0 == 1"))):
        assert Check(0).eq(1)


def test_ne() -> None:
    assert Check(0).ne(1).ne(-1)
    with raises(AssertionError, match=escape(red("0 != 0"))):
        assert Check(0).ne(0)


def test_ge() -> None:
    assert Check(0).ge(0).ge(-1)
    with raises(AssertionError, match=escape(red("0 >= 1"))):
        assert Check(0).ge(1)


def test_gt() -> None:
    assert Check(0).gt(-1).gt(-2)
    with raises(AssertionError, match=escape(red("0 > 0"))):
        assert Check(0).gt(0)
