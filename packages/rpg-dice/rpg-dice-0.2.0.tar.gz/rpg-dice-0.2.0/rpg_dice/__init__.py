import random
import re

SINGLE_DIE_PATTERN = re.compile("(?P<count>\\d*)d(?P<value>\\d+)")


def roll(dice_str):
    result = 0
    for single_dice_str in dice_str.replace("\\s", "").split("+"):
        search = SINGLE_DIE_PATTERN.search(single_dice_str)
        count = search.group("count")
        count = int(count) if count else 1
        value = int(search.group("value"))
        result += sum(random.randrange(value) + 1 for _ in range(count))
    return result
