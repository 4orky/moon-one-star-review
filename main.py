#!/usr/bin/env python3
"""One-star Moon review: pick the strongest hand-written line, verify it, write it.
Twelve drafts were written by hand and graded on five counts, in the order
the bounty brief weighs them: the review must target the Moon alone, it must
amuse on first reading, it must sound like a real one-star review, its
complaint must be specific and fresh instead of the obvious crater, cheese
and brightness gags, and it must waste no words. The top draft scored 46 of
50. A second pass then sharpened it: the early wording reported the vet bill
as enormous, which only states a size; the shipped wording has the Moon
leaving the reviewer the bill, which is shorter, active, and reads like a
customer totalling up what they are owed.
"""
import sys
from hashlib import sha256
from pathlib import Path
TARGET = Path("/output/entry.txt")
CEILING = 120
FORBIDDEN = frozenset({"crater", "cheese", "bright"})
WANT_HEAD = "29245a762173e11ddfa95da7a0e05dfa5"
WANT_TAIL = "e803e95008dced9cecb1aa8e138dac7"
class Entry:
    def __init__(self, bits, marks):
        self.text = "".join(bits)
        self.marks = marks
    def total(self):
        return sum(self.marks)
    def rank(self):
        return (self.total(), -len(self.text))
def _check(entry):
    body = entry.text
    if not body.strip():
        raise ValueError("empty candidate rejected")
    if len(body) > CEILING:
        raise ValueError("candidate exceeds 120 characters: %d" % len(body))
    lowered = body.casefold()
    for word in FORBIDDEN:
        if word in lowered:
            raise ValueError("candidate leans on a banned cliche: %s" % word)
def _choose(pool):
    checked = []
    for entry in pool:
        _check(entry)
        checked.append(entry)
    checked.sort(key=lambda item: item.rank(), reverse=True)
    return checked[0]
POOL = [
    Entry(("One star. Turned ", "my dog into a werewolf ", "and left me the vet bill. ", "No apology, no refund."), (10, 9, 9, 9, 9)),
    Entry(("One star. Same face ", "for 4 billion years. No updates, ", "no improvements, still no atmosphere."), (10, 8, 9, 8, 9)),
    Entry(("One star. The Moon landed ", "a man on it in 1969 and hasn't ", "done a thing since. Resting on its laurels."), (10, 8, 9, 9, 8)),
    Entry(("One star. All its light ", "is stolen from the Sun. It has ", "never had an original idea in 4.5 billion years."), (10, 8, 8, 9, 8)),
    Entry(("One star. Only ever ", "shows me one side. Four billion ", "years and it still won't tell me what it's hiding."), (10, 8, 8, 9, 8)),
    Entry(("One star. Follows me ", "home every night, stares through ", "my window, leaves at dawn. Reported it twice."), (8, 9, 9, 8, 8)),
    Entry(("One star. Shrinks ", "every month and calls it a phase. ", "That's shrinkflation, and I'm not paying for it."), (9, 8, 8, 9, 8)),
    Entry(("One star. Moved my ", "ocean twice a day without asking, ", "then blamed the Sun. No warning, no apology."), (9, 7, 9, 8, 8)),
    Entry(("One star. Been circling ", "my house for billions of years ", "and never once knocked. Rude."), (8, 8, 8, 8, 9)),
    Entry(("One star. Shows up full ", "once a month and acts like it ", "owns the sky. Full of itself, honestly."), (9, 8, 7, 7, 9)),
    Entry(("One star. Blocks the Sun ", "whenever it wants attention, then ", "blames the clouds for its own no-shows."), (9, 7, 8, 8, 8)),
    Entry(("One star. Howled at it ", "for years about the tides. ", "Customer service never replies."), (9, 7, 8, 8, 8)), ]
def run():
    winner = _choose(POOL)
    seen = sha256(winner.text.encode("utf-8")).hexdigest()
    if seen != WANT_HEAD + WANT_TAIL:
        raise SystemExit("hash mismatch: got %s" % seen)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(winner.text, encoding="utf-8")
    back = TARGET.read_text(encoding="utf-8")
    if back != winner.text:
        raise SystemExit("round-trip mismatch after write")
    sys.stdout.write(winner.text + "\n")
run()
