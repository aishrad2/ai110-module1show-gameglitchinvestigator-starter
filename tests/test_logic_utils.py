"""Unit tests for the core game logic in logic_utils.py.

One test group per public function. These lock in the behaviour after the
three bug fixes: difficulty ranges, input validation, and hint direction.
"""

import pytest

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


# ---------------------------------------------------------------------------
# get_range_for_difficulty
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "difficulty, expected",
    [
        ("Easy", (1, 20)),
        ("Normal", (1, 50)),
        ("Hard", (1, 100)),
    ],
)
def test_range_per_difficulty(difficulty, expected):
    assert get_range_for_difficulty(difficulty) == expected


def test_range_widens_as_difficulty_increases():
    # The original bug: Hard was narrower (easier) than Normal.
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert easy_high < normal_high < hard_high


def test_unknown_difficulty_falls_back_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 50)


# ---------------------------------------------------------------------------
# parse_guess
# ---------------------------------------------------------------------------

def test_parse_guess_accepts_whole_number():
    assert parse_guess("42", 1, 50) == (True, 42, None)


def test_parse_guess_strips_whitespace():
    assert parse_guess("  7  ", 1, 50) == (True, 7, None)


@pytest.mark.parametrize("bound", [1, 50])
def test_parse_guess_accepts_both_bounds(bound):
    ok, value, err = parse_guess(str(bound), 1, 50)
    assert (ok, value, err) == (True, bound, None)


@pytest.mark.parametrize("raw", [None, "", "   "])
def test_parse_guess_rejects_empty_input(raw):
    ok, value, err = parse_guess(raw, 1, 50)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."


@pytest.mark.parametrize("raw", ["5.7", "abc", "1e3", "--3", "5 7"])
def test_parse_guess_rejects_non_whole_numbers(raw):
    # Decimals used to be silently truncated ("5.7" -> 5).
    ok, value, err = parse_guess(raw, 1, 50)
    assert ok is False
    assert value is None
    assert err is not None


@pytest.mark.parametrize("raw", ["0", "-3", "51", "9999"])
def test_parse_guess_rejects_out_of_range(raw):
    ok, value, err = parse_guess(raw, 1, 50)
    assert ok is False
    assert value is None
    assert err == "Guess must be between 1 and 50."


def test_parse_guess_range_message_uses_given_bounds():
    _, _, err = parse_guess("500", 1, 100)
    assert err == "Guess must be between 1 and 100."


# ---------------------------------------------------------------------------
# check_guess
# ---------------------------------------------------------------------------

def test_check_guess_win():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_check_guess_too_high_points_lower():
    # The original bug: "Too High" told the player to go HIGHER.
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_check_guess_too_low_points_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


@pytest.mark.parametrize(
    "guess, secret, expected",
    [
        (9, 50, "Too Low"),   # string comparison would call "9" > "50" True
        (50, 9, "Too High"),
        (100, 99, "Too High"),
        (1, 2, "Too Low"),
    ],
)
def test_check_guess_compares_numerically_not_as_strings(guess, secret, expected):
    outcome, _ = check_guess(guess, secret)
    assert outcome == expected


# ---------------------------------------------------------------------------
# update_score
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "attempt_number, expected_points",
    [
        (0, 90),   # 100 - 10 * 1
        (1, 80),
        (4, 50),
        (8, 10),   # 100 - 10 * 9 == 10, right at the floor
    ],
)
def test_win_awards_fewer_points_for_later_attempts(attempt_number, expected_points):
    assert update_score(0, "Win", attempt_number) == expected_points


@pytest.mark.parametrize("attempt_number", [9, 12, 100])
def test_win_points_never_drop_below_ten(attempt_number):
    assert update_score(0, "Win", attempt_number) == 10


def test_win_adds_to_existing_score():
    assert update_score(25, "Win", 0) == 115


def test_too_low_always_costs_five():
    assert update_score(20, "Too Low", 1) == 15
    assert update_score(20, "Too Low", 2) == 15


def test_too_high_on_even_attempt_adds_five():
    # Quirk of the current scoring rule, pinned so a change is deliberate.
    assert update_score(20, "Too High", 2) == 25


def test_too_high_on_odd_attempt_subtracts_five():
    assert update_score(20, "Too High", 3) == 15


def test_unknown_outcome_leaves_score_unchanged():
    assert update_score(42, "Quit", 1) == 42


def test_score_can_go_negative():
    assert update_score(0, "Too Low", 1) == -5
