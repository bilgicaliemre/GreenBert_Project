# v14.1: five narrow guards from the humanizer audit (shipped)

Content hash `c8a3b4699a5ee62d` (v14: `3d7610372fb4faec`). Built from v14 by `scripts/v15/build_v141.py`; SKILL.md grows
from 3,366 to 3,462 words. DEVLOG section 26 has the full record.

Why: the user asked to merge popular GitHub humanizer skills into this one. A rule-by-rule audit of five of them
(529 rules) found that v14 already covered 53 percent, that 91 rules would make the skill invent facts, strengthen
claims, rewrite a person's text or game detectors, and that 7 new rules survived a skeptic. All 7 went into a
candidate, v15 (`../v15_not_shipped`). v15 changed nothing measurable on real edits, and on writing from notes judges
leaned toward v14 (60 percent of position-balanced blind pairs). v14.1 keeps only the five changes that do not touch
Write mode:

- Prose inside a file with code, commands, paths, URLs, YAML, LaTeX markup, citation keys or data: edit only the prose
  and leave the rest exactly as it is, dashes and hyphens included; write only the finished text into the file and
  give notes in the reply (from blader/humanizer).
- `tells.md` section 9: do not "fix" a tell the text is discussing ("delve" named as an example in a paper).
- `tells.md` section 9, plus a one-line pointer in Edit: the user's own informal text keeps its lowercase, short forms,
  fragments and emphatic stops (from blader/humanizer).
- `tells.md` T8: chatbot residue means an assistant's lines; a greeting, sign-off or "let me know by Friday" in the
  user's own message stays (from blader/humanizer).
- Integrity: the watermark sentence now says what Anthropic says: the mark is statistical, carried in word choice, with
  no hidden characters; stripping characters does not remove it, and the skill does not try.

Left out (in v15 only): the two-way edit diff and the writing-sample rule.

Tests (same runs, same judges as v14):
- Behavior probe on the v15 changes: v15 32 of 32, v14 29 of 32 (`eval/results/v15/probe_graded.json`).
- Writing from notes, 16 held-out briefs, two runs, 64 blind paired judgments: v14.1 against v14, p +0.1 [-1.0, +1.2],
  quality -0.06 [-0.27, +0.16], unsupported claims 0.00 [-0.41, +0.39]; position-balanced preference 49 to 51.
- Real edits: v14.1 was not run on its own; v15, which contains every v14.1 change plus two more, matched v14 on 48
  learner essays and 48 science-fair abstracts (judged own and meaning check).
