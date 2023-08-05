# RPG Dice

[![Build Status](https://travis-ci.org/pfertyk/rpg-dice.svg?branch=master)](https://travis-ci.org/pfertyk/rpg-dice)

A simple dice parser for RPG sessions. Turns strings like `2d6 + d20` into
dice roll results.

## Installation

```
pip install rpg-dice
```

## Usage

```python
from rpg_dice import roll
results = roll("2d6")
results = roll("2d6 + d20")
```
