# Kelly Criterion

An exercise in coding the Kelly Criterion in readable Python code.


## Examples

```python
import kelly

# I know I have an edge...
probability = .55
odds = -110

# What should the odds be?
kelly.usa(.55)

# And what do the current odds say the probability is?
kelly.usa(-110)

# How much of my bankroll should I wager?
kelly.bet(probability, odds)

# What about fractional Kelly?
kelly.bet(probability, odds, .25)

# Okay, but there's multiple events in which I have an edge...
games = [(.55, -110), (.55, -115), (.55, -105)]
kelly.multiple(games)
```
