# anti-ai-writing: development log

What was built, what changed, why, and the evidence behind each change. Append only; a reversal gets a new
entry. Numbers say what they were measured on. Raw materials and scripts are in this folder (see the
"Files" section at the end).

Dates are 2026-10-20 unless noted. "Judges" are separate Claude agents that compare two texts blind (they do
not know which condition produced which text); every pair gets two judges with different lenses (a strict
editor, and the genre's real reader: an admissions officer, an English teacher, a science teacher, a journal
reviewer, a blog editor). Detector scores are "% likely AI" from two open-source classifiers (D1 = Desklib
DeBERTa-v3-large trained on RAID; D2 = Fakespot RoBERTa-base).

---

## 0. Goal and constraints (from the user)

- Goal: a Claude skill that makes any writing task read like a strong human wrote it, used for every relevant
  writing task; for college applications it must reach the level of admitted essays at top-15 colleges
  ("specific, vulnerable, I feel I met this person"). The user also asked for detector testing, aiming below
  20% (Turnitin's display threshold).
- Constraints we added after research: no fabricated facts; no detector tricks (typos, homoglyphs); real
  application essays are coached, not ghostwritten (Common App fraud policy, YYGS "own work" certification);
  results reported honestly including failures.

## 1. Research phase (5 parallel research agents + completeness critic)

**1.1 Existing open-source skills.** Surveyed about 15 (notes: `notes/github_candidates.md`).
- blader/humanizer (58.8k stars, MIT) has the best structure (26 patterns ordered by strength, a
  mark/draft/check procedure, a no-fabrication rule) but is about 8k tokens, has no academic carve-outs, and its
  own blind test (issue #229) shows its rewrites made rhythm more uniform (60 to 101) and added aphoristic
  closers (38 to 61): a humanizer creating a new tell.
- conorbronsdon/avoid-ai-writing (MIT) has the best guardrails ("never inject" invented specifics, no staccato
  conversion) and self-measured evidence that word lists are weak (lift 0.9) while structural uniformity is
  strong (lift 11.7x).
- petergyang/no-ai-slop (MIT): minimum effective edit, portability test, eval checklist.
- stop-slop over-corrects (no adverbs, no passive, no triads); skill-deslop's examples invent facts.
- **Decision:** build fresh on humanizer's structure, borrow ideas (not text) from three MIT skills with
  credits, write original examples. Spend words on content and structure, not word lists.

**1.2 Evidence-graded catalog of AI tells** (`notes/tells_catalog.md`, 919 lines, ~40 sources).
- Strongest measured tells: corrective framing ("not X, it's Y"), participial "-ing" tails (2-5x human rate,
  Reinhart et al. PNAS 2025), importance flags ("this matters", 116x human for [a Claude model] per Graphite
  2026), summary closers, uniform sentence length, elegant variation, abstract application-essay nouns
  (journey, growth, resilience: Lee et al. 2025 on 30,000 admissions essays).
- Em dashes are a historical tell; current Claude uses almost none (Graphite, Oct 2026).
- Banning words backfires (Antislop 2025); expert readers detect AI mostly by content and structure (Russell
  et al. 2025).
- **Decision:** audit order content → staging → inflation → lessons → rhythm → tone → words → format.

**1.3 What admitted essays do** (`notes/essay_craft.md`).
- Officers want to "meet" a specific 17-year-old; the common failure is "so what?" (Yale podcast); AI essays
  are "slick but soulless" (Yale ep. 34).
- Techniques: odd specific detail, scene openings, earned (not announced) insight, vulnerability without
  wallowing, endings that open, plain voice.
- Several published admitted essays contain clichés; they work because the body is concrete.

**1.4 Detector facts** (`notes/detector_facts.md`). Turnitin: institutions only, 300-word minimum, 1-19% shown
as "*%"; added "AI bypasser" (humanizer) detection in 2025. Grammarly's score is a share of text; GPTZero's
is a document probability. Independent studies: detectors unreliable and biased against non-native writers.

**1.5 Policies and watermark** (`notes/policies_and_access.md`, verified by a fact-checking agent).
- Claude models from Aug 2026 embed an invisible text watermark that "may persist through some editing";
  detection is a private preview for approved organizations (educational organizations eligible; approved list
  not public). Turnitin/GPTZero cannot read it.
- Common App fraud policy names "the substantive content or output of an artificial intelligence platform"
  presented as one's own. YYGS: AI may "assist" but "your essay must be your own work", certified on signature.
  CJSJ: AI use must be disclosed; undisclosed AI text may be redacted.
- Correction logged: the Isley et al. 2026 admissions-penalty study covers one graduate program (GPTZero
  flags), not undergraduate admissions.

## 2. Measurement setup

**2.1 Local detectors.** Hugging Face was blocked at first; the user opened network access. D1 and D2 run
on CPU (`scripts/score.py`; long texts chunked at ~350 words, length-weighted mean). Binoculars with a
Qwen2.5-1.5B pair was tried and dropped: it did not separate AI from human calibration texts (Orwell 1.15 vs
AI 1.16), so it is not reported.

**2.2 Human baselines (pre-ChatGPT).**
- 16 admitted college essays (Hamilton classes of 2018 and 2022, Connecticut College class of 2025): only
  **5 of 16** under 20% on both detectors; several at 50-95%.
- 18 top-scored student argument essays (PERSUADE 2.0 corpus, grades 8-11): **7 of 18** under 20% on both.
- 3 science explainers from 2020 (Bert Hubert; The Conversation): 2 of 3.
- Pattern: vivid, specific human essays scored low; generic "I learned to be kind" essays scored high.
  **Insight:** these detectors partly detect generic writing.

**2.3 Tasks.** 7 briefs: Common App personal statement and a 250-word short answer for a fictional student
(Inês, from interview notes), 11th-grade argument essay (phones), science-club explainer (mRNA vaccines),
GreenBERT methods section (fact sheet), Gatsby analysis (4 provided quotes only), first-person blog post
(fact sheet). Facts files are the only permitted source of specifics.

**2.4 Conditions.** A = plain Claude (no skill), 2 samples per task. C = the skill's Edit mode applied to A's
sample 1. B = the skill's Write mode, 2 samples per task. All generated by fresh Claude agents.

## 3. Version 1 (skill v1)

**Design:** SKILL.md (hard rules, procedure, modes Write/Edit/Detect/Coach, genre notes, integrity) + four
references (tells, personal-essay, academic, examples). Description 185 characters (claude.ai limit 200).

**Results.**
| Measure | Plain (A) | Skill edit (C) | Skill write (B, v1) |
|---|---|---|---|
| Texts under 20% on both detectors | 7/14 | 4/7 | **14/14** |
| Judge: better writing (vs A) | n/a | **12/14** | **22/28** |
| Judge: more human (vs A) | n/a | 14/14 | 26/28 |
| Unsupported claims (judge-counted, same pairs) | 52 (A vs C), 104 (A vs B) | 14 | 56 |
| Human-likeness, mean of 10 | 5.4 / 5.3 | 7.0 | 7.3 |

- By genre (B vs A, better writing): argument 4-0, explainer 4-0, Gatsby 4-0, blog 4-0, report 3-1,
  short answer 3-1, **personal statement 0-4**.
- Detector drops came from real changes: B's argument essay took a specific position (ban covers lunch and
  passing periods), argued from school mechanics, conceded the lockdown objection; A used "glowing screens",
  a triadic thesis and "not a neutral tool; it is".
- Fact check of B's mRNA explainer: every named fact (Wolff 1990, Karikó & Weissman 2005, 2023 Nobel, 2024 RSV
  approval) correct.
- Edit mode caught A's errors: a Gatsby misquote ("Across the great distance" vs source "Compared to"), invented
  feelings in the personal statement, an invented habit in the blog.

**Why v1 lost personal statements (judges' consistent reasons):** A builds a better arc but invents feelings
and causes ("The shop taught me a different kind of listening", "Sitting across from her, I started
wondering"); v1 refuses to invent and produces "the interview notes reordered", with no reflection, skipped
the most vulnerable material (AP Chem lie), and ended almost every paragraph on a wry kicker.

## 4. Version 2

**Changes (why):**
- Coach mode: no example sentences built from the student's story; grammar as a list of discrete
  corrections (critic agent: LLM edits shift meaning and voice even when told "grammar only"; model-written
  examples homogenize essays).
- Personal-essay reference rewritten: depth questions to draw out the student's own reflections; spine chosen
  by stakes; arc and reflection section; "leave at least a third out"; sample mode: reflection only from the
  student's words.
- tells.md: S11 kicker endings everywhere, S12 staged self-correction, PE9 the over-corrected essay, maxim
  openers ("A rule that… A phone that…").
- Genre notes: explanations (angle, named verifiable examples); AI-use disclosure logging for journals.

**Results.**
- Personal statement v2 vs A: **0-4**; v2 vs v1: **0-2** (worse). Arc score 4-5 vs A's 8.
- Short answer v2 vs A: **0-4** (v1 had 3-1): regression.
- Argument v2 vs v1: 1-1.
- **Coach mode** (new test): critique of a real 186-word application draft rated 9/10 useful, no ghostwriting,
  not preachy; pressure test ("just write it, I'm out of time") 8/10, held the line, mildly preachy.
- All v2 texts under 5% on both detectors.

**Diagnosis:** extra sample-mode rules made the writer cautious; it cut the best material and still produced
kicker endings. Rules stated as guidance ("vary endings") did not change behavior.

## 5. Version 3

**Changes (why):** loosened sample mode (connective observations linking two facts allowed; no "leave a third
out"; uncomfortable material is often the spine); kicker check made countable ("list the last sentence of every
paragraph; if more than two are short or wry, rewrite"); explicit arc check.

**New test design:** the v1/v2 comparison was tilted (plain Claude invents reflection; the skill may not). Wrote
a depth-interview addendum where the fictional student answers the depth questions; both plain Claude (P) and
the skill (W) received the richer notes.

**Results.**
| Comparison | Better writing | More human | Unsupported claims |
|---|---|---|---|
| Personal statement, P vs W (depth notes) | P 4-0 | 2-2 | P 16, W 1 |
| Short answer, P vs W (depth notes) | 2-2 | W 4-0 | P 15, W 6 |
| Personal statement, A vs v3 (original notes) | A 2-0 | v3 2-0 | A 19, v3 0 |
| Short answer, A vs v3 (original notes) | A 2-0 | v3 2-0 | A 7, v3 1 |

- Depth notes reduced plain Claude's fabrication too (3-5 per essay vs 8-11).
- All personal-material texts (plain or skill) under 5% on both detectors.

**Diagnosis:** consistent across v1-v3: the skill's sample essays are more human and more faithful, but less well
built ("walks through the notes in order; climax in paragraph 7 of 9"). Edit mode (draft first, audit after)
had kept the arc (personal statement 1-1, short answer 2-0) with zero unsupported claims.

## 6. Version 4 (shipped to `.claude/skills/anti-ai-writing/`)

**Change (why):** two-pass drafting for personal essays and narratives: pass one writes for shape (arc, turn,
so-what, late climax), pass two runs the full Edit mode on that draft (fact diff cuts invented feelings,
audit passes, kicker count). Rationale: auditing while drafting produced flat essays; edit mode preserved arc.

**Results.**
| Comparison | Better writing | More human | Unsupported claims |
|---|---|---|---|
| Personal statement, P vs v4 (depth notes) | P 3-1 (v3: 4-0) | v4 3-1 | P 19, v4 6 |
| Short answer, P vs v4 (depth notes) | P 3-1 (v3: 2-2) | v4 3-1 | P 15, v4 7 |
| Personal statement, A vs v4 (original notes) | 1-1 (first win for any version here) | v4 2-0 | A 14, v4 4 |

- Arc scores for v4 personal statements 6-7 against plain's 7-8 (v3: 5-6).
- **Decision:** ship v4. Best personal-essay version so far, same rules elsewhere, and its coach mode is the one
  validated in section 4. Sample sizes for personal essays are small (2-4 pairs per cell); phase 2 tests v4 on 8
  personal-essay briefs.
- **Finding for the paper (fidelity–arc tradeoff):** across v1-v4, plain Claude's personal essays win on arc
  because it writes connective feelings and causes the student never stated (3-11 unsupported claims per essay).
  Forbidding that lowers judged arc; two-pass drafting recovers part of it. Depth answers from the student raise
  everyone's quality and cut plain Claude's fabrication by about half.

## 7. Measurement upgrade: third detector

Added D3 = SuperAnnotate/ai-detector (RoBERTa-large; training data includes Anthropic models and RAID; output
capped near 73% by label smoothing). Calibration: human 2.1-3.8%, AI 72.7-73.0%. It scored the 2005 Paul Graham
essay that D2 flagged at 56% as 2.2%. All earlier texts re-scored with D1-D3 (`eval/results/rescore3.json`).

## 8. Phase 2 plan (large evaluation)

20 briefs (4 fictional students × personal statement and short answer with depth notes; 4 argument; 4 explainer;
4 literary analysis with verified Gutenberg quotes) × 5 conditions: P plain; L word-list prompt (the common
"avoid delve, tapestry, em dashes" approach); H blader/humanizer applied to P's draft; E our Edit mode on P's
draft; O our Write mode. Two blind panel judges per brief rank all five; detectors D1-D3 score every text.

---

## Files

- `skill_versions/v1..v4/`: every version of the skill as tested.
- `eval/briefs/`: task briefs, fact sheets, fictional interview notes, Gatsby quotes.
- `eval/out/<condition>/`: every generated text. A = plain, B1/B2 = skill write v1/v2, C1 = skill edit,
  P3 = plain with depth notes, W3/N3 = skill v3 with/without depth notes, X4/Y4 = skill v4.
- `eval/results/`: detector scores (`*_scores.json`), judge outputs (`judges_*.json`), human baseline scores.
- `scripts/`: `score.py` (detectors), `assemble.py`, `judges.py` (tallies), `summarize.py`.
- `notes/`: research notes written by the research agents (our own text; third-party downloads not included).

## 9. Three-detector rescoring (all phase-1 texts and human baselines)

| Group | n | Under 20% on all three | D3 mean |
|---|---|---|---|
| Human admitted college essays (pre-2022) | 16 | **0** | 61.4 (D3 max is about 73) |
| Human PERSUADE argument essays (pre-2022) | 18 | 4 | about 44 |
| Plain Claude (A) | 14 | 5 | 28.5 |
| Plain Claude + skill edit (C1) | 7 | 4 | 17.2 |
| Skill write v1 (B1) | 14 | **14** | 3.5 |
| Skill v2-v4 personal essays | 16 | 16 | 2.4-4.9 |

- **Finding (fairness):** the detector whose training data includes Anthropic models flags every human admitted
  essay and passes every skill-written Claude text: on this genre the detectors invert. Likely cause: personal
  narrative is out of domain for detectors trained on Wikipedia, ELI5, scientific text and RAID; generic,
  polished human prose and template-like structure read as "AI", while concrete, idiosyncratic detail reads as
  "human" whoever wrote it. Paper must state this as a property of these open-source detectors, not of all
  detectors (GPTZero, Turnitin untested).

## 10. Phase 2 results: judges (20 briefs, 40 blind panel judgments)

Run as five workflows (`scripts/phase2.js`, seeds 1, 10-13). Each brief got two judges, a demanding editor and a
genre reader (admissions officer, English teacher or science teacher), each ranking all five texts blind with
labels shuffled. Texts: `eval/out/phase2/<condition>/`; judgments: `eval/results/phase2_judges.json`; summary:
`eval/results/phase2_summary_judges.json` (`scripts/analyze.py`).

| Condition | Mean rank (1 = best) [95% CI] | First places | Human-likeness /10 | Quality /10 | AI suspicion /5 | Unsupported claims per text |
|---|---|---|---|---|---|---|
| P plain | 4.62 [4.40, 4.80] | 0 | 4.50 | 5.62 | 4.10 | 3.38 |
| L word-list prompt | 2.27 [1.98, 2.62] | 6 | **7.33** | 7.38 | 2.55 | 2.65 |
| H humanizer edit of P | 3.48 [3.20, 3.75] | 1 | 5.75 | 6.28 | 3.33 | 1.82 |
| E our edit of P | 3.17 [2.83, 3.50] | 5 | 5.55 | 6.53 | 3.35 | 1.30 |
| O our write (v4) | **1.45** [1.23, 1.73] | **28** | 7.25 | **7.88** | **2.33** | **1.07** |

Friedman test across the five conditions (per-brief mean ranks): chi-square 49.6, p = 4e-10. Pairwise, O ranked
above P in 39 of 40 judgments, above L in 33 of 40 (Wilcoxon p = 0.027), above H in 38 of 40 and above E in 32 of 40.

By genre (mean rank of O; best competitor in brackets): argument 1.00 (L 2.00), explainer 1.00 (L 2.25),
literary analysis 1.00 (L 2.12), short answer 1.75 (E 2.50), **personal statement 2.50 (L 2.25, E 2.38)**.

What this says:
- Writing fresh with the skill wins clearly in the three school genres, and it has the fewest invented claims
  overall (1.07 against 3.38 for plain).
- **Editing loses to writing.** Both edit conditions (ours and the humanizer) land in the middle: they keep the
  plain draft's generic structure and some of its errors. Our Edit mode was built for minimal edits of human
  drafts, which is the wrong behaviour for an AI draft. This motivated Rebuild mode in v5.
- **The word-list prompt is a strong baseline.** It scored highest on human-likeness and voice. Judges said the
  skill's school essays read like an adult essayist, while the word-list essays sounded like an actual 11th grader.
  v5 adds a student-voice rule for school essays.
- **Personal statements are still the weak genre.** Judges criticised our texts for dropping the student's best
  detail (one editor: "leaves out the key self-indictment") and for packing too much into one paragraph. v5 adds a
  short checklist for this (section 11).

### 10b. Phase 2 detector results (100 texts, `eval/results/phase2_scores.json`)

Share of texts under 20% on all three detectors, by genre (4 briefs per genre):

| Genre | Plain | Word list | Humanizer edit | Our edit | Our write |
|---|---|---|---|---|---|
| Personal statement | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| Short answer | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| Argument | 0/4 | 0/4 | 0/4 | 0/4 | **4/4** |
| Explainer | 0/4 | 0/4 | 0/4 | 0/4 | 1/4 |
| Literary analysis | 1/4 | 3/4 | 2/4 | 2/4 | **4/4** |
| **Total** | 9/20 | 11/20 | 10/20 | 10/20 | **17/20** |

Mean scores (D1 / D2 / D3): plain 40.0 / 33.7 / 23.2; word list 20.0 / 19.7 / 7.5; humanizer 26.7 / 19.8 / 9.8;
our edit 26.3 / 17.2 / 11.9; our write 3.0 / 3.6 / 2.6.

- **The personal-essay finding got stronger.** Every model-written personal statement and short answer passed all
  three detectors, plain Claude included (scores 0-3%), while the 16 human admitted essays averaged 61% on D3 and
  none passed it. On this genre the detectors are not just weak; they point the wrong way.
- So the skill's detector advantage comes from the school genres (argument, literary analysis), where plain text
  fails and skill text passes. Explainers are the exception: three of four skill explainers scored 24-28% on one
  detector. Science explanation leaves less room for idiosyncratic detail.
- Editing a plain draft (ours or the humanizer) halves the scores but passes only half the texts. Writing fresh
  matters for detectors too, which supports the Rebuild mode in v5.

## 11. Version 5 (candidate)

Changes, each tied to a phase-2 failure:
1. **Rebuild mode** for AI-written drafts: extract the facts, check them, then write fresh with the Write
   procedure. Reason: edits of AI drafts kept the generic structure and ranked below fresh writing.
2. **Student voice for school essays**: write as the student (stated stance, contractions, plain words, more short
   sentences), avoid stock student openers, never invent an anecdote. Reason: the word-list baseline beat us on voice.
3. **Explainers talk to the reader** ("you") and give them something to try or picture.
4. **Personal-essay checklist** (`references/personal-essay.md` section 5): list the three best details and keep at
   least two; no paragraph with more than two beats; gloss anything an outsider would not know; set up before
   paying off; answer the prompt's own question; keep exact facts.

Test design (`scripts/phase2_v5.js`, six workflows, seeds 40-45): the same 20 briefs, a new five-way blind panel of
P, L and O (reused texts) plus V (v5 write) and R (v5 Rebuild of the plain draft P). Results: section 12.

## 12. Version 5 results: not shipped

Same 20 briefs, new five-way blind panels (P, L and v4's O reused; V = v5 write, R = v5 Rebuild of P), 40
judgments. Data: `eval/results/v5_judges.json`, `eval/results/v5_summary_judges.json`; texts in `eval/out/phase2/V`
and `R`; the tested skill in `skill_versions/v5/`.

| Condition | Mean rank | First places | Human-likeness | Quality | AI suspicion | Unsupported per text |
|---|---|---|---|---|---|---|
| P plain | 4.20 | 2 | 4.78 | 5.97 | 3.90 | 3.23 |
| L word list | 3.33 | 5 | 6.38 | 6.70 | 3.10 | 2.62 |
| O v4 write | **1.95** | **19** | 6.90 | **7.65** | 2.50 | 0.93 |
| V v5 write | 2.60 | 7 | **7.45** | 7.38 | **2.27** | 1.02 |
| R v5 Rebuild of P | 2.92 | 7 | 6.88 | 7.05 | 2.52 | **0.78** |

v4 ranked above v5 write in 28 of 40 judgments (Wilcoxon p = 0.055) and above v5 Rebuild in 30 of 40 (p = 0.022).
By genre (mean rank O / V / R): argument 1.12 / 2.25 / 4.00; explainer 1.50 / 1.62 / 3.00; literary analysis
1.62 / 2.88 / 1.75; personal statement 2.88 / 3.88 / 3.38 (plain 2.62, word list 2.25); short answer 2.62 / 2.38 / 2.50.

What we learned:
- **The student-voice rule bought human-likeness and cost reasoning.** v5's school essays scored higher on
  human-likeness and lower on AI suspicion, but judges caught simplified or faulty reasoning ("'Aspect' means
  appearance here, since the creature hasn't done anything yet") and crammed paragraphs. A younger register
  pulled the argument down with it.
- **Rebuild beat v4 only on literary analysis**, where re-checking the draft's readings of the quotes matters.
  On arguments it ranked 4.00: rebuilding from an AI draft still anchors on that draft's stock arguments.
- **The personal-essay checklist did not help** (v5 3.88 against v4 2.88 on personal statements).
- **Panel context changes personal-statement verdicts.** The same P and O texts were judged in both panels.
  O ranked above P in 8 of 8 personal-statement judgments in the phase-2 panel but in only 3 of 8 in this one. In
  the other genres the result held (8 of 8 in both). In phase 2, two of the five texts were edits of P and shared
  its sentences; judges noticed the overlap ("T5 and T4 share most of their content and many whole sentences")
  and may have marked down the whole family. Conclusion for the paper: the school-genre advantage is robust to
  panel composition; the personal-statement advantage is not, and plain generation's arcs (built partly on
  invented detail: 3.25 unsupported claims per text against 0.62) remain competitive with judges.

Decision: keep v4 as the shipped version for now; diagnose the judge feedback in depth and build v6 from what
worked (section 13).

## 13. Version 6: built from a diagnosis of 160 judgments

Workflow (`v6-diagnosis`): five genre analysts, a residual-tells hunter and a personal-essay specialist read every
judge comment from both panels and the texts themselves; a synthesizer proposed nine changes; two adversarial
critics (overfitting, side effects) reviewed them; a writer applied the survivors to a copy of v4. Full changelog
with counts and quotes: `skill_versions/v6/CHANGELOG.md`. The main findings behind the changes:

1. **Arguments win on construction, not ideas.** The v4 essays that ranked first stated the thesis against the
   nearest alternative (the usual compromise, a double standard) and let that one idea organize the essay; judges
   credited this in 16 of 16 judgments. v5 had largely the same ideas as a list of reasons. v6 adds an argument
   section: thesis against the nearest alternative, one worked case, the strongest objection to the writer's own
   remedy answered by changing the remedy, a concrete opening (never "I think" first, never "every student knows").
2. **Student register as a pass after the argument is built**, with a check that every paragraph's claim
   survives. v5's register raised human-likeness (7.75 vs 6.25 on arguments) and lowered AI suspicion (2.0 vs
   3.0 in 8 of 8 judgments) but cost structure when applied while drafting. Its example stance line became an
   opening template (3 of 4 v5 arguments start with "I think"), so the example is gone.
3. **Reading check** for any text that interprets a source: a quote can be exact and the reading wrong. About
   half of the claims judges flagged in literary analyses sat in the final paragraph, so the check says to read
   the last paragraph hardest.
4. **Rebuild routed by source.** With a facts or quotes file, keep the checked evidence and write fresh. With
   only a topic, the draft's examples and plan are the stock answer: write from step 1 with your own plan (v5's
   Rebuild kept the plain draft's outline and ranked 4th on arguments in 8 of 8 judgments).
5. **Beat outline before drafting** personal statements (spine, beats in cause order, joins, turn, prompt
   answer, ending from the notes), replacing v5's after-the-fact checklist, which did not fix order.
6. **Explanations:** an everyday opening with the answer in one sentence, one organizing idea, one worked number,
   misconceptions conceded with their size; v5's "talk to the reader as you" rule dropped (no measurable effect).
7. **Logic row** in the audit table: connectives that claim a cause the text does not show, and generalizations
   stated as fact.
8. **Evaluation hygiene:** v4 contained example phrases taken from the development personas ("a notebook with 61
   entries" and similar). v6 removes them, so phase-2 scores for v4 and v5 on those personas are slightly
   optimistic. The held-out briefs share nothing with the skill files (checked by search).

v6 SKILL.md: 189 lines (v4: 159); new `references/school-essays.md` (108 lines).

## 14. Held-out evaluation (phase 3): design

16 new briefs written after v6's design was fixed (`eval/briefs3/`): two new fictional students (personal
statement and short answer each), two arguments, two explainers, two literary analyses (Romeo and Juliet, Pride
and Prejudice; every quote checked against the Project Gutenberg text by script), and six genres never tested:
an email to a teacher, a cold email to a professor, a cover letter, a team blog post, a lab-report discussion and
a school news article. A checking agent fixed three weekday/date contradictions in the fact files and one
surname that matched a real scientist.

Six conditions per brief: P plain, L word list, H humanizer edit of P, F v4 write, S v6 write, B v6 Rebuild of P.
Three blind judges per brief: an editor and a genre reader as before, plus a second genre reader running on a
different model tier, to check that rankings do not depend on the judge model. Script: `scripts/phase3.js`.
