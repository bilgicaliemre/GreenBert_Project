# v13: the mode table moves to the end of SKILL.md (shipped)

Content hash `5e5db96e61ff8552`. Same as v12 (see `../v12/CHANGELOG.md`) except in SKILL.md:

- The "Pick the mode first" table, which v10 placed at the top, is now a section near the end ("Which mode and
  reference for which text"). The opening paragraph gains one line pointing to it. Nothing else changed, so v13
  keeps v11's strict Edit mode and every genre reference.

Why: in arguments, explainers and literary analyses v9 and v12 received the same files apart from SKILL.md and
wrote texts with the same surface features, yet judges preferred v9's arguments and organization. The largest
difference at the point where the model starts drafting was the routing table at the top.

Result on the 12 school briefs (development data; 24 blind judgments, four texts per panel):

| | Mean rank (1 best) | Ranked first | Quality |
|---|---|---|---|
| v9, sample 1 | 2.25 | 10 of 24 | 7.71 |
| v9, sample 2 (same prompt, to measure noise) | 2.29 | 6 of 24 | 7.67 |
| v12 | 2.96 | 4 of 24 | 7.12 |
| v13 | 2.50 | 4 of 24 | 7.54 |

The two v9 samples tied (12 of 24). v13 against the v9 samples: -0.25 and -0.21 rank points, both intervals
crossing zero; against v12 +0.46. A routing probe (five fictional requests, two samples each) passed 10 of 10 for
both v12 and v13: application essay and "write my Why Tufts" went to Coach, "improve my abstract" and a learner's
"fix my grammar" got errors-only edits with suggestions listed separately, and an explainer request was written.

Caveat: these briefs had been read while diagnosing v12, so this is a development result. v13 inherits the held-out
Edit-mode results of v11 (its Edit text is unchanged) but was not itself re-run on the edit benchmark.
