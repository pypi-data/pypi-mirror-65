from unittest.mock import patch, call

from rpg_dice import roll


@patch("random.randrange")
def test_1d6(randrange):
    randrange.side_effect = [4]
    assert roll("1d6") == 5
    randrange.assert_called_with(6)


@patch("random.randrange")
def test_2d6(randrange):
    randrange.side_effect = [4, 2]
    assert roll("2d6") == 8
    randrange.assert_has_calls([call(6), call(6)])


@patch("random.randrange")
def test_default_number_of_dice_is_1(randrange):
    randrange.side_effect = [3]
    assert roll("d6") == 4
    randrange.assert_called_with(6)


@patch("random.randrange")
def test_1d20(randrange):
    randrange.side_effect = [17]
    assert roll("1d20") == 18
    randrange.assert_called_with(20)


@patch("random.randrange")
def test_1d2(randrange):
    randrange.side_effect = [1]
    assert roll("1d2") == 2
    randrange.assert_called_with(2)


def test_1d1():
    """ This one isn't really random, 1d1 will always return 1 """
    assert roll("1d1") == 1
