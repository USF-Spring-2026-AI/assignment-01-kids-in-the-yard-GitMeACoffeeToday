"""
Utility functions for family tree simulation.
"""

import random


def decade_from_year(year: int) -> str:
    """Convert year to decade string."""
    decade = (year // 10) * 10
    return f"{decade}s"


def weighted_choice(items, weights):
    """Return random item using weighted probability."""
    return random.choices(items, weights=weights, k=1)[0]


def clamp(value, minimum, maximum):
    """Clamp value between minimum and maximum."""
    return max(minimum, min(maximum, value))