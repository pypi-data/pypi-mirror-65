"""
Core functionality for working with the Kelly Criterion.
"""

from __future__ import division

from collections import Iterable
from itertools import chain, combinations

import numpy as np


# ----------------------------------------------------------------------------
# Utilities
# ----------------------------------------------------------------------------

def powerset(iterable):
    """
    Taken from itertools recipes:

    https://docs.python.org/2/library/itertools.html#itertools-recipes
    """
    range_of_items = range(1, len(iterable) + 1)
    combos = chain.from_iterable(combinations(iterable, r) for r in range_of_items)
    return list(combos)


# ----------------------------------------------------------------------------
# Odds
# ----------------------------------------------------------------------------

def american(odds):
    """
    Turn American odds into a probability.

    >>> american(-115)
    .5349

    >>> american(.524)
    -110
    """
    # The user actually wants probability here.
    if 0 < odds < 1:
        return probability(odds)

    odds = int(odds)
    if odds > 0:
        percent = 1.0 + (odds / 100.0)
    else:
        percent = 1.0 - (100.0 / odds)
    return round(1.0 / percent, 4)


def dec(odds):
    """
    Turn decimal odds into a probability.

    >>> dec(1.8)
    .5405
    """
    return round(1.0 / odds, 4)


def decimal(odds):
    """
    Turn decimal odds into a probability.

    >>> decimal(1.8)
    .5405
    """
    return round(1.0 / odds, 4)


def probability(percent, american_odds=True):
    """
    Turn a probability estimate into American odds.

    >>> probability(.55)
    -115
    """
    if percent > 1:
        raise Exception("Use a number between 0 and 1.")
    odds = round(1.0 / percent, 4)
    if american_odds:
        return int(dec_to_usa(odds))
    return odds


def usa(odds):
    """Shorthand for `american`"""
    return american(odds)


# ----------------------------------------------------------------------------
# Conversions
# ----------------------------------------------------------------------------

def dec_to_usa(odds):
    """
    Convert international odds to American format.

    >>> dec_to_usa(1.8)
    -125
    """
    if odds <= 1:
        raise Exception("Can't be less than 1.")
    if odds < 2:
        american_odds = -100 / (odds - 1)
    else:
        american_odds = (odds - 1) * 100
    return round(american_odds)


def usa_to_dec(odds):
    """
    Convert international odds to American format.

    >>> usa_to_dec(-125)
    1.8
    """
    if abs(odds) < 100:
        raise Exception("Can't be less than 100.")
    if odds > 0:
        dec_odds = 1 + (odds / 100)
    else:
        dec_odds = 1 - (100 / odds)
    return round(dec_odds, 4)


# ----------------------------------------------------------------------------
# Kelly Criterion
# ----------------------------------------------------------------------------

def bet(percent, odds, adjustment=1):
    """
    Kelly Criterion in Python with optional adjustment (Half Kelly, Quarter, etc.)

    >>> bet(.55, -110)
    .1
    """
    return kelly(percent, odds, adjustment)


def edge(percent, odds):
    """
    What is your edge -- given you have a probability and odds.

    >>> edge(.55, .5)
    """
    # Did the user supply actual probability odds or European decimal odds?
    if abs(odds) >= 100:
        odds = american(odds)
    if 1 < percent < 100:
        percent *= .01
    if odds < 1:
        odds = 1.0 / odds
    answer = percent * odds - 1.0
    return round(answer, 4)


def kelly(percent, odds, adjustment=1):
    """
    Kelly Criterion in Python with optional adjustment (Half Kelly, Quarter, etc.)

    >>> kelly(.55, -110)
    .1
    """
    # First, convert the odds.
    if abs(odds) >= 100:
        odds = american(odds)
    # Did the user forget that they should be percents?
    if 1 < percent < 100:
        percent *= .01
    if 1 < odds < 100:
        odds *= .01
    odds = 1.0 / odds
    # What is the edge?
    edge = odds * percent - 1.0
    # Compute the Kelly Criterion...
    amount = edge / (odds - 1.0)
    return round(amount * adjustment, 4)


def multiple(odds):
    """
    Kelly Criterion for multiple events at the same time. Make sure the odds are
    already calculated before using this function.

    >>> multiple([.1, .1, .3, .3, .1])
    [0.03951  0.03951  0.15291  0.15291  0.03951]
    """
    if isinstance(odds, Iterable) and isinstance(odds[0], Iterable):
        odds = [kelly(*game) for game in odds]
    number_of_items = len(odds)
    # Create the powerset combinations...
    values = [np.multiply.reduce(c) for c in powerset(odds)]
    indexes = powerset(range(number_of_items))
    # We have to keep track of parlay odds...
    parlay_odds = [0] * number_of_items
    for i, index in enumerate(indexes):
        # Exclude single elements.
        if i < number_of_items:
            continue
        # Calculate parlay possibilities for odd numbers of events.
        elif len(index) % 2:
            for n in index:
                parlay_odds[n] += values[i]
        # Otherwise, calculate the odds for the given events.
        else:
            for n in index:
                values[n] -= values[i]
    # Modified Kelly Criterion probabilities...
    odds = values[:number_of_items]
    modified = np.array(odds) + np.array(parlay_odds)
    return modified
