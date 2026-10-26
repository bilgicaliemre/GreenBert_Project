# Human-anchored benchmark scripts

Methods for DEVLOG section 21. The essays themselves are not in this repository: they are real students' essays
that colleges published as examples, so they stay private (copyright, and the writers are real people). The
reverse-engineered notes and the model-written versions are derived from them and stay private for the same reason.

Pipeline:
1. `hc_gen.js` (workflow): for each admitted essay, write the counselor's interview notes the student would have
   given before writing (facts, quotes and feelings, regrouped, no run of more than six words copied), then write
   the essay from the notes alone three ways: plain model (P), word list (L), skill (F).
   `hc_fill.js` writes missing versions from existing notes (never regenerates notes) and adds the v8 skill (G).
2. `pile.py`: normalizes every version (straight quotes, single spaces, no title) under a random file name and
   builds reading piles of four essays by four different students, a fresh random set per judge.
3. `hc_pile_judge.js` (workflow): each judge reads one pile, told any mix of real and AI is possible, and gives each
   essay a probability that a real student wrote it, a quality score and the evidence.
4. `pile_analyze.py`: per version, mean probability, AUC against the real essays (0.5 = indistinguishable), quality,
   and paired differences against the same student's real essay.

`hc_judge.js`, `anonymize.py` and `hc_analyze.py` are the first design (find the real essay among four versions of
one story). It was dropped because the three model versions share paraphrases from the same notes, which gives the
real essay away; see DEVLOG section 21.
