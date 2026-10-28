def get_range_for_difficulty(difficulty: str):
    """Return the (low, high) range of secret numbers for a difficulty.

    Fix: Normal and Hard had their ranges swapped, so Hard (1-50) was
    easier than Normal (1-100). Ranges now widen as difficulty increases:
    Easy 1-20, Normal 1-50, Hard 1-100.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str, low: int, high: int):
    """Validate raw text input and convert it to an int guess.

    Returns (ok, value, error_message).

    Fix: improper input used to be accepted. Decimals like "5.7" were
    silently truncated to 5, and numbers outside the difficulty range
    (including negatives) were allowed. Now only whole numbers are
    accepted, surrounding whitespace is ignored, and the guess must fall
    within [low, high].
    """
    if raw is None:
        return False, None, "Enter a guess."

    raw = raw.strip()
    if raw == "":
        return False, None, "Enter a guess."

    try:
        value = int(raw)
    except ValueError:
        return False, None, "Enter a whole number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """Compare a guess to the secret and return (outcome, hint message).

    Fix: the hints were backwards ("Too High" told the player to go
    HIGHER). Also, the caller turned the secret into a string on every
    even attempt, which forced string comparison ("9" > "50" is True)
    and produced wrong hints. Both values are now always ints, the hint
    messages point the right way, and the string fallback was removed.
    """
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
