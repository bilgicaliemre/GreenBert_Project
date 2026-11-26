# v15 (tested, not shipped): the seven survivors of the humanizer audit

Content hash `f0e22bd800926879`. Built from v14 by `scripts/v15/build_v15.py`; SKILL.md 3,366 to 3,699 words.

The seven changes: the five in v14.1 (see `../v14.1/CHANGELOG.md`) plus

- an edit diff that checks both directions: every claim, hedge, number, name, date and quote of the user's version stays
  or is named as a cut, joined sentences add no order, ranking, cause or "same time", and every difference needs a reason
  (from blader/humanizer and conorbronsdon/avoid-ai-writing);
- matching the countable habits of a writing sample the user says is theirs, in Write and Edit (from blader/humanizer).

Results (DEVLOG section 26):
- Real edits, same run as a second v14 sample: learner essays judged own 35 percent against 36 (difference -0.3
  [-4.4, +3.3]); abstracts 98 against 100 (-0.3 [-2.5, +1.7]); statements added, removed and changed within the range
  of the two v14 runs.
- Behavior probe: 32 of 32 against v14's 29 of 32.
- Writing from notes, 64 blind paired judgments: p -0.7 [-1.6, +0.1], quality -0.16 [-0.39, +0.08]; v14 preferred in 60
  percent of position-balanced pairs (raw count 40 of 64, inflated by an unbalanced slot order, see DEVLOG 26).

Not shipped: no measured gain on real text, a lean against it on writing, and 333 more words in the file that loads
every time.
