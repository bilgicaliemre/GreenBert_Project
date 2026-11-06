# v10.1: fidelity fix to the short-answer guide (shipped)

Content hash `3571b11768657399`. Same as v10 (see `../v10/CHANGELOG.md`) except `references/short-answers.md`:

- Rule 4 now says to state a conclusion "as strongly as the student holds them and no stronger": where the student
  is unsure, say so once, plainly; never turn an open question into a goal or a doubt into a certainty.
- New rule 5: add no "so", "because" or "which is why" link between facts the student gave separately, and no
  reason for a choice the student did not give.
- The final checklist gains a fact diff for goals, conclusions, feelings and causal links.

Why: in v10's held-out test the short-answer writer added more unsupported content than plain Claude (1.08 against
0.58 statements per answer, 4 of 12 answers clean against 5 of 12), mostly doubts turned into commitments by v10's
"whole-hearted" rule and added causal links. After the fix, on the same 12 test questions: 0.25 per answer, 10 of
12 clean; sentence length and contractions stayed close to v10's (17.9 words, 0.8 per 100 words).

Caveat: this check reused the test questions after I had read the v10 fidelity report, so it is not a clean
held-out result, and v10.1 was not re-judged for human-likeness (budget).
