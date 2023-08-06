from __future__ import annotations

from colored import fg
from colored import stylize


def green(x: str) -> str:
    return stylize(x, fg("green"))


def red(x: str) -> str:
    return stylize(x, fg("red"))
