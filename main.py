#!/usr/bin/env python3
"""The Battery's Last Text to Its Charger (make.fun).

Writes exactly one line of plain text to /output/entry.txt: the phone
battery's final message to the charger it waited for all day.

The program scores a few candidate lines on the judge's own criteria, in
the order the judge weighs them (a real joke with a turn that pays off in
the final words first, then a voice a person would actually type, then
spending the 200 characters well, then an angle beyond the obvious dying
complaint), and writes the winner. Scores are fixed judgements, not data
read from anywhere else: the entry must be self-contained.
"""

import os

# Judge's criteria, in the order the judge weighs them. Weights: a payoff
# in the final words 5, a real typed voice (neediness or spite) 4, using
# the characters well 3, a fresh angle 2. On-topic-ness is satisfied by
# construction: every candidate is the battery's last text to its charger.
WEIGHTS = {"payoff": 5, "voice": 4, "economy": 3, "angle": 2}

CANDIDATES = {
    # A: spite with a threat as the payoff. The battery waited, the
    # earbuds got the charger instead, and the last word is revenge:
    # your alarms die with me. Short, typed like a real text.
    "A": {
        "text": "hey. 1%. you left me on 4% all afternoon so your "
                "earbuds could live. i hope the lamp was worth it. "
                "goodbye, i'm taking your alarms with me.",
        "payoff": 9, "voice": 9, "economy": 8, "angle": 8,
    },
    # B: loyal-dog setup, but the ending trails off into a shrug
    # instead of landing a punchline. Sad-cute more than funny.
    "B": {
        "text": "1% left. i waited all day by the outlet like a dog at "
                "the door and you picked the lamp. tell the wifi i loved "
                "it. don't cry. just plug me in. too late.",
        "payoff": 5, "voice": 7, "economy": 6, "angle": 6,
    },
    # C: doomscroll setup with the same alarm threat, but the closing
    # "your move, charger" spends the last words on a dare instead of
    # the joke itself, and the line runs longer for the same payoff.
    "C": {
        "text": "it's me, your battery. 1%. i held on all day so you "
                "could doomscroll in bed. plug me in or i'm taking your "
                "6am alarm down with me. your move, charger.",
        "payoff": 7, "voice": 8, "economy": 6, "angle": 7,
    },
}


def score(candidate):
    """Weighted total for one candidate on the judge's criteria."""
    return sum(WEIGHTS[key] * candidate[key] for key in WEIGHTS)


def pick_line():
    """Return the text with the highest weighted score.

    Ties break toward the earlier candidate (A before B before C),
    matching the competition's own tie-break spirit: first wins.
    """
    best = None
    best_score = None
    for key in sorted(CANDIDATES):
        total = score(CANDIDATES[key])
        if best_score is None or total > best_score:
            best = CANDIDATES[key]["text"]
            best_score = total
    return best


def main():
    line = pick_line()
    out_path = "/output/entry.txt"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    # Read it back and verify the gate before finishing: UTF-8 text of
    # 1 to 200 characters, not only white space, exactly one line. A
    # failed write must fail loudly here, not silently reach the judge
    # as an invalid entry.
    with open(out_path, "rb") as f:
        written = f.read()
    text = written.decode("utf-8")
    if not 1 <= len(text) <= 200 or not text.strip() or "\n" in text:
        raise SystemExit("entry.txt failed the gate: %r" % written)
    return line


if __name__ == "__main__":
    print(main())
