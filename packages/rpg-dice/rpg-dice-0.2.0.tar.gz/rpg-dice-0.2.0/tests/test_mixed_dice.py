from unittest.mock import patch, call

from rpg_dice import roll


@patch("random.randrange")
def test_2d6_2d8(randrange):
    randrange.side_effect = [4, 5, 1, 7]
    assert roll("2d6 + 2d8") == 21
    randrange.assert_has_calls(
        [call(6), call(6), call(8), call(8)], any_order=True
    )


@patch("random.randrange")
def test_d6_d20_ignores_multiple_spaces(randrange):
    randrange.side_effect = [3, 15]
    assert roll("d6     +   d20") == 20
    randrange.assert_has_calls([call(6), call(20)], any_order=True)


@patch("random.randrange")
def test_d6_d20_works_without_spaces(randrange):
    randrange.side_effect = [3, 15]
    assert roll("d6+d20") == 20
    randrange.assert_has_calls([call(6), call(20)], any_order=True)


@patch("random.randrange")
def test_d4_d12_without_spaces(randrange):
    randrange.side_effect = [2, 9]
    assert roll("d4 + d12") == 13
    randrange.assert_has_calls([call(4), call(12)], any_order=True)


@patch("random.randrange")
def test_1d2_2d4_3d6(randrange):
    randrange.side_effect = [1, 1, 3, 2, 5, 4]
    assert roll("1d2 + 2d4 + 3d6") == 22
    randrange.assert_has_calls(
        [call(2), call(4), call(4), call(6), call(6), call(6)], any_order=True
    )
