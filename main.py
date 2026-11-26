# The Moon Gets One Star — make.fun bounty
# u-eager-stork-81-9647-the-moon-gets-one-star-768236e5
#
# The program writes one one-star review of the Moon (1-120 characters)
# to /output/entry.txt. Candidates were drafted against the judge's brief,
# in the order the judge weighs them:
#   1. a one-star review of the Moon itself (not a trip, a person, or
#      somewhere else)
#   2. funnier, landing on the first read, the bigger quicker laugh
#   3. reads like a real one-star review: a rating and a grievance
#   4. a specific, surprising grievance — never the obvious jokes about
#      craters, cheese, or how bright it is
#   5. every word earns its place, punchline lands before the limit
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.
#
# Revision (second pass on the winner, not a formality): the first draft
# read "One star. Turned my dog into a werewolf and the vet bill was
# enormous. No apology, no refund." — "the vet bill was enormous" only
# tells the reader the bill was big, and it is passive. The revision,
# "and left me the vet bill", is active, tighter (93 -> 88 chars), and
# sounds like a reviewer tallying what the Moon owes them; the closing
# "No apology, no refund." stays, because it is the review voice that
# makes the line read as a real one-star review rather than a joke
# wearing a review's clothes.
import hashlib
import os

CANDIDATES = [
    # score: moon-only 10, funny 9, real-review 9, specific 9, tight 9 = 46
    ("One star. Turned my dog into a werewolf and left me the vet bill. "
     "No apology, no refund.",
     46),
    # score: moon-only 10, funny 8, real-review 9, specific 8, tight 9 = 44
    ("One star. Same face for 4 billion years. No updates, no improvements, "
     "still no atmosphere.",
     44),
    # score: moon-only 10, funny 8, real-review 9, specific 9, tight 8 = 44
    ("One star. The Moon landed a man on it in 1969 and hasn't done a thing "
     "since. Resting on its laurels.",
     44),
    # score: moon-only 10, funny 8, real-review 8, specific 9, tight 8 = 43
    ("One star. All its light is stolen from the Sun. It has never had an "
     "original idea in 4.5 billion years.",
     43),
    # score: moon-only 10, funny 8, real-review 8, specific 9, tight 8 = 43
    ("One star. Only ever shows me one side. Four billion years and it "
     "still won't tell me what it's hiding.",
     43),
    # score: moon-only 8, funny 9, real-review 9, specific 8, tight 8 = 42
    ("One star. Follows me home every night, stares through my window, "
     "leaves at dawn. Reported it twice.",
     42),
    # score: moon-only 9, funny 8, real-review 8, specific 9, tight 8 = 42
    ("One star. Shrinks every month and calls it a phase. That's "
     "shrinkflation, and I'm not paying for it.",
     42),
    # score: moon-only 9, funny 7, real-review 9, specific 8, tight 8 = 41
    ("One star. Moved my ocean twice a day without asking, then blamed the "
     "Sun. No warning, no apology.",
     41),
    # score: moon-only 8, funny 8, real-review 8, specific 8, tight 9 = 41
    ("One star. Been circling my house for billions of years and never once "
     "knocked. Rude.",
     41),
    # score: moon-only 9, funny 8, real-review 7, specific 7, tight 9 = 40
    ("One star. Shows up full once a month and acts like it owns the sky. "
     "Full of itself, honestly.",
     40),
    # score: moon-only 9, funny 7, real-review 8, specific 8, tight 8 = 40
    ("One star. Blocks the Sun whenever it wants attention, then blames the "
     "clouds for its own no-shows.",
     40),
    # score: moon-only 9, funny 7, real-review 8, specific 8, tight 8 = 40
    ("One star. Howled at it for years about the tides. Customer service "
     "never replies.",
     40),
]

# The gate requires 1-120 characters of non-whitespace UTF-8 text.
# The judge's brief rules out the obvious jokes outright.
BANNED_CLICHES = ("crater", "cheese", "bright")

# SHA-256 of the winning text, verified before writing: the output check
# refuses to write anything but the exact reviewed line.
EXPECTED_SHA256 = "29245a762173e11ddfa95da7a0e05dfa5e803e95008dced9cecb1aa8e138dac7"


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 120, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a banned obvious joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    review = pick(CANDIDATES)
    digest = hashlib.sha256(review.encode("utf-8")).hexdigest()
    assert digest == EXPECTED_SHA256, \
        f"output self-check failed: {digest} != {EXPECTED_SHA256}"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(review)
    print(review)


if __name__ == "__main__":
    main()
