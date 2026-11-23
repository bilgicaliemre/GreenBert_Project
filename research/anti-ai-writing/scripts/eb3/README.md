# EB3: v14 against four popular humanizer skills on real writing

Scripts behind the third edit benchmark (2026-11-23). Real texts and model outputs stay private; only aggregates are in
`eval/results/eb3/`.

## Texts

- 48 English-learner essays from ELLIPSE (12 per proficiency band, grade 9 or above, 250 to 500 words, none used before;
  `select3.py` reproduces the first edit benchmark's selection and excludes it).
- 48 winning ISEF abstracts, 2014 to 2021, from 12 categories never collected before (`isef_collect2.py`,
  `isef_fetch2.py`; four per category). No finalist names or schools are stored.

## Conditions (`build_edit3.py`)

Task E, "Can you improve it?" on the real text: C errors-only copyedit, PI plain, BI plain plus "Make the smallest edits
you can and keep my wording.", S14 our skill v14, and four third-party skills given the same request with their
installed files embedded: HB blader/humanizer (4.0.0 plus unreleased edits), HT hardikpandya/stop-slop,
HN petergyang/no-ai-slop (1.0.6), HA conorbronsdon/avoid-ai-writing (3.39.0).

Task R, "had AI help me improve it, but now it sounds like AI wrote it. Can you make it sound more human?" on the plain
rewrite (PI): RP plain, R14, RB, RT, RN, RA.

Every job: two texts per agent, pinned effort, an explicit no-tools line, the same request for every condition.
Scripts that ship with the third-party skills cannot run in this setup, as for every condition.

## Measures

- `build_judge3.py`: blind single-text piles of 12, two lenses per genre, p(written by the person) 0 to 100 and quality.
- `build_mp3.py`: blind meaning check. Task E edits are compared with the real original; task R outputs with the text
  they were given, so "added" there counts what the skill invented.
- `analyze_x.py`: the repo's `analyze.py` plus `--exclude` (drops refused outputs, listed in
  `eval/results/eb3/excluded.json`).
- `tokscan.py`: per-condition output tokens and tool use from the agent transcripts.

## Known problem: the triggering message reached every agent

The workflow harness passes the user message that started a run to every agent. For this run that message asked to add
humanizer skills and a "Claude watermark remover" to our skill. On the ISEF abstracts, 22 of 384 edits were refusals
or safety-classifier stops that cited it (plain 8, stop-slop 6, no-ai-slop 4, blader 2, v14 2), and 8 of 72 judge piles
came back empty (rerun; 2 stayed empty). These outputs are excluded. Learner-essay edit sizes match a run from before that
message within 0.02, and no essay output refused. Rerun the abstracts from a neutral message before using them in a paper.

Set `BENCH_MODEL` to the model alias to run them; paths point to the session that ran them.
