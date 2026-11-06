# v11: a stricter Edit mode

Frozen before any held-out output was generated: content hash `cdda4484b09a1155`. Same as v10.1 (see
`../v10.1/CHANGELOG.md`) except the Edit-mode paragraph of SKILL.md:

- Make the minimum effective edit even when the user asks to "improve" the text: fix outright errors and anything
  that blocks meaning, cut clear AI tells, and keep everything else.
- Add no transitions, thesis preview, definitions, examples, statistics, appeals to authority, idioms or reasons
  the writer did not give, and never make a claim stronger.
- Do not make a non-native writer's grammatical phrasing native.
- List up to five bigger changes after the text for the writer to decide on, instead of making them.
- A learner's practice or graded essay goes to Coach.

Why: in the edit benchmark (DEVLOG section 24), v10.1's "improve it" edits of real English-learner essays were
judged the student's own in only 3% of ratings. Judges named template transitions, definitions and authorities the
student had not written, native idioms and uniformly clean grammar. The new paragraph was written from the
development halves only.

Held-out result (test halves; v11 against v10.1 on "improve it", paired over texts, points of p(written by the
person)): appeals +4.1 [+2.3, +6.1]; abstracts +0.2 [-3.1, +3.6]; learner essays +1.8 [-6.1, +10.7]. On "fix the
grammar": abstracts +2.5 [+0.4, +4.8]. The blind meaning check improved in all three genres: edits that changed no
statement rose from 6% to 44% (abstracts), 40% to 100% (appeals) and 0% to 44% (learner essays), and voice kept rose
from 6.9 to 8.9 of 10 on learner essays. Judged quality of "improve" edits fell by 0.12 to 0.56 points.
