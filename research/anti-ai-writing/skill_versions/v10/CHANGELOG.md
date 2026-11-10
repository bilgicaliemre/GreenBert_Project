# v10: one skill, a mode per genre

Frozen before any held-out output was generated: content hash `d05f855dc7111b57` (sha256 over the files of
`anti-ai-writing/` in sorted walk order, first 16 hex digits).

## What changed from v9

1. **Mode table at the top of SKILL.md** ("Pick the mode first"): each kind of text maps to a mode (Coach, Edit,
   Write) and a reference file. Application essays and short answers stay Coach-only. Research text is Edit-first.
   School essays that will be graded as the student's own work go to Coach.
2. **New `references/short-answers.md`** (supplements, why us, short takes, activity list and honors). Built from
   16 real admitted short answers (MIT applicants in The Tech and on MIT's blogs; Tufts' "Supplements Revisited"
   and "Essays That Worked"; classes of 2026 or earlier) compared blind with model answers. Main content: real
   admitted answers are plainer and more whole-hearted than model answers; model answers are caught by
   over-crafting (stacked figures and names, labeled-object hooks, quips, planted metaphors, hedged or trailing
   endings), clipped sentences, contractions and colons. The activity-list section follows admissions offices'
   published advice and was not tested against real lists.
3. **New `references/research.md`** (replaces `academic.md`, keeps all of its content). Built from 24 winning ISEF
   abstracts (2014 to 2021, a third from Turkey) compared blind with model versions written from the same project
   notes. Adds: edit the researcher's own draft first (real abstracts with only their errors fixed stayed 100%
   judged human); what models add (fluency, hedges, promotion, narrated logic, lay simplification, stitched and
   balanced sentences); register rules (technical, passive in procedures, no contractions, no glossing).
4. `personal-essay.md` section 9 points to `short-answers.md`; `tells.md` points to `research.md`.
5. Description updated to name the modes.

## Development results (all in-sample; see DEVLOG section 23)

| Genre | Version | Judged human | Mean p(human) | AUC vs real | Quality |
|---|---|---|---|---|---|
| Research abstracts (24) | real | 100% | 86.6 | - | 5.7 |
| | real, errors fixed | 100% | 85.8 | 0.53 to 0.58 | 6.0 |
| | plain model | 2 to 17% | 33 to 38 | 1.00 | 6.1 to 6.2 |
| | v9 | 4% | 34.0 | 1.00 | 6.1 |
| | research guide r0 | 8% | 33.8 | 1.00 | 5.9 |
| | research guide r1 (in v10) | 6% | 34.8 | 1.00 | 6.1 |
| Short answers (16) | real | 100% | 87.3 | - | 4.8 |
| | plain model | 0% | 9.0 | 1.00 | 7.1 |
| | short-answer guide s0 | 0% | 9.7 | 1.00 | 7.0 |

r1 against plain, paired: +1.6 [-0.3, +3.5] on p(human), quality unchanged; it cut the judges' citations of hedges
(31% to 21%), glossed terms (15% to 4%), promotional claims (23% to 10%) and stock transitions (19% to 10%).
s0 against plain: +0.6 [-1.1, +2.4]. The s1 changes in `short-answers.md` (from s0's judgments) were not run on
development data before the freeze.

## Known limits

- No model version of either genre was mistaken for the real one by these judges (AUC 1.00). The modes reduce
  specific tells; they do not make model text pass as a student's.
- Short-answer writers worked from invented applicants (see DEVLOG 23 for why), so judges partly caught the
  invented content, not only the writing.
- Judges are models. Two lenses per genre; no human raters yet.
